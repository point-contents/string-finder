import re
from trie import Trie
from get_strings import Constants

def get_forbidden_words(filename):
    with open(filename, 'r') as wordlist:
        return [word.strip().lower() for word in wordlist]


badwords = get_forbidden_words("badwords")

def trie_regex_from_words(words):
    trie = Trie()
    for word in words:
        trie.add(word)
    return re.compile(trie.pattern(), re.IGNORECASE)

def find(word):
    return union.search(word)


constants = Constants()
constants.filename = "lex.py"
strings = constants.get_strings()


union = trie_regex_from_words(badwords)

for ids in strings:
    target_word = ids['value']
    result = re.findall(union, target_word)
    if result:
        print(result)
        print(ids)

