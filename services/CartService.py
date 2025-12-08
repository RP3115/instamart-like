"""
CartService - Business logic for cart operations
"""

from typing import List, Optional
from models.Cart import Cart, CartItem
from models.Product import Product
from models.PromoCode import PromoCode
from factories.CartFactory import CartFactory


class CartService:
    def __init__(self, cart: Cart = None):
        self.cart = cart or CartFactory.create_cart()
    
    def add_product_to_cart(self, product: Product, quantity: int = 1) -> bool:
        """Add a product to cart with validation"""
        if not product.is_available():
            return False
        
        if not product.is_valid_quantity(quantity):
            return False
        
        cart_item = CartFactory.create_cart_item_from_product(product, quantity)
        
        self.cart.add_item(cart_item)
        return True
    
    def remove_product_from_cart(self, product_id: str) -> bool:
        """Remove a product from cart"""
        if product_id in self.cart.items:
            self.cart.remove_item(product_id)
            return True
        return False
    
    def update_product_quantity(self, product_id: str, quantity: int) -> bool:
        """Update quantity of a product in cart"""
        if product_id not in self.cart.items:
            return False
        
        if quantity <= 0:
            self.remove_product_from_cart(product_id)
            return True
        
        # Validate quantity with product constraints if needed
        self.cart.update_item_quantity(product_id, quantity)
        return True
    
    def increment_quantity(self, product_id: str, amount: int = 1) -> bool:
        """Increment quantity of an item in cart"""
        if product_id not in self.cart.items:
            return False
        
        current_item = self.cart.items[product_id]
        new_quantity = current_item.quantity + amount
        return self.update_product_quantity(product_id, new_quantity)
    
    def decrement_quantity(self, product_id: str, amount: int = 1) -> bool:
        """Decrement quantity of an item in cart"""
        if product_id not in self.cart.items:
            return False
        
        current_item = self.cart.items[product_id]
        new_quantity = max(0, current_item.quantity - amount)
        return self.update_product_quantity(product_id, new_quantity)
    
    def apply_promo_code(self, promo_code: PromoCode) -> bool:
        """Apply promo code to cart"""
        subtotal = self.cart.get_subtotal()
        
        if not promo_code.is_valid(subtotal):
            return False
        
        discount = promo_code.calculate_discount(subtotal)
        self.cart.applied_promo_code = promo_code.code
        self.cart.discount_amount = discount
        return True
    
    def remove_promo_code(self):
        """Remove applied promo code"""
        self.cart.applied_promo_code = ""
        self.cart.discount_amount = 0.0
    
    def get_cart_summary(self) -> dict:
        """Get cart summary with all calculations"""
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
        """Clear all items from cart"""
        self.cart.clear()
    
    def get_cart_items(self) -> List[CartItem]:
        """Get list of all cart items"""
        return self.cart.get_items_list()
    
    def is_cart_empty(self) -> bool:
        """Check if cart is empty"""
        return len(self.cart.items) == 0

