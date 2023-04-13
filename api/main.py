from fastapi import FastAPI
import linecache
import random
import requests
from bs4 import BeautifulSoup
import uvicorn
import time
from fastapi.middleware.cors import CORSMiddleware
# from fastapi import APIRouter

TOTAL_WORDS = 58109
ONE_WORD = 0
DICTIONARY_URL = "https://www.thefreedictionary.com/"
POS = {'n': 'noun', 'adj': 'adjective', 'v': 'verb', 'adv': 'adverb'}
app = FastAPI()

origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    return {
        "word": def_body.section.h2.text.replace("·", "").lower(),
        "pos": list(set(cleaned))
    }


def req_to_free_dictionary(selected_word: str) -> dict:
    get_dict_page = requests.get(DICTIONARY_URL + selected_word)
    if get_dict_page.status_code != 200:
        return {}
    processed = parse_response(get_dict_page.text)
    return processed if processed else {}


def get_base_form(word: str, line: int) -> str or None:
    while line - 1:
        selected_line = linecache.getline('english.txt', line - 1)
        line -= 1
        if selected_line[0] != word[0]:
            break
        if selected_line.startswith(word) and not selected_line.endswith(('ing', 'ed')):
            return selected_line
    return None


def prepare_word(line_in: int) -> dict:
    selected_line = linecache.getline('english.txt', line_in)
    if selected_line.endswith('\n'):
        selected_line = selected_line[:-1]
    if len(selected_line) < 3:
        return {}
    if selected_line.endswith(('ing', 'ed')):
        trimmed = selected_line[:-2] if selected_line.endswith('ing') else selected_line[:-1]
        temp = get_base_form(trimmed, line_in)
        if temp:
            selected_line = temp
    pack = req_to_free_dictionary(selected_line)
    return pack


def generate_exercise(word_count: int) -> dict:
    target_pos: str = random.choices(list(POS.values()), weights=[2, 2, 2, 1], k=1)[ONE_WORD]
    word_indexes: list = random.choices(range(TOTAL_WORDS), k=word_count)
    word_set = pull_words(target_pos, word_count, word_indexes)
    return word_set


def pull_words(target_pos, word_count, word_indexes) -> dict:
    word_set = {"target": target_pos, "set": []}
    at_least_one_correct = False
    for ar_in, word_ind in enumerate(word_indexes):
        one_word_obj: dict = {}
        while not one_word_obj:
            one_word_obj = prepare_word(word_ind)
            if one_word_obj:
                matched = target_pos in one_word_obj['pos']
                if matched:
                    at_least_one_correct = True
                if ar_in == word_count - 1 and not at_least_one_correct:
                    one_word_obj.clear()
                else:
                    word_set['set'].append(one_word_obj)
                    continue
            word_ind = word_ind + 1 if word_ind < TOTAL_WORDS else 1
    return word_set


@app.get("/get-new-tasks/")
async def task_generator(word_count: int = 7):
    if word_count > 10:
        word_count = 10
    start = time.time()
    res_payload = generate_exercise(word_count)
    if not res_payload:
        return {"error_msg": "internal api problem"}
    print(res_payload)
    end = time.time()
    print(f"execution time:  {end - start}")
    return res_payload

# if __name__ == '__main__':
#     uvicorn.run(app, host="0.0.0.0", port=8000)
