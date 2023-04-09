import pytest

from coding import *
from codec import *


@pytest.mark.parametrize("binary,gray", [
    ("1111101111", "1000011000"),
    ("1111101110", "1000011001"),
    ("1010101010", "1111111111"),
    ("0000000000", "0000000000")
])
def test_binary_to_gray(binary, gray):
    assert convert_binary_to_grey(binary) == gray


@pytest.mark.parametrize("gray,binary", [
    ("1000011000", "1111101111"),
    ("1000011001", "1111101110"),
    ("1111111111", "1010101010"),
    ("0000000000", "0000000000")
])
def test_convert_grey_to_binary(gray, binary):
    assert convert_grey_to_binary(gray) == binary


@pytest.mark.parametrize("a,b,precision,result", [
    (0, 10.23, 2, 10),
    (-5.12, 5.11, 2, 10),
    (0, 3.1, 1, 5),
])
def test_genome_length(a, b, precision, result):
    assert calculate_genome_length(a, b, precision) == result


@pytest.mark.parametrize("binary,a,b,precision,result", [
    ('00011', 0, 3.1, 1, 0.3),
    ('00111', 0, 3.1, 1, 0.7)
])
def test_convert_binary_to_decimal(binary, a, b, precision, result):
    assert convert_binary_to_decimal(binary, a, precision) == result


@pytest.mark.parametrize("x,a,b,precision,result", [
    (0.3, 0, 3.1, 1, '00011'),
    (0.7, 0, 3.1, 1, '00111')
])
def test_convert_decimal_to_binary(x, a, b, precision, result):
    assert convert_decimal_to_binary(x, a, b, precision) == result
