from konlpy.tag import Kkma

import openai
import json

class EasySentenceTranslator:
    def __init__(self, api_key: str) -> None:
        openai.api_key = api_key
        
        dir_path = __file__
        last_separator = dir_path.rfind('\\')
        if last_separator == -1:
            last_separator = dir_path.rfind('/')
        dir_path = dir_path[0:last_separator]
        
        with open(dir_path + '/simplify_sentence_prompt.txt', 'r', encoding='utf-8') as f:
            self._simplify_sentence_prompt = f.read()

        self._kkma = Kkma()

    def _query(self, prompt: str) -> str:
        messages = [{'role': 'user', 'content': prompt}]

        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=messages,
            temperature=0.5
        )

        if response['choices'][0]['finish_reason'] != 'stop':
            raise Exception("GPT didn't answer")

        return response['choices'][0]['message']['content']

    def _parse_json(self, text: str):
        markdown = text.find('```')
        start_idx = 0
        if markdown != -1:
            start_idx = markdown + 2
        l = text.find('{', start_idx)
        r = text.rfind('}') + 1
        text = text[l:r]

        try:
            ret = json.loads(text)
        except:
            return -1

        return ret

    def simplifySentence(self, sentence: str) -> list[str]:
        prompt = self._simplify_sentence_prompt + sentence

        while True:
            answer = self._query(prompt)
            json_object = self._parse_json(answer)

            if json_object == -1:
                print('again')
                print('prompt: ', prompt)
                print('answer: ', answer)
                continue
            else:
                break

        return json_object['sentences']

    def translate(self, text: str) -> list[list[str]]:
        sentences = self._kkma.sentences(text)

        ret = []
        for sentence in sentences:
            ret.append(self.simplifySentence(sentence))
        
        return ret
