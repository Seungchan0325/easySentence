import argparse
import openai
import json

openai.api_key = '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'

def query(prompt: str) -> str:
    messages = [{'role': 'user', 'content': prompt}]

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages,
        temperature=1
    )

    if response['choices'][0]['finish_reason'] != 'stop':
        print("Error: gpt didn't answer")
        exit(-1)

    return response['choices'][0]['message']['content']

def parse_json(text: str) -> bool:
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

def translateToEasySentences(sentence: str) -> list[str]:
    prompt = translate_to_easy_sentences_prompt + f'\n\n ```{sentence}```'

    while True:
        answer = query(prompt)
        json_object = parse_json(answer)

        if json_object == -1:
            print('again')
            continue
        else:
            break

    return json_object['sentences']

def splitText(text: str) -> list[str]:
    prompt = split_text_prompt + f'\n\n```{text}```'
    
    while True:
        answer = query(prompt)
        json_object = parse_json(answer)

        if json_object == -1:
            print('again1')
            continue
        else:
            break

    return json_object['sentences']

def main(args: argparse.Namespace):
    with open(args.input_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    global translate_to_easy_sentences_prompt
    global split_text_prompt
    with open('./translate_to_easy_sentences_prompt.txt', 'r', encoding='utf-8') as f:
        translate_to_easy_sentences_prompt = f.read()
    with open('./split_text_prompt.txt', 'r', encoding='utf-8') as f:
        split_text_prompt = f.read()

    sentences = splitText(text)
    for sentence in sentences:
        for easy_sentence in translateToEasySentences(sentence):
            print(easy_sentence)
        print('-'*50)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-file', dest='input_file', required=True, help='입력 파일')

    args = parser.parse_args()

    main(args)