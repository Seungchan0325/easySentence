import openai

openai.api_key = "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"

pre_message = []
def split_sentence(sentence: str) -> str:
    message = pre_message
    message.append({"role": "user", "content": f'""{sentence}""'})
    print(message)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message
    )
    print(response)

    text = response['choices'][0]['message']['content']
    print(text)
    return text 

sentence = input()

a = split_sentence(sentence)
print(a)