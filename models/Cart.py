"""
Cart Entity - Represents the shopping cart
"""

from typing import Dict, List


class CartItem:
    """CartItem Entity - Represents an item in the shopping cart"""
    
    def __init__(self, product_id: str, quantity: int, unit_price: float, 
                 product_name: str = "", product_image: str = "", weight: str = ""):
        self.product_id = product_id
        self.quantity = quantity
        self.unit_price = unit_price  # Snapshot price at time of adding to cart
        self.product_name = product_name
        self.product_image = product_image
        self.weight = weight
    
    def get_item_total(self) -> float:
        """Calculate total price for this cart item"""
        return self.quantity * self.unit_price
    
    def update_quantity(self, new_quantity: int):
        """Update the quantity of the item"""
        if new_quantity > 0:
            self.quantity = new_quantity
        else:
            self.quantity = 0
    
    def increment_quantity(self, amount: int = 1):
        """Increment quantity by given amount"""
        self.quantity += amount
    
    def decrement_quantity(self, amount: int = 1):
        """Decrement quantity by given amount"""
        if self.quantity > amount:
            self.quantity -= amount
        else:
            self.quantity = 0


class Cart:
    def __init__(self, cart_id: str = "", minimum_order_value: float = 0.0, 
                 delivery_charges: float = 0.0):
        self.cart_id = cart_id
        self.items: Dict[str, CartItem] = {}  # product_id -> CartItem
        self.minimum_order_value = minimum_order_value
        self.delivery_charges = delivery_charges
        self.applied_promo_code: str = ""
        self.discount_amount: float = 0.0
    
    def add_item(self, cart_item: CartItem):
        """Add an item to the cart"""
        if cart_item.product_id in self.items:
            # Update quantity if item already exists
            existing_item = self.items[cart_item.product_id]
            existing_item.quantity += cart_item.quantity
        else:
            self.items[cart_item.product_id] = cart_item
    
    def remove_item(self, product_id: str):
        """Remove an item from the cart"""
        if product_id in self.items:
            del self.items[product_id]
    
    def update_item_quantity(self, product_id: str, quantity: int):
        """Update quantity of a specific item"""
        if product_id in self.items:
            if quantity > 0:
                self.items[product_id].update_quantity(quantity)
            else:
                self.remove_item(product_id)
    
    def get_item_count(self) -> int:
        """Get total number of items in cart"""
        return sum(item.quantity for item in self.items.values())
    
    def get_subtotal(self) -> float:
        """Calculate subtotal of all items"""
        return sum(item.get_item_total() for item in self.items.values())
    
    def get_total(self) -> float:
        """Calculate total including delivery charges and discounts"""
        subtotal = self.get_subtotal()
        return subtotal + self.delivery_charges - self.discount_amount
    
    def is_minimum_order_met(self) -> bool:
        """Check if minimum order value is met"""
        return self.get_subtotal() >= self.minimum_order_value
    
    def clear(self):
        """Clear all items from cart"""
        self.items.clear()
        self.applied_promo_code = ""
        self.discount_amount = 0.0
    
    def get_items_list(self) -> List[CartItem]:
        """Get list of all cart items"""
        return list(self.items.values())

