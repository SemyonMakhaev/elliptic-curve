#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Elliptic curve points."""
from abc import ABCMeta
from copy import copy
from functools import reduce

from lib.points import Point


def convert_polynomial(polynomial):
    """Convert polynomial to int."""
    if polynomial is None:
        return None
    return reduce(lambda acc, power: acc ^ (1 << power), polynomial, 0)


class BinaryPoint(Point, metaclass=ABCMeta):
    # pylint: disable=abstract-method
    """Binary point from field of characteristic P."""
    def __init__(self, params):
        super().__init__(params)

        payload = params.get('payload')

        if not isinstance(payload, int):
            payload = convert_polynomial(payload)

        self.polynomial = payload

    def inverse(self, number):
        """Inverses a specified number."""
        values = [number, self.polynomial]
        bits = [1, 0]

        while values[-1] != 1:
            value_1_len = values[-1].bit_length()
            value_2_len = values[-2].bit_length()

            if value_1_len == value_2_len:
                values.append(values[-1] ^ values[-2])
                bits.append(bits[-1] ^ bits[-2])
            elif value_1_len < value_2_len:
                values.append(values[-1] << (value_2_len - value_1_len))
                bits.append(bits[-1] << (value_2_len - value_1_len))
                values[-1] = values[-1] ^ values[-3]
                bits[-1] = bits[-1] ^ bits[-3]
            else:
                values.append(values[-2] << (value_1_len - value_2_len))
                bits.append(bits[-2] << (value_1_len - value_2_len))
                values[-1] = values[-1] ^ values[-2]
                bits[-1] = bits[-1] ^ bits[-2]

        return self.modulus(bits[-1])

    def modulus(self, number):
        """Get modulus of number."""
        bit_length = number.bit_length()
        polynomial_bit_length = self.polynomial.bit_length()

        while bit_length >= polynomial_bit_length:
            number ^= self.polynomial << (bit_length - polynomial_bit_length)
            bit_length = number.bit_length()

        return number

    def multiply(self, this_num, that_num):
        """Multiplies numbers."""
        if not this_num or not that_num:
            return 0

        result = this_num

        for bit in bin(that_num)[3:]:
            result <<= 1
            if bit == '1':
                result ^= this_num

        return self.modulus(result)

    def __str__(self):
        if self.x is None or self.y is None:
            return 'e'

        return '({}, {})'.format(
            bin(self.x)[2:].rjust(self.polynomial.bit_length() - 1, '0'),
            bin(self.y)[2:].rjust(self.polynomial.bit_length() - 1, '0'),
        )

    __repr__ = __str__


class Point2N(BinaryPoint):
    """Point on not a supersingular curve."""
    # pylint: disable=no-member
    def __add__(self, addend):
        if not isinstance(addend, BinaryPoint):
            raise TypeError('Addend is not a point of non-supersingular curve: {}'.format(addend))

        if self.x is None or self.y is None:
            return addend

        if addend.x is None or addend.y is None:
            return self

        result = {
            'payload': self.polynomial,
            'coefficients': [self.a, self.b, self.c],
        }

        if self.x == addend.x:
            if self.x == 0 or self.y != addend.y:
                return Point2N({})
            numerator = self.multiply(self.x, self.x) ^ self.multiply(self.a, self.y)
            denominator = self.inverse(self.multiply(self.x, self.a))
            factor = self.multiply(numerator, denominator)
            factor_square = self.multiply(factor, factor)
            result['x'] = factor_square ^ self.b ^ self.multiply(factor, self.a)
        else:
            numerator = self.y ^ addend.y
            x_xor = self.x ^ addend.x
            denominator = self.inverse(x_xor)
            factor = self.multiply(numerator, denominator)
            factor_square = self.multiply(factor, factor)
            factorized_a = self.multiply(self.a, factor)
            result['x'] = factor_square ^ x_xor ^ factorized_a ^ self.b

        factorized_x = self.multiply(factor, self.x ^ result['x'])
        result['y'] = self.y ^ factorized_x ^ self.multiply(self.a, result['x'])

        return Point2N(result)

    def __mul__(self, factor):
        if factor < 0:
            new_point = copy(self)
            new_point.y = self.multiply(self.x, self.a) ^ self.y

            return new_point * (-factor)

        if factor == 0:
            return Point2N({})

        return self.factorize(factor)


class Point2S(BinaryPoint):
    """Point on a supersingular curve."""
    # pylint: disable=no-member
    def __add__(self, addend):
        if not isinstance(addend, BinaryPoint):
            raise TypeError('Addend is not a point of supersingular curve: {}'.format(addend))

        if self.x is None or self.y is None:
            return addend

        if addend.x is None or addend.y is None:
            return self

        result = {
            'payload': self.polynomial,
            'coefficients': [self.a, self.b, self.c],
        }

        if self.x == addend.x:
            if self.x == 0 or self.y != addend.y:
                return Point2N({})
            numerator = self.multiply(self.x, addend.x) ^ self.b
            denominator = self.inverse(self.a)
            factor = self.multiply(numerator, denominator)
            result['x'] = self.multiply(factor, factor)
        else:
            numerator = self.y ^ addend.y
            x_xor = self.x ^ addend.x
            denominator = self.inverse(x_xor)
            factor = self.multiply(numerator, denominator)
            result['x'] = self.multiply(factor, factor) ^ self.x ^ addend.x

        result['y'] = self.multiply(self.x ^ result['x'], factor) ^ self.y ^ self.a

        return Point2N(result)

    def __mul__(self, factor):
        if factor < 0:
            new_point = copy(self)
            new_point.y = self.y ^ self.a

            return new_point * (-factor)

        if factor == 0:
            return Point2S({})

        return self.factorize(factor)
