#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Elliptic curve points module."""
from lib.points.point import Point
from lib.points.prime_point import PrimePoint
from lib.points.binary_points import Point2N, Point2S


POINTS = {
    'n': Point2N,
    's': Point2S,
    'p': PrimePoint
}


def points_factory(curve_type, params):
    """Point factory."""
    return POINTS[curve_type](params)
