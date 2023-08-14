import argparse
import openai
import json

openai.api_key = ""

def query(prompt: str) -> str:
    messages = [{"role": "user", "content": prompt}]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7
    )
    print(prompt)
    print(response['choices'][0]['message']['content'])

    if response['choices'][0]['finish_reason'] != 'stop':
        print("Error: gpt didn't answer")
        exit(-1)
    return response['choices'][0]['message']['content']

def parse_json(text: str):
    markdown = text.find("```")
    start_idx = 0
    if markdown != -1:
        start_idx = markdown + 2
    l = text.find('{', start_idx)
    r = text.rfind('}') + 1
    text = text[l:r]

    return json.loads(text)

def translateToEasySentence(sentence: str) -> list[str]:
    prompt = f'''
나는 언어장애인들이 한글 문장을 이해하기 쉽도록 한글 문장을 쉬운 문장으로 바꾸고 있다.

이를 위한 과정은
STEP 1: 문장을 나눌 수 있다면, 여러 개의 문장으로 나눈다. (예시: "나는 그가 떠난 것을 안다." -> "그가 떠났다.", "나는 그것을 안다.")
STEP 2: 나눈 문장의 단어를 쉬운 단어로 바꾸어 준다.
이다.

위의 과정의 결과를 JSON 형식으로 sentences 키를 가진 문자열 목록으로 생성하라.

아래의 문장이 한글 문장이다.

"{sentence}"
'''
#세 개의 역따옴표로 구분된 한글 문장이 주워진다.
    
    answer = query(prompt)
    #print("Debug: ", answer)
    json_object = parse_json(answer)
    return json_object['sentences']

def splitText(text: str) -> list[str]:
    prompt = f'''
세 개의 역따옴표로 구분된 문단이 주워진다.
문단을 문장 단위로 나눈다.
그 결과를 JSON 형식으로 sentences 키를 가진 문자열 목록으로 생성하라.

```{text}```
'''
    answer = query(prompt)
    #print("Debug: ", answer)
    json_object = parse_json(answer)
    return json_object['sentences']

def main(args: argparse.Namespace):
    with open(args.input_file, 'r', encoding='utf-8') as f:
        text = f.read()

        sentences = splitText(text)
        for sentence in sentences:
            for easy_sentence in translateToEasySentence(sentence):
                print(easy_sentence)
            print('-'*50)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-file', dest='input_file', required=True, help='입력 파일')

    args = parser.parse_args()

    main(args)