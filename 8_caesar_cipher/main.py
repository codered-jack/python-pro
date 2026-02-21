from art import logo

print(logo)
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


def caesar(original_text, shift_amount, direction):
    caesar_text = ""
    shift_amount = shift_amount % len(alphabet)

    if direction == "decode":
        shift_amount = shift_amount * -1

    for char in original_text:
        if char in alphabet:
            alphabet_index = alphabet.index(char) + shift_amount
            caesar_text += alphabet[alphabet_index]
        else:
            caesar_text += char

    return caesar_text


should_continue = True

while should_continue:
    direction = input("Type 'encode' to encrypt, type 'decode' to decrypt:\n")
    text = input("Type your message:\n").lower()
    shift = int(input("Type the shift number:\n"))

    result = caesar(original_text=text, shift_amount=shift, direction=direction)

    print(f"Here is the {direction} {result}")

    restart = input("Type 'yes' if you want to go again. Otherwise type 'no'.\n").lower()

    if restart == "no":
        should_continue = False
        print("Bye!")


