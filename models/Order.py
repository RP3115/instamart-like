from typing import List
from datetime import datetime


class OrderItem:
    def __init__(self, order_id: str, product_id: str, quantity: int, unit_price: float,
                 product_name: str = "", product_image: str = "", weight: str = ""):
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.product_name = product_name
        self.product_image = product_image
        self.weight = weight
    
    def get_item_total(self) -> float:
        return self.quantity * self.unit_price


class Order:
    def __init__(self, order_id: str, user_id: str, order_date: datetime = None,
                 status: str = "pending", total_amount: float = 0.0,
                 delivery_address: str = "", payment_method: str = "",
                 order_items: List[OrderItem] = None):
        self.order_id = order_id
        self.user_id = user_id
        self.order_date = order_date or datetime.now()
        self.status = status
        self.total_amount = total_amount
        self.delivery_address = delivery_address
        self.payment_method = payment_method
        self.order_items: List[OrderItem] = order_items or []
        self.subtotal: float = 0.0
        self.delivery_charges: float = 0.0
        self.discount_amount: float = 0.0
        self.applied_promo_code: str = ""
    
    def get_item_count(self) -> int:
        return sum(item.quantity for item in self.order_items)
    
    def get_subtotal(self) -> float:
        return sum(item.get_item_total() for item in self.order_items)
    
    def get_total(self) -> float:
        return self.total_amount
    
    def get_status(self) -> str:
        return self.status
    
    def is_delivered(self) -> bool:
        return self.status == "delivered"
    
    def is_cancelled(self) -> bool:
        return self.status == "cancelled"
    
    def get_ordered_product_ids(self) -> List[str]:
        return [item.product_id for item in self.order_items]
