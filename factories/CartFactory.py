"""
CartFactory - Factory class for creating Cart and CartItem instances
"""

from models.Cart import Cart, CartItem
from models.Product import Product


class CartFactory:
    @staticmethod
    def create_cart(cart_id: str = "", minimum_order_value: float = 0.0,
                   delivery_charges: float = 0.0) -> Cart:
        """Create a new Cart instance"""
        return Cart(
            cart_id=cart_id,
            minimum_order_value=minimum_order_value,
            delivery_charges=delivery_charges
        )
    
    @staticmethod
    def create_cart_item(product_id: str, quantity: int, unit_price: float,
                        product_name: str = "", product_image: str = "",
                        weight: str = "") -> CartItem:
        """Create a new CartItem instance"""
        return CartItem(
            product_id=product_id,
            quantity=quantity,
            unit_price=unit_price,
            product_name=product_name,
            product_image=product_image,
            weight=weight
        )
    
    @staticmethod
    def create_cart_item_from_product(product: Product, quantity: int = 1) -> CartItem:
        """Create CartItem from Product (snapshots current price)"""
        return CartItem(
            product_id=product.product_id,
            quantity=quantity,
            unit_price=product.get_discounted_price(),  # Snapshot the discounted price
            product_name=product.name,
            product_image=product.image,
            weight=product.weight
        )
    
    @staticmethod
    def create_cart_from_dict(data: dict) -> Cart:
        """Create Cart from dictionary"""
        cart = Cart(
            cart_id=data.get("cart_id", ""),
            minimum_order_value=data.get("minimum_order_value", 0.0),
            delivery_charges=data.get("delivery_charges", 0.0)
        )
        
        # Add items if present
        items_data = data.get("items", {})
        for product_id, item_data in items_data.items():
            cart_item = CartFactory.create_cart_item(
                product_id=product_id,
                quantity=item_data.get("quantity", 0),
                unit_price=item_data.get("unit_price", 0.0),
                product_name=item_data.get("product_name", ""),
                product_image=item_data.get("product_image", ""),
                weight=item_data.get("weight", "")
            )
            cart.items[product_id] = cart_item
        
        cart.applied_promo_code = data.get("applied_promo_code", "")
        cart.discount_amount = data.get("discount_amount", 0.0)
        
        return cart

