def mult_two(a: int, b: int, c: int) -> int:
    return a * 2, b / 4, c + a * b

if __name__ == '__main__':
    print('Example: ')
    print(mult_two (int(input()), int(input()), int(input()) ))