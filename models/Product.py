from typing import List


class Category:
    def __init__(self, category_id: str, name: str, icon: str = "", image: str = ""):
        self.category_id = category_id
        self.name = name
        self.icon = icon
        self.image = image
    
    def get_display_name(self) -> str:
        return self.name


class Product:
    def __init__(self, product_id: str, name: str, image: str, category_id: str, 
                 price: float, discount: float, weight: str, description: str = "", 
                 stock: int = 0, max_quantity: int = 10, images: List[str] = []):
        self.product_id = product_id
        self.name = name
        self.image = image
        self.categories = {}  # Add category : sub category mapping or something better ? 
        self.price = price
        self.discount = discount
        self.weight = weight
        self.description = description
        self.stock = stock
        self.max_quantity = max_quantity
        self.images = images
    
    def get_discounted_price(self) -> float:
        if self.discount > 0:
            return self.price * (1 - self.discount / 100)
        return self.price
    
    def get_discount_percentage(self) -> float:
        return self.discount
    
    def is_available(self) -> bool:
        return self.stock > 0
    
    def is_valid_quantity(self, quantity: int) -> bool:
        return 0 < quantity <= min(self.stock, self.max_quantity)
