"""
ProductFactory - Factory class for creating Product instances
"""

from models.Product import Product


class ProductFactory:
    @staticmethod
    def create_product(product_id: str, name: str, image: str, category_id: str,
                      price: float, discount: float = 0.0, weight: str = "",
                      description: str = "", stock: int = 0, max_quantity: int = 10) -> Product:
        """Create a new Product instance"""
        return Product(
            product_id=product_id,
            name=name,
            image=image,
            category_id=category_id,
            price=price,
            discount=discount,
            weight=weight,
            description=description,
            stock=stock,
            max_quantity=max_quantity
        )
    
    @staticmethod
    def create_from_dict(data: dict) -> Product:
        """Create Product from dictionary"""
        return Product(
            product_id=data.get("product_id", ""),
            name=data.get("name", ""),
            image=data.get("image", ""),
            category_id=data.get("category_id", ""),
            price=data.get("price", 0.0),
            discount=data.get("discount", 0.0),
            weight=data.get("weight", ""),
            description=data.get("description", ""),
            stock=data.get("stock", 0),
            max_quantity=data.get("max_quantity", 10)
        )

