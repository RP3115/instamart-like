"""
Banner Entity - Represents promotional banners/offers
"""


class Banner:
    def __init__(self, banner_id: str, image_url: str, title: str = "", 
                 description: str = "", link_url: str = "", is_active: bool = True):
        self.banner_id = banner_id
        self.image_url = image_url
        self.title = title
        self.description = description
        self.link_url = link_url
        self.is_active = is_active
    
    def is_valid(self) -> bool:
        """Check if banner is active"""
        return self.is_active

