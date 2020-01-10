def f(text: str):
    if len(text) % 2 == 0:
        mid = len(text) // 2
    else:
        mid = (len(text) + 1) // 2
    return text[mid]


print(f("Annie"))
