from konlpy.tag import Kkma

import openai
import json

class EasySentenceTranslator:
    def __init__(self, api_key: str) -> None:
        openai.api_key = api_key

        with open('./simplify_sentence_prompt.txt', 'r', encoding='utf-8') as f:
            self.simplify_sentence_prompt = f.read()

        self.kkma = Kkma()

    def query(self, prompt: str) -> str:
        messages = [{'role': 'user', 'content': prompt}]

        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=messages,
            temperature=1
        )

        if response['choices'][0]['finish_reason'] != 'stop':
            raise Exception("GPT didn't answer")

        return response['choices'][0]['message']['content']

    def parse_json(self, text: str):
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
        prompt = self.simplify_sentence_prompt + f'\n\n ```{sentence}```'

        while True:
            answer = self.query(prompt)
            json_object = self.parse_json(answer)

            if json_object == -1:
                # print('again')
                # print('prompt: ', prompt)
                # print('answer: ', answer)
                continue
            else:
                break

        return json_object['sentences']

    def translate(self, text: str) -> list[list[str]]:
        sentences = self.kkma.sentences(text)

        ret = []
        for sentence in sentences:
            ret.append(self.simplifySentence(sentence))
        
        return ret