import re
from typing import List

from regexpath import constants


class PathElement:
    def __init__(self, element):
        self.origin = element
        self.result = self.convert(element)

    @property
    def mid_index(self):
        return len(self.result) // 2

    def join(self):
        if (len(self.result) % 2) == 0:
            self.result.insert(self.mid_index + 1, r")\s*?")
            self.result.insert(self.mid_index - 1, r"\s*?(")
            self.result.insert(self.mid_index, r"[\s\S]*?")
        return "".join(self.result)

    def embed(self, prop):
        self.result[self.mid_index - 1] = self.result[self.mid_index - 1].replace(
            "[^>]*>", f"[^>]*{prop.result[0]}[^>]*>"
        )
        self.result.pop()

    def merge(self, element):
        self.result[self.mid_index : self.mid_index] = element.result

    @staticmethod
    def convert(element: str):
        if element.startswith("@"):
            return [rf'{element[1:]}=["\']*([^"\']+)["\']*']
        elif "[" not in element:
            return [rf"<{element}[^>]*>", constants.CLOSURE.format(element)]
        else:
            tag = element.split("[")[0]
            if "contains(@" in element:
                contains = constants.RE_CONTAINS.search(element)
                if contains:
                    contains = contains.groupdict()
                    return [
                        rf'<{tag}[^>]*{contains.get("property")}=["\']*[^"\']*{contains.get("value")}[^"\']*["\']*[^>]*>',
                        constants.CLOSURE.format(tag),
                    ]
            else:
                prop = constants.RE_PROPERTY.search(element)
                if prop:
                    prop = prop.groupdict()
                    return [
                        rf'<{tag}[^>]*{prop.get("property")}=["\']*{prop.get("value")}["\']*[^>]*>',
                        constants.CLOSURE.format(tag),
                    ]

    def __repr__(self):
        kws = [f"{key}={value!r}" for key, value in self.__dict__.items()]
        return "{}({})".format(type(self).__name__, ", ".join(kws))


class Parser:
    def compile(self, path: str) -> re.Pattern:
        elements = [PathElement(element) for element in path.split("/") if element]
        compiled_regex = re.compile(self.parse(elements))
        return compiled_regex

    @staticmethod
    def parse(elements: List[PathElement]) -> str:
        """Converts element node to regex equivalent

        '//h3/a':
         - h3 parent -> '<h3[^>]*>[\s\S]*</h3>'
         - a child -> '(<a[^>]*>[\s\S]*<\a>)'
         '//h1[@itemprop="name"]' -> '<h1[^>]*itemprop="name"[^>]*>[^<]*</h1>'
        """
        result = []
        for element in elements:
            if result:
                if len(element.result) == 1:
                    result.embed(element)
                else:
                    result.merge(element)
            else:
                result = element
        return result.join()

    def __repr__(self):
        kws = [f"{key}={value!r}" for key, value in self.__dict__.items()]
        return "{}({})".format(type(self).__name__, ", ".join(kws))


class RegexPath:
    parser = Parser()

    def __init__(self, source):
        self.source = source

    def xpath(self, path: str) -> List[str]:
        return self.parser.compile(path).findall(self.source)
