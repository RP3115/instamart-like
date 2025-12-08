"""
PromoCodeFactory - Factory class for creating PromoCode instances
"""

from datetime import datetime
from models.PromoCode import PromoCode


class PromoCodeFactory:
    @staticmethod
    def create_promo_code(code: str, discount_type: str, discount_value: float,
                         min_order_value: float = 0.0, max_discount: float = 0.0,
                         valid_from: datetime = None, valid_until: datetime = None,
                         is_active: bool = True) -> PromoCode:
        """Create a new PromoCode instance"""
        return PromoCode(
            code=code,
            discount_type=discount_type,
            discount_value=discount_value,
            min_order_value=min_order_value,
            max_discount=max_discount,
            valid_from=valid_from,
            valid_until=valid_until,
            is_active=is_active
        )
    
    @staticmethod
    def create_from_dict(data: dict) -> PromoCode:
        """Create PromoCode from dictionary"""
        valid_from = None
        valid_until = None
        
        if data.get("valid_from"):
            valid_from = datetime.fromisoformat(data["valid_from"])
        if data.get("valid_until"):
            valid_until = datetime.fromisoformat(data["valid_until"])
        
        return PromoCode(
            code=data.get("code", ""),
            discount_type=data.get("discount_type", "percentage"),
            discount_value=data.get("discount_value", 0.0),
            min_order_value=data.get("min_order_value", 0.0),
            max_discount=data.get("max_discount", 0.0),
            valid_from=valid_from,
            valid_until=valid_until,
            is_active=data.get("is_active", True)
        )

