#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Elliptic curve prime point."""
from copy import copy

from lib.points.point import Point


class PrimePoint(Point):
    """Prime point on elliptic curve."""
    def __init__(self, params):
        super().__init__(params)
        self.modulus = self.payload[0] if self.payload else None

    def inverse(self, number):
        """Inverses a specified number."""
        number %= self.modulus
        previous_num = 0
        current_num = 1
        previous_res = self.modulus
        current_res = number

        while current_res != 1:
            factor = previous_res // current_res
            previous_res, current_res = current_res, previous_res % current_res
            previous_num, current_num = current_num, previous_num - (factor * current_num)

        return current_num % self.modulus

    def __add__(self, addend):
        if self.x is None or self.y is None:
            return addend

        if addend.x is None or addend.y is None:
            return self

        if self.x == addend.x:
            if self.y == 0 or self.y != addend.y:
                return PrimePoint({})

            numerator = 3 * (self.x ** 2) + self.a
            denominator = 2 * self.y
        else:
            numerator = addend.y - self.y
            denominator = addend.x - self.x

        denominator = self.inverse(denominator)
        coefficient = (numerator * denominator) % self.modulus
        res_x = (pow(coefficient, 2, self.modulus) - self.x - addend.x) % self.modulus
        res_y = (coefficient * (self.x - res_x) - self.y) % self.modulus
        return PrimePoint({
            'x': res_x,
            'y': res_y,
            'payload': [self.modulus],
            'coefficients': [self.a, self.b, self.c],
        })

    def __mul__(self, factor):
        if factor < 0:
            new_point = copy(self)
            new_point.y = self.modulus - self.y

            return new_point * -factor

        if factor == 0:
            return PrimePoint({})

        return self.factorize(factor)

    def __copy__(self):
        return PrimePoint({
            'x': self.x,
            'y': self.y,
            'curve_type': self.curve_type,
            'payload': self.payload,
            'coefficients': list(filter(bool, [self.a, self.b, self.c]))
        })
