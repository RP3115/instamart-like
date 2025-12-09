from models.Product import Category


class CategoryFactory:
    @staticmethod
    def create_category(category_id: str, name: str, icon: str = "", 
                      image: str = "") -> Category:
        return Category(
            category_id=category_id,
            name=name,
            icon=icon,
            image=image
        )
    
    @staticmethod
    def create_from_dict(data: dict) -> Category:
        return Category(
            category_id=data.get("category_id", ""),
            name=data.get("name", ""),
            icon=data.get("icon", ""),
            image=data.get("image", "")
        )
