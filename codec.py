import math
from functools import lru_cache


@lru_cache
def convert_binary_to_grey(binary):
    grey = binary[0]
    for i in range(1, len(binary)):
        grey += str(int(binary[i - 1]) ^ int(binary[i]))
    return grey


@lru_cache
def convert_grey_to_binary(gray):
    binary = gray[0]
    for i in range(1, len(gray)):
        binary += str(int(binary[i - 1]) ^ int(gray[i]))
    return binary


@lru_cache
def calculate_genome_length(a, b, precision):
    return int(math.log2((b - a) * math.pow(10, precision) + 1))


@lru_cache
def convert_binary_to_decimal(binary, a, precision):
    decimal = int(binary, 2)
    return round(a + decimal / (10 ** precision), 2)


@lru_cache
def convert_decimal_to_binary(x, a, b, precision):
    length = calculate_genome_length(a, b, precision)
    decimal = (x - a) * (10 ** precision)
    bin_str = bin(int(decimal)).replace("0b", "")
    return '0' * (length - len(bin_str)) + bin_str
