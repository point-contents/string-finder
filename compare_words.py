import re
from trie import Trie

def get_forbidden_words(filename):
    with open(filename, 'r') as wordlist:
        return [word.strip().lower() for word in wordlist]


badwords = get_forbidden_words("badwords")

def trie_regex_from_words(words):
    trie = Trie()
    for word in words:
        trie.add(word)
    return re.compile("\b" + trie.pattern +f"\b", re.IGNORECASE)

def find(word):
    def fun():
        return union.match(word)
    return fun



