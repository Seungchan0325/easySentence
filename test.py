import src.easySentence as easySentence

translator = easySentence.EasySentenceTranslator("OPENAI API KEY")

with open('./samples/test_samples.txt', 'r', encoding='utf-8') as input, open('./samples/samples_result.txt', 'w', encoding='utf-8') as output:
    while True:
        sentence = input.readline()
        if not sentence:
            break
        result = translator.simplifySentence(sentence)
        print(result)
        buf = '[' + ', '.join(f'"{i}"' for i in result) + ']\n'
        output.writelines(buf)