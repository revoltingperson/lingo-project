from fastapi import FastAPI
import linecache
import os
import random
import requests
import uvicorn

TOTAL_WORDS = 233464
YANDEX_URL = "https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key="
ONE_WORD = 0
API_KEY = os.environ.get('YANDEX_API')

app = FastAPI()


def req_to_yandex(word: str) -> dict:
    yandex_dict_res = requests.post(YANDEX_URL + API_KEY, data={
        "lang": "en-en",
        "text": f"{word}"
    })
    if yandex_dict_res.status_code != 200:
        return {}
    return yandex_dict_res.json()


def prepare_word(line_in: int) -> dict:
    selected_line = linecache.getline('english.txt', line_in)
    selected_line.strip(".,")
    if selected_line.endswith('\n'):
        selected_line = selected_line[:-1]
    if len(selected_line) < 3:
        return {}
    selected_line = selected_line.split()[ONE_WORD]
    pack = req_to_yandex(selected_line)
    if not pack or pack.get('def') is None:
        return {}
    new_obj = {'word': None, 'pos': []}
    if pack['def']:
        new_obj['word'] = pack['def'][ONE_WORD]['text']
        for obj in pack['def']:
            for sub_obj in obj['tr']:
                if sub_obj['pos'] not in new_obj['pos']:
                    new_obj['pos'].append(sub_obj['pos'])
        if 'participle' in new_obj['pos']:
            new_obj['pos'].remove('participle')
            new_obj['pos'].extend(('verb', 'adjective'))
            new_obj['pos'] = list(set(new_obj['pos']))
    return new_obj


def generate_exercise(word_count: int) -> list:
    pos = ['noun', 'adjective', 'verb', 'adverb']
    target_pos: str = random.choices(pos, weights=[2, 2, 2, 1], k=1)[ONE_WORD]
    word_indexes: list = random.choices(range(TOTAL_WORDS), k=word_count)
    word_set = [target_pos]
    at_least_one_correct = False
    for ar_in, word_ind in enumerate(word_indexes):
        one_word_obj: dict = {}
        while not one_word_obj:
            one_word_obj = prepare_word(word_ind)
            if not one_word_obj:
                return []
            if one_word_obj['word'] is None:
                one_word_obj.clear()
            else:
                matched = target_pos in one_word_obj['pos']
                if matched:
                    at_least_one_correct = True
                if ar_in == word_count - 1 and not at_least_one_correct:
                    one_word_obj.clear()
                else:
                    word_set.append(one_word_obj)
                    continue
            word_ind = word_ind + 1 if word_ind < TOTAL_WORDS else 1
    return word_set


@app.get("/get-new-tasks/")
async def task_generator(word_count: int = 7):
    if word_count > 10:
        word_count = 10
    res_payload = generate_exercise(word_count)
    if not res_payload:
        return {"error_msg": "internal api problem"}
    print(res_payload)
    return {"words": res_payload}
