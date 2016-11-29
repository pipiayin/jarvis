import sys
import os


os.environ['NLTK_DATA'] = 'nltk_data'
from textblob import TextBlob
b = TextBlob("Simple is better than complex.")
print(b.tags)
b = TextBlob("What happens in the president election?")

print(b.tags)
print(dir(b))
print(b.noun_phrases)
