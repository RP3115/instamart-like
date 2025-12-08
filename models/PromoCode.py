"""
PromoCode Entity - Represents a promotional code or coupon
"""

from datetime import datetime


class PromoCode:
    def __init__(self, code: str, discount_type: str, discount_value: float,
                 min_order_value: float = 0.0, max_discount: float = 0.0,
                 valid_from: datetime = None, valid_until: datetime = None,
                 is_active: bool = True):
        self.code = code
        self.discount_type = discount_type  # "percentage" or "fixed"
        self.discount_value = discount_value
        self.min_order_value = min_order_value
        self.max_discount = max_discount
        self.valid_from = valid_from
        self.valid_until = valid_until
        self.is_active = is_active
    
    def is_valid(self, order_value: float, current_date: datetime = None) -> bool:
        """Check if promo code is valid for the given order value"""
        if not self.is_active:
            return False
        
        if current_date is None:
            current_date = datetime.now()
        
        if self.valid_from and current_date < self.valid_from:
            return False
        
        if self.valid_until and current_date > self.valid_until:
            return False
        
        if order_value < self.min_order_value:
            return False
        
        return True
    
    def calculate_discount(self, order_value: float) -> float:
        """Calculate discount amount for given order value"""
        if not self.is_valid(order_value):
            return 0.0
        
        if self.discount_type == "percentage":
            discount = order_value * (self.discount_value / 100)
            if self.max_discount > 0:
                discount = min(discount, self.max_discount)
            return discount
        elif self.discount_type == "fixed":
            return min(self.discount_value, order_value)
        
        return 0.0

