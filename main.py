import string


def cesar_cipher(text, key, cipher):
    if type(text) == str and type(key) == int:
        shift = 1 if cipher else -1
        list_of_crypted_chars = []
        for char in text:
            list_of_crypted_chars.append(chr((ord(char) + shift * key) % 1_114_112))

        crypted_text = "".join(list_of_crypted_chars)
        return crypted_text
    else:
        raise (TypeError)


def hack_cesar_cipher(crypted_text, alphabet):
    if type(crypted_text) == str and type(alphabet) == str:
        for possible_key in range(0, 1_114_112):
            possible_uncryption = cesar_cipher(crypted_text, possible_key, cipher=False)
            if possible_uncryption[0] in alphabet:
                print(possible_key)
                print(possible_uncryption)
                print("_" * 20)
    else:
        raise (TypeError)


def vigenere_cipher(text, password, cipher):
    list_of_crypted_chars = []
    list_of_keys = [ord(char) for char in password]

    for index, current_char in enumerate(text):

        current_key = list_of_keys[index % len(list_of_keys)]
        current_crypted_char = cesar_cipher(current_char, current_key, cipher)

        list_of_crypted_chars.append(current_crypted_char)

    crypted_text = "".join(list_of_crypted_chars)

    return crypted_text


# if __name__ == "__main__":
#     message = "le chocolat est bon"

#     crypted_text = cesar_cipher(message, 12, cipher=True)  # exo 1
#     print(crypted_text)

#     initial_message = cesar_cipher(crypted_text, 12, cipher=False)  # exo 2
#     print(initial_message == message)

#     hack_cesar_cipher(crypted_text, alphabet=string.printable)  # exo3

#     crypted_message = vigenere_cipher(
#         text=message, password="Azerty12345!", cipher=True
#     )
#     print(crypted_message)
#     initial_message = vigenere_cipher(
#         text=crypted_message, password="Azerty12345!", cipher=False
#     )
#     print(initial_message)

from PIL import Image


def afficher_image(path):
    image = Image.open(path)
    image.show()
    return image


def valeur_pixel(image, x, y):
    pixel_value = image.getpixel((x, y))
    print(f"La valeur du pixel {x}, {y} est {pixel_value}")


def text_to_binaire(texte):
    return "".join(format(ord(c), "08b") for c in texte)


def pixels_pairs(image):
    pixels = list(image.getdata())
    pixels_pairs = [p if p % 2 == 0 else p - 1 for p in pixels]
    new_img = Image.new("L", image.size)
    new_img.putdata(pixels_pairs)
    return new_img


def encoder_message(image, message):

    message_binaire = text_to_binaire(message) + "1111111111111110"
    pixels = list(image.getdata())

    if len(message_binaire) > len(pixels):
        raise ValueError(
            "Le message est trop long"
        )  # vérification du message pour voir si il est trop long par rapport aux nombre de pixels

    pixels_modifies = []
    for i in range(len(message_binaire)):
        pixel = pixels[i]
        if message_binaire[i] == "1":
            pixels_modifies.append(pixel + 1)
        else:
            pixels_modifies.append(pixel)

    pixels_modifies += pixels[len(message_binaire) :]

    new_img = Image.new("L", image.size)
    new_img.putdata(pixels_modifies)
    return new_img


def decoder_message(image):
    pixels = list(image.getdata())
    bits = [str(p % 2) for p in pixels]
    message_binaire = "".join(bits)

    octets = [message_binaire[i : i + 8] for i in range(0, len(message_binaire), 8)]
    message = ""
    for octet in octets:
        if octet == "11111111":
            break
        message += chr(int(octet, 2))
    return message


if __name__ == "__main__":
    img = Image.open("asset/image_steph.png")

    img_pairs = pixels_pairs(img)

    message_secret = "Bonjour"
    img_encoded = encoder_message(img_pairs, message_secret)
    img_encoded.save("image_encoded.png")

    img_test = Image.open("image_encoded.png").convert("L")
    message_decode = decoder_message(img_test)

    print("Message original :", message_secret)
    print("Message décodé   :", message_decode)
