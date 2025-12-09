from typing import List, Optional
from models.Profile import Profile, Location
from models.UserSettings import UserSettings
from models.Cart import Cart, CartItem
from models.Order import Order
from models.Product import Product
from services.CartService import CartService
from services.OrderService import OrderService
from services.ProductService import ProductService


class UserService:
    def __init__(self, user_id: str, profile: Profile = None, user_settings: UserSettings = None,
                 cart_service: CartService = None, order_service: OrderService = None,
                 product_service: ProductService = None):
        self.user_id = user_id
        self.profile = profile or Profile(user_id=user_id)
        self.user_settings = user_settings or UserSettings(user_id=user_id)
        self.cart_service = cart_service or CartService()
        self.order_service = order_service or OrderService()
        self.product_service = product_service or ProductService()
    
    def get_order_history(self, limit: int = None) -> List[Order]:
        orders = self.order_service.get_user_orders(self.user_id)
        return orders[:limit] if limit else orders
    
    def get_recent_orders(self, limit: int = 5) -> List[Order]:
        return self.order_service.get_recent_orders(self.user_id, limit)
    
    def get_order_by_id(self, order_id: str) -> Optional[Order]:
        order = self.order_service.get_order_by_id(order_id)
        return order if order and order.user_id == self.user_id else None
    
    def search_orders(self, query: str) -> List[Order]:
        return self.order_service.search_orders(self.user_id, query)
    
    def get_orders_by_status(self, status: str) -> List[Order]:
        return self.order_service.get_order_by_status(self.user_id, status)
    
    def get_previously_ordered_products(self) -> List[Product]:
        product_ids = self.order_service.get_previously_ordered_products(self.user_id)
        return [p for pid in product_ids if (p := self.product_service.get_product_by_id(pid))]
    
    def get_quick_reorder_items(self) -> List[CartItem]:
        order_items = self.order_service.get_quick_reorder_items(self.user_id)
        cart_items = []
        for order_item in order_items:
            product = self.product_service.get_product_by_id(order_item.product_id)
            if product and product.is_available():
                cart_items.append(CartItem(
                    product_id=product.product_id,
                    quantity=order_item.quantity,
                    unit_price=product.get_discounted_price(),
                    product_name=product.name,
                    product_image=product.image,
                    weight=product.weight
                ))
        return cart_items
    
    def quick_reorder(self) -> bool:
        cart_items = self.get_quick_reorder_items()
        if not cart_items:
            return False
        for cart_item in cart_items:
            product = self.product_service.get_product_by_id(cart_item.product_id)
            if product:
                self.cart_service.add_product_to_cart(product, cart_item.quantity)
        return True
    
    def get_order_stats(self) -> dict:
        return {
            "total_orders": self.order_service.get_total_orders_count(self.user_id),
            "total_spent": self.order_service.get_total_spent(self.user_id),
            "pending_orders": len(self.get_orders_by_status("pending")),
            "delivered_orders": len(self.get_orders_by_status("delivered"))
        }
    
    def get_cart(self) -> Cart:
        return self.cart_service.cart
    
    def get_cart_summary(self) -> dict:
        return self.cart_service.get_cart_summary()
    
    def add_to_cart(self, product: Product, quantity: int = 1) -> bool:
        return self.cart_service.add_product_to_cart(product, quantity)
    
    def remove_from_cart(self, product_id: str) -> bool:
        return self.cart_service.remove_product_from_cart(product_id)
    
    def update_cart_quantity(self, product_id: str, quantity: int) -> bool:
        return self.cart_service.update_product_quantity(product_id, quantity)
    
    def clear_cart(self):
        self.cart_service.clear_cart()
    
    def is_cart_empty(self) -> bool:
        return self.cart_service.is_cart_empty()
    
    def add_to_wishlist(self, product_id: str) -> bool:
        if not self.product_service.get_product_by_id(product_id):
            return False
        self.user_settings.add_to_wishlist(product_id)
        return True
    
    def remove_from_wishlist(self, product_id: str) -> bool:
        return self.user_settings.remove_from_wishlist(product_id)
    
    def get_wishlist_products(self) -> List[Product]:
        return [p for pid in self.user_settings.get_wishlist() 
                if (p := self.product_service.get_product_by_id(pid))]
    
    def is_in_wishlist(self, product_id: str) -> bool:
        return self.user_settings.is_in_wishlist(product_id)
    
    def move_wishlist_to_cart(self, product_id: str) -> bool:
        if not self.is_in_wishlist(product_id):
            return False
        product = self.product_service.get_product_by_id(product_id)
        if not product or not self.add_to_cart(product):
            return False
        self.remove_from_wishlist(product_id)
        return True
    
    def clear_wishlist(self):
        self.user_settings.clear_wishlist()
    
    def get_profile(self) -> Profile:
        return self.profile
    
    def get_user_settings(self) -> UserSettings:
        return self.user_settings
    
    def update_name(self, name: str):
        self.profile.update_name(name)
    
    def update_email(self, email: str):
        self.profile.update_email(email)
    
    def update_phone(self, phone: str):
        self.profile.update_phone(phone)
    
    def update_payment_method(self, payment_method: str):
        self.profile.update_payment_method(payment_method)
    
    def add_location(self, location: Location):
        self.user_settings.add_location(location)
    
    def remove_location(self, location_id: str) -> bool:
        return self.user_settings.remove_location(location_id)
    
    def set_default_location(self, location_id: str) -> bool:
        return self.user_settings.set_default_location(location_id)
    
    def get_default_location(self) -> Optional[Location]:
        return self.user_settings.get_default_location()
