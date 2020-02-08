def mystery(num):
    if num <= 0:
        return
    mystery(num - 2)
    print(num, end="")
    mystery(num - 1)


mystery(3)
