import re

_WORD_RE = re.compile(r"[a-zA-Z0-9']+")

def normalize(text:str) -> str:
    text = text.lower()
    tokens = _WORD_RE.findall(text)
    return " ".join(tokens)

test = normalize("I Got liBraries in my mind and an Album in my soul. And I don't play boy")
print(test)

