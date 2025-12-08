"""
UserSettings Entity - Represents user settings and preferences
"""

from typing import List, Optional


class Location:
    """Location Entity - Represents delivery location"""
    
    def __init__(self, location_id: str = "", address: str = "", 
                 city: str = "", state: str = "", pincode: str = "", 
                 latitude: float = 0.0, longitude: float = 0.0, is_default: bool = False):
        self.location_id = location_id
        self.address = address
        self.city = city
        self.state = state
        self.pincode = pincode
        self.latitude = latitude
        self.longitude = longitude
        self.is_default = is_default
    
    def get_full_address(self) -> str:
        """Get complete address string"""
        parts = [self.address, self.city, self.state, self.pincode]
        return ", ".join(filter(None, parts))
    
    def get_short_address(self) -> str:
        """Get short address for display"""
        if self.address:
            return self.address
        return f"{self.city}, {self.state}"


class UserSettings:
    def __init__(self, user_id: str = "", name: str = "", email: str = "", 
                 phone: str = "", payment_method: str = "", locations: List[Location] = None,
                 wishlist: List[str] = None):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.phone = phone
        self.payment_method = payment_method
        self.locations: List[Location] = locations or []
        self.wishlist: List[str] = wishlist or []  # List of product_ids
    
    def update_name(self, name: str):
        """Update user name"""
        self.name = name
    
    def update_email(self, email: str):
        """Update user email"""
        self.email = email
    
    def update_phone(self, phone: str):
        """Update user phone"""
        self.phone = phone
    
    def update_payment_method(self, payment_method: str):
        """Update payment method"""
        self.payment_method = payment_method
    
    def add_location(self, location: Location):
        """Add a new location"""
        # If this is set as default, unset other defaults
        if location.is_default:
            for loc in self.locations:
                loc.is_default = False
        self.locations.append(location)
    
    def remove_location(self, location_id: str) -> bool:
        """Remove a location by ID"""
        for i, loc in enumerate(self.locations):
            if loc.location_id == location_id:
                self.locations.pop(i)
                return True
        return False
    
    def get_default_location(self) -> Optional[Location]:
        """Get the default location"""
        for loc in self.locations:
            if loc.is_default:
                return loc
        return self.locations[0] if self.locations else None
    
    def set_default_location(self, location_id: str) -> bool:
        """Set a location as default"""
        for loc in self.locations:
            if loc.location_id == location_id:
                # Unset other defaults
                for other_loc in self.locations:
                    other_loc.is_default = False
                loc.is_default = True
                return True
        return False
    
    def get_location_by_id(self, location_id: str) -> Optional[Location]:
        """Get location by ID"""
        for loc in self.locations:
            if loc.location_id == location_id:
                return loc
        return None
    
    def add_to_wishlist(self, product_id: str):
        """Add product to wishlist"""
        if product_id not in self.wishlist:
            self.wishlist.append(product_id)
    
    def remove_from_wishlist(self, product_id: str) -> bool:
        """Remove product from wishlist"""
        if product_id in self.wishlist:
            self.wishlist.remove(product_id)
            return True
        return False
    
    def is_in_wishlist(self, product_id: str) -> bool:
        """Check if product is in wishlist"""
        return product_id in self.wishlist
    
    def get_wishlist(self) -> List[str]:
        """Get all wishlist product IDs"""
        return self.wishlist.copy()
    
    def clear_wishlist(self):
        """Clear entire wishlist"""
        self.wishlist.clear()

