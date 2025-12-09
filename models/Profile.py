from typing import List, Optional


class Location:
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
        parts = [self.address, self.city, self.state, self.pincode]
        return ", ".join(filter(None, parts))
    
    def get_short_address(self) -> str:
        if self.address:
            return self.address
        return f"{self.city}, {self.state}"


class Profile:
    def __init__(self, user_id: str = "", name: str = "", email: str = "", 
                 phone: str = "", payment_method: str = ""):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.phone = phone
        self.payment_method = payment_method
    
    def update_name(self, name: str):
        self.name = name
    
    def update_email(self, email: str):
        self.email = email
    
    def update_phone(self, phone: str):
        self.phone = phone
    
    def update_payment_method(self, payment_method: str):
        self.payment_method = payment_method

