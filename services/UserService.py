from typing import List, Optional
from models.Profile import Profile, Location
from models.UserSettings import UserSettings
from models.Cart import CartItem
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
        pending = self.order_service.get_order_by_status(self.user_id, "pending")
        delivered = self.order_service.get_order_by_status(self.user_id, "delivered")
        return {
            "total_orders": self.order_service.get_total_orders_count(self.user_id),
            "total_spent": self.order_service.get_total_spent(self.user_id),
            "pending_orders": len(pending),
            "delivered_orders": len(delivered)
        }
    
    def add_to_wishlist(self, product_id: str) -> bool:
        if not self.product_service.get_product_by_id(product_id):
            return False
        self.user_settings.add_to_wishlist(product_id)
        return True
    
    def get_wishlist_products(self) -> List[Product]:
        return [p for pid in self.user_settings.get_wishlist() 
                if (p := self.product_service.get_product_by_id(pid))]
    
    def move_wishlist_to_cart(self, product_id: str) -> bool:
        if not self.user_settings.is_in_wishlist(product_id):
            return False
        product = self.product_service.get_product_by_id(product_id)
        if not product or not self.cart_service.add_product_to_cart(product):
            return False
        self.user_settings.remove_from_wishlist(product_id)
        return True
