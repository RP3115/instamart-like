from typing import List, Optional
from models.Profile import Location


class UserSettings:
    def __init__(self, user_id: str = "", locations: List[Location] = None,
                 wishlist: List[str] = None):
        self.user_id = user_id
        self.locations: List[Location] = locations or []
        self.wishlist: List[str] = wishlist or []
    
    def add_location(self, location: Location):
        if location.is_default:
            for loc in self.locations:
                loc.is_default = False
        self.locations.append(location)
    
    def remove_location(self, location_id: str) -> bool:
        for i, loc in enumerate(self.locations):
            if loc.location_id == location_id:
                self.locations.pop(i)
                return True
        return False
    
    def get_default_location(self) -> Optional[Location]:
        for loc in self.locations:
            if loc.is_default:
                return loc
        return self.locations[0] if self.locations else None
    
    def set_default_location(self, location_id: str) -> bool:
        for loc in self.locations:
            if loc.location_id == location_id:
                for other_loc in self.locations:
                    other_loc.is_default = False
                loc.is_default = True
                return True
        return False
    
    def get_location_by_id(self, location_id: str) -> Optional[Location]:
        for loc in self.locations:
            if loc.location_id == location_id:
                return loc
        return None
    
    def add_to_wishlist(self, product_id: str):
        if product_id not in self.wishlist:
            self.wishlist.append(product_id)
    
    def remove_from_wishlist(self, product_id: str) -> bool:
        if product_id in self.wishlist:
            self.wishlist.remove(product_id)
            return True
        return False
    
    def is_in_wishlist(self, product_id: str) -> bool:
        return product_id in self.wishlist
    
    def get_wishlist(self) -> List[str]:
        return self.wishlist.copy()
    
    def clear_wishlist(self):
        self.wishlist.clear()
