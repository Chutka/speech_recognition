import argparse

from recognizer.recognizer import Recognizer, RecognizerTypes

if __name__ == '__main__':
    ap = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='''\
Аргументы командной строки, для использования программы
----------------------''',
        epilog='''
----------------------'''
    )
    ap.add_argument(
        '--type',
        '-t',
        type=str,
        help='''Поля тип используемого средства для распознавания: GOOGLE_SPEECH_RECOGNITION значение по умолчанию
Возможные значения:
- Sphinx
- Google Speech Recognition
- Google Cloud Speech
- Wit.ai
- Microsoft Bing Voice Recognition
- Houndify
- IBM Speech to Text
''',
        default=RecognizerTypes.GOOGLE_SPEECH_RECOGNITION.value
    )
    ap.add_argument(
        '--device_index',
        type=int,
        help='Индекс используемого микрофона. По умолчанию стоит 0',
        default=0,
    )
    ap.add_argument(
        '--file',
        '-f',
        help='''Имя файла. Если передать, то текст будет записан в файл, иначе просто будет выведен в консоль''',
        default=None
    )
    ap.add_argument(
        '--audio',
        type=str,
        help='''Имя файла аудио, из которого будет производить распознавание речи.''',
        default=None
    )
    args = ap.parse_args()

    r = Recognizer(RecognizerTypes(args.type), device_index=args.device_index)

    if args.audio:
        audio = r.from_file(args.audio)
    else:
        audio = r.listen()

    recognized_text = None
    if audio:
        recognized_text = r.recognition(audio)
        print(recognized_text)
        if args.file is not None:
            with open(args.file, 'w') as file:
                print('Результат программы записан в файл - {}'.format(args.file))
                file.write(recognized_text)
    else:
        print('Не удалось записать аудио')
