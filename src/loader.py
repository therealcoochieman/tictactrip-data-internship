from math import isnan


def input_num(string):
    num = input(string)
    return int(num) if num.isdigit() else -1

def parse_num(num):
    num = float(num)
    return num if not isnan(num) else 0
