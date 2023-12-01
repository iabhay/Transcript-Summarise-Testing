from googletrans import Translator


class TranslateHandler:
    def __init__(self):
        pass

    def translate(self, content, target):
        translator = Translator()
        result = translator.translate(content, dest=target)
        return result
