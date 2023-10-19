#!/usr/bin/env python
"""map.py"""
import sys

delimiter = ','
for line in sys.stdin:
    arr = line.split(delimiter)
    price = arr[1]
    print(price)
