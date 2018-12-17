#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Elliptic curve points."""
# pylint: disable=invalid-name
from abc import ABCMeta, abstractmethod
from copy import copy


class Point(metaclass=ABCMeta):
    """
    Base point on elliptic curve delegates computation to a Point
    of a specified curve type.
    """
    # pylint: disable=too-many-instance-attributes
    def __init__(self, params):
        self.x = params.get('x')
        self.y = params.get('y')
        self.curve_type = params.get('curve_type')
        self.payload = params.get('payload')
        self.coefficients = params.get('coefficients', [None] * 3)
        self._unpack_coefficients()

    def _unpack_coefficients(self):
        """Coefficients unpacking."""
        if len(self.coefficients) < 3:
            self.coefficients.append(None)

        self.a, self.b, self.c = self.coefficients

    def factorize(self, factor):
        """Point factorization."""
        result = copy(self)

        for bit in bin(factor)[3:]:
            result += result

            if bit == '1':
                result += self

        return result

    @abstractmethod
    def inverse(self, number):
        """Inverses a specified number."""
        raise NotImplementedError()

    @abstractmethod
    def __add__(self, addend):
        raise NotImplementedError()

    @abstractmethod
    def __mul__(self, factor):
        raise NotImplementedError()

    def __str__(self):
        if self.x is None or self.y is None:
            return 'e'

        return '({}, {})'.format(self.x, self.y)

    __repr__ = __str__
