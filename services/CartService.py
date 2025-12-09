from typing import List
from models.Cart import Cart, CartItem
from models.Product import Product
from models.PromoCode import PromoCode
from factories.CartFactory import CartFactory


class CartService:
    def __init__(self, cart: Cart = None):
        self.cart = cart or CartFactory.create_cart()
    
    def add_product_to_cart(self, product: Product, quantity: int = 1) -> bool:
        if not product.is_available() or not product.is_valid_quantity(quantity):
            return False
        
        cart_item = CartFactory.create_cart_item_from_product(product, quantity)
        self.cart.add_item(cart_item)
        return True
    
    def remove_product_from_cart(self, product_id: str) -> bool:
        if product_id in self.cart.items:
            self.cart.remove_item(product_id)
            return True
        return False
    
    def update_product_quantity(self, product_id: str, quantity: int) -> bool:
        if product_id not in self.cart.items:
            return False
        
        if quantity <= 0:
            self.remove_product_from_cart(product_id)
            return True
        
        self.cart.update_item_quantity(product_id, quantity)
        return True
    
    def increment_quantity(self, product_id: str, amount: int = 1) -> bool:
        if product_id not in self.cart.items:
            return False
        current_item = self.cart.items[product_id]
        return self.update_product_quantity(product_id, current_item.quantity + amount)
    
    def decrement_quantity(self, product_id: str, amount: int = 1) -> bool:
        if product_id not in self.cart.items:
            return False
        current_item = self.cart.items[product_id]
        return self.update_product_quantity(product_id, max(0, current_item.quantity - amount))
    
    def apply_promo_code(self, promo_code: PromoCode) -> bool:
        subtotal = self.cart.get_subtotal()
        if not promo_code.is_valid(subtotal):
            return False
        
        discount = promo_code.calculate_discount(subtotal)
        self.cart.applied_promo_code = promo_code.code
        self.cart.discount_amount = discount
        return True
    
    def remove_promo_code(self):
        self.cart.applied_promo_code = ""
        self.cart.discount_amount = 0.0
    
    def get_cart_summary(self) -> dict:
        return {
            "item_count": self.cart.get_item_count(),
            "subtotal": self.cart.get_subtotal(),
            "delivery_charges": self.cart.delivery_charges,
            "discount": self.cart.discount_amount,
            "total": self.cart.get_total(),
            "minimum_order_met": self.cart.is_minimum_order_met(),
            "minimum_order_value": self.cart.minimum_order_value
        }
    
    def clear_cart(self):
        self.cart.clear()
    
    def get_cart_items(self) -> List[CartItem]:
        return self.cart.get_items_list()
    
    def is_cart_empty(self) -> bool:
        return len(self.cart.items) == 0
