"""
ProductService - Business logic for product operations
"""

from typing import List, Optional
from models.Product import Product, Category


class ProductService:
    def __init__(self, products: List[Product] = None, categories: List[Category] = None):
        self.products = products or []
        self.categories = categories or []
        self._product_map = {p.product_id: p for p in self.products}
        self._category_map = {c.category_id: c for c in self.categories}
    
    def get_all_products(self) -> List[Product]:
        """Get all products"""
        return self.products
    
    def get_product_by_id(self, product_id: str) -> Optional[Product]:
        """Get product by ID"""
        return self._product_map.get(product_id)
    
    def get_products_by_category(self, category_id: str) -> List[Product]:
        """Get products filtered by category"""
        return [p for p in self.products if p.category_id == category_id]
    
    def search_products(self, query: str) -> List[Product]:
        """Search products by name or description"""
        query_lower = query.lower()
        return [
            p for p in self.products
            if query_lower in p.name.lower() or query_lower in p.description.lower()
        ]
    
    def filter_available_products(self, products: List[Product] = None) -> List[Product]:
        """Filter only available products"""
        product_list = products or self.products
        return [p for p in product_list if p.is_available()]
    
    def sort_products_by_price(self, products: List[Product], ascending: bool = True) -> List[Product]:
        """Sort products by price"""
        return sorted(products, key=lambda p: p.get_discounted_price(), reverse=not ascending)
    
    def sort_products_by_discount(self, products: List[Product], descending: bool = True) -> List[Product]:
        """Sort products by discount percentage"""
        return sorted(products, key=lambda p: p.get_discount_percentage(), reverse=descending)
    
    def get_all_categories(self) -> List[Category]:
        """Get all categories"""
        return self.categories
    
    def get_category_by_id(self, category_id: str) -> Optional[Category]:
        """Get category by ID"""
        return self._category_map.get(category_id)
    
    def add_product(self, product: Product):
        """Add a product to the service"""
        if product.product_id not in self._product_map:
            self.products.append(product)
            self._product_map[product.product_id] = product
    
    def add_category(self, category: Category):
        """Add a category to the service"""
        if category.category_id not in self._category_map:
            self.categories.append(category)
            self._category_map[category.category_id] = category

