import qrcode


def caesar_cipher():
    m = input("Please enter your message:\n")
    key = int(input("Please enter the key:\n"))
    return ''.join([chr(((ord(char) - 65 + key) % 26) + 65) if char.isupper() else chr(
        ((ord(char) - 97 + key) % 26) + 97) if char.islower() else char for char in m])


print(caesar_cipher())
