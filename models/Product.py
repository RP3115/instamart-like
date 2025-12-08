"""
Product Entity - Represents a product in the store
"""


class Category:
    """Category Entity - Represents a product category"""
    
    def __init__(self, category_id: str, name: str, icon: str = "", image: str = ""):
        self.category_id = category_id
        self.name = name
        self.icon = icon
        self.image = image
    
    def get_display_name(self) -> str:
        """Return the display name of the category"""
        return self.name


class Product:
    def __init__(self, product_id: str, name: str, image: str, category_id: str, 
                 price: float, discount: float, weight: str, description: str = "", 
                 stock: int = 0, max_quantity: int = 10):
        self.product_id = product_id
        self.name = name
        self.image = image
        self.categories = {}
        self.price = price
        self.discount = discount
        self.weight = weight
        self.description = description
        self.stock = stock
        self.max_quantity = max_quantity
    
    def get_discounted_price(self) -> float:
        """Calculate and return the discounted price"""
        if self.discount > 0:
            return self.price * (1 - self.discount / 100)
        return self.price
    
    def get_discount_percentage(self) -> float:
        """Return discount percentage"""
        return self.discount
    
    def is_available(self) -> bool:
        """Check if product is in stock"""
        return self.stock > 0
    
    def is_valid_quantity(self, quantity: int) -> bool:
        """Check if requested quantity is valid"""
        return 0 < quantity <= min(self.stock, self.max_quantity)

