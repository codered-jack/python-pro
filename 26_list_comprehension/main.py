import pandas as pd

data = pd.read_csv("nato_phonetic_alphabet.csv")
print(data)

phonetic_dict = { row.letter: row.code for (index, row) in data.iterrows() }

print(phonetic_dict)

user_word = input("Type your word: ").upper()

nato_list = [phonetic_dict[letter] for letter in user_word]
print(nato_list)

