import argparse
import src.easySentence as easySentence

def main(args: argparse.Namespace):
    with open(args.input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    translator = easySentence.EasySentenceTranslator("OPENAI API KEY")
    
    result = translator.translate(text)
    for i in result:
        for j in i:
            print(j)
        print('-' * 50)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-file', dest='input_file', required=True, help='입력 파일')

    args = parser.parse_args()

    main(args)