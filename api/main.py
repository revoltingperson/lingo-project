from fastapi import FastAPI
import linecache
import os
import random
import requests

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
    selected_line = selected_line.split()[ONE_WORD]
    return req_to_yandex(selected_line)


def word_matches_pos(target_pos: str, definitions: dict) -> bool:
    for obj in definitions['tr']:
        if obj['pos'] == target_pos:
            return True
    return False


def generate_exercise(word_count: int) -> list:
    pos = ['noun', 'adjective', 'verb', 'adverb']
    target_pos: str = random.choices(pos, weights=[2, 2, 2, 1], k=1)[ONE_WORD]
    word_indexes: list = random.choices(range(TOTAL_WORDS), k=word_count)
    word_set = [target_pos]
    at_least_one_correct = False
    for ar_in, word_ind in enumerate(word_indexes):
        continue_search = True
        while continue_search:
            one_word_obj = prepare_word(word_ind)
            if not one_word_obj or one_word_obj.get('def') is None:
                return []
            if one_word_obj['def']:
                matched = word_matches_pos(target_pos, one_word_obj['def'][ONE_WORD])
                if matched:
                    at_least_one_correct = True
                if ar_in == word_count - 1 and not at_least_one_correct:
                    pass
                else:
                    word_set.append({'word': one_word_obj['def'][ONE_WORD]['text'],
                                     'pos': target_pos if matched else one_word_obj['def'][ONE_WORD]['pos']})
                    continue_search = False
                    continue
            word_ind = word_ind + 1 if word_ind < TOTAL_WORDS else 1
    return word_set


@app.get("/get-new-task/")
async def root(word_count: int = 7):
    if word_count > 10:
        word_count = 10
    res_payload = generate_exercise(word_count)
    if not res_payload:
        return {"error_msg": "internal api problem"}
    return {"words": res_payload}
