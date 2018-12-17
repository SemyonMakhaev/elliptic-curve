#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Integration tests for elliptic curve computer."""
from unittest import TestCase

from lib import Computer


class EllipticCurveTest(TestCase):
    """Elliptic curve test class."""
    def test_prime_mul(self):
        """Should multiply points in Zp."""
        curve_type = 'p'
        payload = [
            26959946667150639794667015087019630673557916260026308143510066298881
        ]
        coefficients = [
            -3,
            18958286285566608000408668544493926415504680968679321075787234672564
        ]

        computer = Computer(curve_type, payload, coefficients)

        # pylint: disable=line-too-long
        instructions = {
            '(19277929113566293071110308034699488026831934219452440156649784352033, 19926808758034470970197974370888749184205991990603949537637343198772) * 2':
                '(11838696407187388799350957250141035264678915751356546206913969278886, 2966624012289393637077209076615926844583158638456025172915528198331)',
            '(19277929113566293071110308034699488026831934219452440156649784352033, 19926808758034470970197974370888749184205991990603949537637343198772) * 26959946667150639794667015087019625940457807714424391721682722368061':
                'e'
        }
        # pylint: enable=line-too-long

        for instruction in instructions:
            actual = computer.calc(instruction)

            self.assertEqual(str(actual), instructions[instruction])

    def test_prime_sum_points(self):
        """Should sum points in Zp."""
        curve_type = 'p'
        payload = [13]
        coefficients = [1, 1]

        computer = Computer(curve_type, payload, coefficients)

        instructions = {
            '(4, 2) + (10, 6)': '(11, 2)',
            '(0, 1) + (0, 1)': '(10, 7)',
            '(1, 4) + (1, 4)': '(8, 12)',
            '(4, 2) + (4, 2)': '(8, 1)',
            '(5, 1) + (5, 1)': '(4, 11)',
            '(7, 0) + (7, 0)': 'e',
            '(8, 1) + (8, 1)': '(11, 2)',
            '(10, 6) + (10, 7)': 'e',
            '(11, 2) + (11, 2)': '(4, 11)'
        }

        for instruction in instructions:
            actual = computer.calc(instruction)

            self.assertEqual(str(actual), instructions[instruction])

    def test_prime_sum_points_and_numbers(self):
        """Should sum points and numbers in Zp."""
        curve_type = 'p'
        payload = [17]
        coefficients = [2, 2]

        computer = Computer(curve_type, payload, coefficients)

        instructions = {
            '(4, 2) + (10, 6)': '(11, 16)',
            '(0, 1) + (0, 1)': '(1, 15)',
            '(1, 4) + (1, 4)': '(13, 14)',
            '(4, 2) + (4, 2)': '(8, 16)',
            '(5, 1) + (5, 1)': '(6, 3)',
            '(7, 0) + (7, 0)': 'e',
            '(8, 1) + (8, 1)': '(9, 4)',
            '(10, 6) + (10, 7)': 'e',
            '(11, 2) + (11, 2)': '(16, 5)'
        }

        for instruction in instructions:
            actual = computer.calc(instruction)

            self.assertEqual(str(actual), instructions[instruction])

    def test_prime_mul_large(self):
        """Should correctly multiply large points and numbers in Zp."""
        curve_type = 'p'
        payload = [6277101735386680763835789423207666416083908700390324961279]
        coefficients = [
            6277101735386680763835789423207666416083908700390324961276,
            2455155546008943817740293915197451784769108058161191238065
        ]

        computer = Computer(curve_type, payload, coefficients)

        # pylint: disable=line-too-long
        instruction = '(235734543244397598274, 1157127558854445202073904637583650569445255326968907996897) * 50000000000000000000000000000000000'
        expected = '(4078202597509891473402912356459053652474434919592369011542, 4420576899388766547143116187637032682625183218536716470203)'
        # pylint: enable=line-too-long

        actual = computer.calc(instruction)

        self.assertEqual(str(actual), expected)

    def test_non_supersingular(self):
        """Should sum and multiply points and numbers on a non-supersingular curve."""
        curve_type = 'n'
        payload = [4, 1, 0]
        coefficients = [1, 1, 1]

        computer = Computer(curve_type, payload, coefficients)

        instructions = {
            '(0b1000, 0b0010) + (0b1000, 0b0010)': '(0110, 0111)',
            '(0b1000, 0b0010) * 1': '(1000, 0010)',
            '(0b1000, 0b0010) * 2': '(0110, 0111)',
            '(0b1000, 0b0010) * 3': '(1010, 0101)',
            '(0b1000, 0b0010) * 4': '(0001, 0110)',
            '(0b1000, 0b0010) * 5': '(1100, 1000)',
            '(0b1000, 0b0010) * 6': '(0111, 0110)',
            '(0b1000, 0b0010) * 7': '(1111, 1100)',
            '(0b1000, 0b0010) * 8': '(0000, 0001)',
            '(0b1000, 0b0010) * 9': '(1111, 0011)',
            '(0b1000, 0b0010) * 10': '(0111, 0001)',
            '(0b1000, 0b0010) * 11': '(1100, 0100)',
            '(0b1000, 0b0010) * 12': '(0001, 0111)',
            '(0b1000, 0b0010) * 13': '(1010, 1111)',
            '(0b1000, 0b0010) * 14': '(0110, 0001)',
            '(0b1000, 0b0010) * 16': 'e'
        }

        for instruction in instructions:
            actual = computer.calc(instruction)

            self.assertEqual(str(actual), instructions[instruction])

    def test_prime_mul_2(self):
        """Should multiply points in Zp."""
        curve_type = 'p'
        payload = [199]
        coefficients = [1, 3]

        computer = Computer(curve_type, payload, coefficients)

        instructions = {
            '(1, 76) * 1': '(1, 76)',
            '(1, 76) * 2': '(158, 166)',
            '(1, 76) * 3': '(138, 47)',
            '(1, 76) * 196': '(1, 123)',
            '(1, 76) * 197': 'e',
            '(1, 76) * 198': '(1, 76)'
        }

        for instruction in instructions:
            actual = computer.calc(instruction)

            self.assertEqual(str(actual), instructions[instruction])

    def test_prime_mul_large_2(self):
        """Should nultiply large points and numbers in Zp."""
        curve_type = 'p'
        payload = [
            6277101735386680763835789423207666416083908700390324961279
        ]
        coefficients = [
            -3,
            2455155546008943817740293915197451784769108058161191238065
        ]

        computer = Computer(curve_type, payload, coefficients)

        # pylint: disable=line-too-long
        instructions = {
            '(602046282375688656758213480587526111916698976636884684818, 174050332293622031404857552280219410364023488927386650641) * 6277101735386680763835789423176059013767194773182842284080':
                '(602046282375688656758213480587526111916698976636884684818, 6103051403093058732430931870927447005719885211462938310638)',
            '(602046282375688656758213480587526111916698976636884684818, 174050332293622031404857552280219410364023488927386650641) * 6277101735386680763835789423176059013767194773182842284082':
                '(602046282375688656758213480587526111916698976636884684818, 174050332293622031404857552280219410364023488927386650641)',
            '(602046282375688656758213480587526111916698976636884684818, 174050332293622031404857552280219410364023488927386650641) * 6277101735386680763835789423176059013767194773182842284081':
                'e'
        }
        # pylint: enable=line-too-long

        for instruction in instructions:
            actual = computer.calc(instruction)

            self.assertEqual(str(actual), instructions[instruction])
