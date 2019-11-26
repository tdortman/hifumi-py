import qrcode


def caesar_cipher():
    m = input("Please enter your message:\n")
    key = int(input("Please enter the key:\n"))
    return ''.join([chr(((ord(char) - 65 + key) % 26) + 65) if char.isupper() else chr(
        ((ord(char) - 97 + key) % 26) + 97) if char.islower() else char for char in m])


print(caesar_cipher())






qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=0,
    )
    qr.add_data(cipher)
    qr.make(fit=True)





qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=0,
    )
    qr.add_data("Ima leave it like this for now. You're amazing Annie!!!")
    qr.make(fit=True)

    file_name = '{0}.png'.format(current_time[2:])
    img = qr.make_image(fill_color="black", back_color="white")

    img.save(r'C:\Users\TIMBOLA\Desktop\HifuBot\hifumi_cipher_images\{0}'.format(file_name))
    with open(r'C:\Users\TIMBOLA\Desktop\HifuBot\hifumi_cipher_images\{0}'.format(file_name), 'rb') as picture:
        await ctx.channel.send(file=discord.File(picture, "new_filename.png"))