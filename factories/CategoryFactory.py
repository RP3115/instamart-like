"""
CategoryFactory - Factory class for creating Category instances
"""

from models.Product import Category


class CategoryFactory:
    @staticmethod
    def create_category(category_id: str, name: str, icon: str = "", 
                      image: str = "") -> Category:
        """Create a new Category instance"""
        return Category(
            category_id=category_id,
            name=name,
            icon=icon,
            image=image
        )
    
    @staticmethod
    def create_from_dict(data: dict) -> Category:
        """Create Category from dictionary"""
        return Category(
            category_id=data.get("category_id", ""),
            name=data.get("name", ""),
            icon=data.get("icon", ""),
            image=data.get("image", "")
        )

