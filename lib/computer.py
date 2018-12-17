#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""Elliptic curve computer."""
import re

from lib.points import points_factory

INSTRUCTION_PATTERN = re.compile(r'^\((.+?), (.+?)\) ([+*]) (?:\((.+?), (.+?)\)|([\S]+))$')

HANDLERS = {
    '+': lambda this, that: this + that,
    '*': lambda this, that: this * that
}

BASES = {
    '0b': 2,
    '0o': 8,
    '0x': 16
}


def parse_number(number):
    """Parsing by a radix."""
    radix = number[:2]
    base = 10

    if radix in BASES:
        base = BASES.get(radix, 10)

    return int(number, base)


class Computer:
    """Computer class."""
    # pylint: disable=too-few-public-methods
    def __init__(self, curve_type, payload, coefficients):
        self.payload = payload
        self.coefficients = coefficients
        self.curve_type = curve_type
        self.cache = {}

    def calc(self, raw_instruction):
        """Instruction calculation."""
        if raw_instruction in self.cache:
            return self.cache[raw_instruction]

        left, handler, right = self._parse_instruction(raw_instruction)
        result = handler(left, right)
        self.cache[raw_instruction] = result

        return result

    def _get_point(self, x, y):
        """Creates point."""
        params = {
            'x': parse_number(x),
            'y': parse_number(y),
            'curve_type': self.curve_type,
            'payload': self.payload,
            'coefficients': self.coefficients
        }

        return points_factory(self.curve_type, params)

    def _parse_instruction(self, raw_instruction):
        """Raw instruction parsing."""
        match = re.findall(INSTRUCTION_PATTERN, raw_instruction)[0]

        if not match:
            raise Exception('Incorrect instruction: {}'.format(raw_instruction))

        x1, y1, operator, x2, y2, factor = match

        left = self._get_point(x1, y1)
        right = self._get_point(x2, y2) if x2 and y2 else int(factor)
        handler = HANDLERS[operator]

        return left, handler, right
