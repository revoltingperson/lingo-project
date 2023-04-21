import linecache
import queue
import random
import threading
import time
import concurrent.futures
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from my_log.logger import app_log

TOTAL_WORDS = 58109
ONE_WORD = 0
DICTIONARY_URL = "https://www.thefreedictionary.com/"
POS = {'n': 'noun', 'adj': 'adjective', 'v': 'verb', 'adv': 'adverb'}
PATH_TO_FILE = 'english.txt'
TASK_SIZE = 7
MAX_TASKS = 10

grammar_tasks = queue.Queue(maxsize=MAX_TASKS)
event = threading.Event()


def generate_task_thread():
    tasks = 0
    while True:
        if grammar_tasks.full():
            app_log.info("queue is full")
            event.clear()
        if not event.is_set():
            event.wait()
            app_log.info(f"q size before: {grammar_tasks.qsize()}")
        else:
            tasks += 1
            start = time.time()
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                dics_for_resp = [executor.submit(generate_one) for _ in range(MAX_TASKS - grammar_tasks.qsize())]
                for future in concurrent.futures.as_completed(dics_for_resp):
                    try:
                        wanted_dic = future.result()
                        grammar_tasks.put(wanted_dic)
                    except Exception as exc:
                        app_log.info('%r generated an exception: %s' % (exc, wanted_dic))

            app_log.info(f"q size now: {grammar_tasks.qsize()}")
            app_log.info(f"generated tasks total: {tasks}")
            end = time.time()
            dec = "{:.2f}".format(end - start)
            app_log.info(f"stacked filled in within: {dec} seconds")


def generate_one():
    target_pos: str = random.choices(list(POS.values()), weights=[2, 2, 2, 1], k=1)[ONE_WORD]
    previously_used = []
    start = time.time()
    word_set = {"target": target_pos, "set": []}
    at_least_one_correct = False
    while TASK_SIZE != len(word_set['set']):
        generate_now = TASK_SIZE - len(word_set['set'])
        while len(set(previously_used).intersection(
                word_indexes := random.choices(range(TOTAL_WORDS), k=generate_now))):
            continue
        previously_used.extend(word_indexes)
        lexical_items = [get_word_from_file(word_ind) for word_ind in word_indexes]
        http_async_res = asyncio.run(send_reqs_with_words(lexical_items))
        words_dict_objects: list = find_valid_definitions(http_async_res)
        if not at_least_one_correct:
            at_least_one_correct = any(d_obj for d_obj in words_dict_objects if target_pos in d_obj['pos'])
        no_duplicates = [obj for obj in words_dict_objects if obj not in word_set['set']]
        word_set['set'].extend(no_duplicates)
        if len(word_set['set']) == TASK_SIZE and not at_least_one_correct:
            word_set['pos'] = word_set['set'][random.randint(0, TASK_SIZE - 1)]['pos'][ONE_WORD]

    end = time.time()
    dec = "{:.2f}".format(end - start)
    app_log.info(f"pull words function for {word_set} words is {dec}")

    return word_set


def get_word_from_file(line_in: int) -> str:
    if line_in > TOTAL_WORDS:
        line_in = 0
    selected_line = linecache.getline(PATH_TO_FILE, line_in)
    if selected_line.endswith('\n'):
        selected_line = selected_line[:-1]
    if len(selected_line) < 3:
        return get_word_from_file(line_in + 1)
    if selected_line.endswith(('ing', 'ed')):
        trimmed = selected_line[:-2] if selected_line.endswith('ing') else selected_line[:-1]
        temp = get_base_form(trimmed, line_in)
        if temp:
            selected_line = temp[:-1]
    return selected_line


def get_base_form(word: str, line: int) -> str or None:
    while line - 1:
        selected_line = linecache.getline(PATH_TO_FILE, line - 1)
        line -= 1
        if selected_line[0] != word[0]:
            break
        if selected_line.startswith(word) and not selected_line.endswith(('ing', 'ed')):
            return selected_line
    return None


def find_valid_definitions(responses: list) -> list:
    lex_pack = []
    for resp_obj in responses:
        if type(resp_obj) == str:
            good_parse = parse_response(resp_obj)
            if good_parse:
                lex_pack.append(good_parse)
    return lex_pack


async def scrape_page(session, url):
    async with session.get(url) as resp:
        if resp.status == 200:
            return await resp.text()


async def send_reqs_with_words(word_list: list):
    coro_objs = []

    async with aiohttp.ClientSession() as session:
        for word in word_list:
            coro_objs.append(
                scrape_page(session, DICTIONARY_URL + word)
            )

        results = await asyncio.gather(*coro_objs)

    return results


def parse_response(page: str) -> dict or None:
    soup = BeautifulSoup(page, "lxml")
    def_body = soup.find(attrs={"id": "Definition"})
    if def_body is None or def_body.section is None:
        return None
    all_is = def_body.find_all(name="i")
    cleaned = []
    for tag in all_is:
        if tag.parent.get('class') is not None:
            if any(word for word in ['etyseg', 'runseg'] if word in tag.parent.get('class')):
                continue
        for no_dot in tag.text.split("."):
            if POS.get(no_dot) is not None:
                cleaned.append(POS.get(no_dot))
    if not cleaned:
        return None
    header_cleaned = "".join([c for c in def_body.section.h2.text if c.isalpha()])
    return {
        "word": header_cleaned,
        "pos": list(set(cleaned))
    }
