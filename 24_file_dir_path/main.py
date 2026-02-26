with open("./Input/Letters/starting_letter.txt") as letter_file:
    letter = letter_file.read()
    print(letter)

with open("./Input/Names/invited_names.txt") as names_file:
    names = names_file.readlines()

for name in names:
    stripped_name = name.strip("\n")
    with open(f"./Output/ReadyToSend/letter_for_{stripped_name}.txt", mode="w") as final:
        final.write(letter.replace("[name]", stripped_name))
