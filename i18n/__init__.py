
import json
locales = ["en", "ru"]


class Translate:
    def __init__(self, locale, module):
        self.locale = locale
        self.module = module

    def __call__(self, id):
        # open file
        with open("i18n/" + self.locale + ".json", "r", encoding="utf8") as f:
            # read file
            data = json.load(f)
            # return data
            try:
                id = self.module + "." + id
                return data[self.module][id]
            except BaseException:
                return "Error: Failed to load translation"
