"""
UserService - Business logic for user operations (order history, cart, wishlist)
"""

from typing import List, Optional
from models.UserSettings import UserSettings, Location
from models.Cart import Cart, CartItem
from models.Order import Order
from models.Product import Product
from services.CartService import CartService
from services.OrderService import OrderService
from services.ProductService import ProductService


class UserService:
    def __init__(self, user_id: str, user_settings: UserSettings = None,
                 cart_service: CartService = None, order_service: OrderService = None,
                 product_service: ProductService = None):
        self.user_id = user_id
        self.user_settings = user_settings or UserSettings(user_id=user_id)
        self.cart_service = cart_service or CartService()
        self.order_service = order_service or OrderService()
        self.product_service = product_service or ProductService()
    
    # ==================== ORDER HISTORY ====================
    
    def get_order_history(self, limit: int = None) -> List[Order]:
        """Get user's order history"""
        orders = self.order_service.get_user_orders(self.user_id)
        if limit:
            return orders[:limit]
        return orders
    
    def get_recent_orders(self, limit: int = 5) -> List[Order]:
        """Get recent orders"""
        return self.order_service.get_recent_orders(self.user_id, limit)
    
    def get_order_by_id(self, order_id: str) -> Optional[Order]:
        """Get specific order by ID"""
        order = self.order_service.get_order_by_id(order_id)
        # Verify it belongs to this user
        if order and order.user_id == self.user_id:
            return order
        return None
    
    def search_orders(self, query: str) -> List[Order]:
        """Search user's orders"""
        return self.order_service.search_orders(self.user_id, query)
    
    def get_orders_by_status(self, status: str) -> List[Order]:
        """Get orders by status"""
        return self.order_service.get_order_by_status(self.user_id, status)
    
    def get_previously_ordered_products(self) -> List[Product]:
        """Get previously ordered products as Product objects"""
        product_ids = self.order_service.get_previously_ordered_products(self.user_id)
        products = []
        for product_id in product_ids:
            product = self.product_service.get_product_by_id(product_id)
            if product:
                products.append(product)
        return products
    
    def get_quick_reorder_items(self) -> List[CartItem]:
        """Get items from most recent order for quick reorder"""
        order_items = self.order_service.get_quick_reorder_items(self.user_id)
        # Convert OrderItems to CartItems (for adding to cart)
        cart_items = []
        for order_item in order_items:
            product = self.product_service.get_product_by_id(order_item.product_id)
            if product and product.is_available():
                # Use current product price, not order price
                cart_item = CartItem(
                    product_id=product.product_id,
                    quantity=order_item.quantity,
                    unit_price=product.get_discounted_price(),
                    product_name=product.name,
                    product_image=product.image,
                    weight=product.weight
                )
                cart_items.append(cart_item)
        return cart_items
    
    def quick_reorder(self) -> bool:
        """Add items from last order to cart"""
        cart_items = self.get_quick_reorder_items()
        if not cart_items:
            return False
        
        for cart_item in cart_items:
            product = self.product_service.get_product_by_id(cart_item.product_id)
            if product:
                self.cart_service.add_product_to_cart(product, cart_item.quantity)
        return True
    
    def get_order_stats(self) -> dict:
        """Get order statistics for user"""
        return {
            "total_orders": self.order_service.get_total_orders_count(self.user_id),
            "total_spent": self.order_service.get_total_spent(self.user_id),
            "pending_orders": len(self.get_orders_by_status("pending")),
            "delivered_orders": len(self.get_orders_by_status("delivered"))
        }
    
    # ==================== CART OPERATIONS ====================
    
    def get_cart(self) -> Cart:
        """Get user's current cart"""
        return self.cart_service.cart
    
    def get_cart_summary(self) -> dict:
        """Get cart summary"""
        return self.cart_service.get_cart_summary()
    
    def add_to_cart(self, product: Product, quantity: int = 1) -> bool:
        """Add product to cart"""
        return self.cart_service.add_product_to_cart(product, quantity)
    
    def remove_from_cart(self, product_id: str) -> bool:
        """Remove product from cart"""
        return self.cart_service.remove_product_from_cart(product_id)
    
    def update_cart_quantity(self, product_id: str, quantity: int) -> bool:
        """Update product quantity in cart"""
        return self.cart_service.update_product_quantity(product_id, quantity)
    
    def clear_cart(self):
        """Clear cart"""
        self.cart_service.clear_cart()
    
    def is_cart_empty(self) -> bool:
        """Check if cart is empty"""
        return self.cart_service.is_cart_empty()
    
    # ==================== WISHLIST OPERATIONS ====================
    
    def add_to_wishlist(self, product_id: str) -> bool:
        """Add product to wishlist"""
        product = self.product_service.get_product_by_id(product_id)
        if not product:
            return False
        self.user_settings.add_to_wishlist(product_id)
        return True
    
    def remove_from_wishlist(self, product_id: str) -> bool:
        """Remove product from wishlist"""
        return self.user_settings.remove_from_wishlist(product_id)
    
    def get_wishlist_products(self) -> List[Product]:
        """Get wishlist as Product objects"""
        product_ids = self.user_settings.get_wishlist()
        products = []
        for product_id in product_ids:
            product = self.product_service.get_product_by_id(product_id)
            if product:
                products.append(product)
        return products
    
    def is_in_wishlist(self, product_id: str) -> bool:
        """Check if product is in wishlist"""
        return self.user_settings.is_in_wishlist(product_id)
    
    def move_wishlist_to_cart(self, product_id: str) -> bool:
        """Move product from wishlist to cart"""
        if not self.is_in_wishlist(product_id):
            return False
        
        product = self.product_service.get_product_by_id(product_id)
        if not product:
            return False
        
        if self.add_to_cart(product):
            self.remove_from_wishlist(product_id)
            return True
        return False
    
    def clear_wishlist(self):
        """Clear wishlist"""
        self.user_settings.clear_wishlist()
    
    # ==================== USER SETTINGS OPERATIONS ====================
    
    def get_user_settings(self) -> UserSettings:
        """Get user settings"""
        return self.user_settings
    
    def update_name(self, name: str):
        """Update user name"""
        self.user_settings.update_name(name)
    
    def update_email(self, email: str):
        """Update user email"""
        self.user_settings.update_email(email)
    
    def update_phone(self, phone: str):
        """Update user phone"""
        self.user_settings.update_phone(phone)
    
    def add_location(self, location: Location):
        """Add location"""
        self.user_settings.add_location(location)
    
    def remove_location(self, location_id: str) -> bool:
        """Remove location"""
        return self.user_settings.remove_location(location_id)
    
    def set_default_location(self, location_id: str) -> bool:
        """Set default location"""
        return self.user_settings.set_default_location(location_id)
    
    def get_default_location(self) -> Optional[Location]:
        """Get default location"""
        return self.user_settings.get_default_location()

