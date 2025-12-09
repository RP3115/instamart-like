from typing import Dict, List


class CartItem:
    def __init__(self, product_id: str, quantity: int, unit_price: float, 
                 product_name: str = "", product_image: str = "", weight: str = ""):
        self.product_id = product_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.product_name = product_name
        self.product_image = product_image
        self.weight = weight
    
    def get_item_total(self) -> float:
        return self.quantity * self.unit_price
    
    def update_quantity(self, new_quantity: int):
        self.quantity = new_quantity if new_quantity > 0 else 0
    
    def increment_quantity(self, amount: int = 1):
        self.quantity += amount
    
    def decrement_quantity(self, amount: int = 1):
        self.quantity = max(0, self.quantity - amount)


class Cart:
    def __init__(self, cart_id: str = "", minimum_order_value: float = 0.0, 
                 delivery_charges: float = 0.0):
        self.cart_id = cart_id
        self.items: Dict[str, CartItem] = {}
        self.minimum_order_value = minimum_order_value
        self.delivery_charges = delivery_charges
        self.applied_promo_code: str = ""
        self.discount_amount: float = 0.0
    
    def add_item(self, cart_item: CartItem):
        if cart_item.product_id in self.items:
            self.items[cart_item.product_id].quantity += cart_item.quantity
        else:
            self.items[cart_item.product_id] = cart_item
    
    def remove_item(self, product_id: str):
        if product_id in self.items:
            del self.items[product_id]
    
    def update_item_quantity(self, product_id: str, quantity: int):
        if product_id in self.items:
            if quantity > 0:
                self.items[product_id].update_quantity(quantity)
            else:
                self.remove_item(product_id)
    
    def get_item_count(self) -> int:
        return sum(item.quantity for item in self.items.values())
    
    def get_subtotal(self) -> float:
        return sum(item.get_item_total() for item in self.items.values())
    
    def get_total(self) -> float:
        return self.get_subtotal() + self.delivery_charges - self.discount_amount
    
    def is_minimum_order_met(self) -> bool:
        return self.get_subtotal() >= self.minimum_order_value
    
    def clear(self):
        self.items.clear()
        self.applied_promo_code = ""
        self.discount_amount = 0.0
    
    def get_items_list(self) -> List[CartItem]:
        return list(self.items.values())
