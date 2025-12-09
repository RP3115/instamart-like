from typing import List, Optional, Dict
from models.Banner import Banner
from models.Product import Product, Category
from models.Cart import CartItem
from services.ProductService import ProductService
from services.CartService import CartService
from services.UserService import UserService

# Basic Home Page render which combines logics
class HomePageService:
    def __init__(self, product_service: ProductService = None, 
                 cart_service: CartService = None,
                 user_service: UserService = None,
                 banners: List[Banner] = None):
        self.product_service = product_service or ProductService()
        self.cart_service = cart_service or CartService()
        self.user_service = user_service
        self.banners = banners or []
    
    def get_active_banners(self) -> List[Banner]:
        return [b for b in self.banners if b.is_valid()]
    
    def get_categories(self) -> List[Category]:
        return self.product_service.get_all_categories()
    
    def get_deals_products(self, limit: int = 20) -> List[Product]:
        all_products = self.product_service.get_all_products()
        deals = [p for p in all_products if p.get_discount_percentage() > 0]
        sorted_deals = self.product_service.sort_products_by_discount(deals, descending=True)
        return sorted_deals[:limit]
    
    def get_featured_products(self, limit: int = 20) -> List[Product]:
        all_products = self.product_service.filter_available_products()
        return all_products[:limit]
    
    def get_top_deals(self, limit: int = 10) -> List[Product]:
        deals = self.get_deals_products(limit * 2)
        return deals[:limit]
    
    def get_products_by_category(self, category_id: str, limit: int = None) -> List[Product]:
        products = self.product_service.get_products_by_category(category_id)
        available = self.product_service.filter_available_products(products)
        return available[:limit] if limit else available
    
    def search_products(self, query: str, limit: int = None) -> List[Product]:
        results = self.product_service.search_products(query)
        available = self.product_service.filter_available_products(results)
        return available[:limit] if limit else available
    
    def get_recently_viewed_products(self, limit: int = 10) -> List[Product]:
        if not self.user_service: # No login case
            return [] 
        return self.user_service.get_previously_ordered_products()[:limit]
    
    def get_quick_reorder_section(self) -> List[CartItem]:
        if not self.user_service:
            return []
        return self.user_service.get_quick_reorder_items()
    
    def add_product_to_cart(self, product_id: str, quantity: int = 1) -> bool:
        product = self.product_service.get_product_by_id(product_id)
        if not product:
            return False
        return self.cart_service.add_product_to_cart(product, quantity)
    
    def get_cart_item_count(self) -> int:
        return self.cart_service.cart.get_item_count()
    
    def get_homepage_data(self, user_id: str = None) -> Dict:
        data = {
            "banners": self.get_active_banners(),
            "categories": self.get_categories(),
            "top_deals": self.get_top_deals(10),
            "deals_products": self.get_deals_products(20),
            "featured_products": self.get_featured_products(20),
            "cart_item_count": self.get_cart_item_count()
        }
        
        if self.user_service:
            data["quick_reorder"] = self.get_quick_reorder_section()
            data["recently_viewed"] = self.get_recently_viewed_products(10)
        
        return data
    
    def filter_and_sort_products(self, category_id: str = None, 
                                 search_query: str = None,
                                 sort_by: str = "default",
                                 ascending: bool = True,
                                 limit: int = None) -> List[Product]:
        if search_query:
            products = self.product_service.search_products(search_query)
        elif category_id:
            products = self.product_service.get_products_by_category(category_id)
        else:
            products = self.product_service.get_all_products()
        
        products = self.product_service.filter_available_products(products)
        
        if sort_by == "price":
            products = self.product_service.sort_products_by_price(products, ascending)
        elif sort_by == "discount":
            products = self.product_service.sort_products_by_discount(products, descending=not ascending)
        
        return products[:limit] if limit else products
    
    def get_product_with_cart_info(self, product_id: str) -> Optional[Dict]:
        product = self.product_service.get_product_by_id(product_id)
        if not product:
            return None
        
        cart_item = self.cart_service.cart.items.get(product_id)
        in_cart = cart_item is not None
        cart_quantity = cart_item.quantity if cart_item else 0
        
        return {
            "product": product,
            "in_cart": in_cart,
            "cart_quantity": cart_quantity,
            "is_available": product.is_available()
        }

