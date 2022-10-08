"""
for adational or externela services
you can create .py files and import it
in any project file `from app.service import [SERVICE NAME]`
"""

from .pprediction import PriceCalculator
from .dprediction import *
from .vin_code import search_with_vin

__all__ = ['PriceCalculator', 'search_with_vin']
