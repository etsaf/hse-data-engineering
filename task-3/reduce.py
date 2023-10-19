#!/usr/bin/env python
"""reduce.py"""

import sys
import math

max_price = -math.inf
for line in sys.stdin:
    price = int(line.strip())
    if price > max_price:
        max_price = price

print(max_price)
