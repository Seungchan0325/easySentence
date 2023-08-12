import openai
import json

openai.api_key = ""

def query(question: str) -> str:
    messages = [{"role": "user", "content": question}]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=1
    )
    print("Debug: ", response)
    return response['choices'][0]['message']['content']

def parse_json(text: str):
    l = text.find('{')
    r = text.rfind('}') + 1
    text = text[l:r]

    return json.loads(text)

def splitSentence(sentence: str) -> list[str]:
    message = """우리의 목표는 문장을 이해하기 쉽도록 여러 완전한 문장으로 나누는 것입니다.
문장을 나누는 방법은 하나의 문장을 같은 의미를 한 여러 개의 문장으로 나누는 것 또는 이 외에도 여러 방법으로 문장을 나눌 수 있습니다.

입력은 한글로 이루어진 한국어 문장입니다.

출력은 다음과 같은 형식을 따릅니다.
아래와 같은 JSON 형식의 sentences배열에 나누어진 문장을 추가합니다. 나누지 않았을 경우에도 sentences 배열에 추가합니다.
{
	"sentences": []
}

입력이 "%s" 일 때 JSON 파일 출력하세요.""" % sentence

    text = query(message)
    json_object = parse_json(text)
    return json_object['sentences']

def easyWord(sentence: str) -> str:
    message = """우리의 목표는 한국어 문장에 어려운 단어가 있다면 쉽고 간결한 단어로 바꾸는 것이다.
만약 어려운 단어를 바꿀 쉬운 단어가 없다면 어려운 단어를 풀어쓰면 된다.
어려운 단어가 없다면 아무 작업을 하지 않아도 좋다.

입력은 한국어 문장으로 주워진다.

출력은 다음과 같은 형식을 따른다.
아래와 같은 JSON 형식의 sentence 문자열에 결과를 대입한다.
{
	"sentence": ""
}

입력이 "%s" 일 때 JSON 파일을 출력하라.""" % sentence

    text = query(message)
    json_object = parse_json(text)
    return json_object['sentence']

def easySentence(sentence: str) -> list[str]:
    sentences = splitSentence(sentence)
    
    ret = []
    for i in sentences:
        ret.append(easyWord(i))
    
    return ret

def main():
    text = input()
    result = easySentence(text)

    for i in result:
        print(i)

if __name__ == '__main__':
    main()