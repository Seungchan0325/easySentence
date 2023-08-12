import openai

openai.api_key = "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"

def query(message: list[dict[str, str]]) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message
    )
    print("Debug: ", response)
    return response['choices'][0]['message']['content']

def splitSentence(sentence: str) -> list[str]:
    message = [
        {"role": "user", "content": ""},
        {"role": "user", "content": f'""{sentence}""'}
    ]

    text = query(message)

    return text

def easyWord(sentence: str) -> str:
    message = [
        {"role": "user", "content": ""},
        {"role": "user", "content": f'""{sentence}""'}
    ]

    text = query(message)

    return text

def easySentence(sentence: str) -> list[str]:
    sentences = splitSentence(sentence)
    
    ret = []
    for i in sentences:
        ret.append(easyWord(i))
    
    return ret

def main():
    text = input()

    result = easySentence(text)

    print(result)

if __name__ == '__main__':
    main()