import requests
import re
from collections import Counter
import os

url = "https://dummyjson.com/quotes"

response = requests.get(url)
data = response.json()

quotes = data['quotes']
texts = [quote['quote'] for quote in quotes]

excluded_words = ['a', 'an', 'the', 'and', 'but', 'or', 'in', 'on', 'at', 'for', 'to', 'with']

word_list = [re.findall(r'\b\w+\b', text.lower()) for text in texts]

words = [word for sublist in word_list for word in sublist if word not in excluded_words]

word_counts = Counter(words)

top_ten_words = word_counts.most_common(10)

print("Top 10 de palabras más repetidas (excluyendo artículos y conectores):")

for word, count in top_ten_words:
    print(f"{word}: {count}")

directory = 'archivos_texto'
if not os.path.exists(directory):
    os.makedirs(directory)

for word, count in top_ten_words:
    file_name = f'{directory}/{word}.txt'
    with open(file_name, 'w') as file:
        file.write(f'La palabra "{word}" se repite {count} veces.\n')

    os.chmod(file_name, 0o400)

print("Se han creado los archivos de texto con los nombres de las palabras más repetidas.")
