"""
PromoCodeService - Business logic for promo code operations
"""

from typing import List, Optional, Tuple
from models.PromoCode import PromoCode
from datetime import datetime


class PromoCodeService:
    def __init__(self, promo_codes: List[PromoCode] = None):
        self.promo_codes = promo_codes or []
        self._code_map = {pc.code.upper(): pc for pc in self.promo_codes}
    
    def get_promo_code_by_code(self, code: str) -> Optional[PromoCode]:
        """Get promo code by code string"""
        return self._code_map.get(code.upper())
    
    def validate_promo_code(self, code: str, order_value: float, 
                           current_date: datetime = None) -> Tuple[bool, Optional[PromoCode]]:
        """Validate promo code and return (is_valid, promo_code)"""
        promo_code = self.get_promo_code_by_code(code)
        
        if promo_code is None:
            return False, None
        
        if current_date is None:
            current_date = datetime.now()
        
        is_valid = promo_code.is_valid(order_value, current_date)
        return is_valid, promo_code if is_valid else None
    
    def get_all_active_promo_codes(self, current_date: datetime = None) -> List[PromoCode]:
        """Get all active promo codes"""
        if current_date is None:
            current_date = datetime.now()
        
        return [pc for pc in self.promo_codes if pc.is_active and pc.is_valid(0.0, current_date)]
    
    def add_promo_code(self, promo_code: PromoCode):
        """Add a promo code to the service"""
        if promo_code.code.upper() not in self._code_map:
            self.promo_codes.append(promo_code)
            self._code_map[promo_code.code.upper()] = promo_code

