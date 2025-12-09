from datetime import datetime
from models.Order import Order, OrderItem
from models.Cart import Cart, CartItem


class OrderFactory:
    @staticmethod
    def create_order(order_id: str, user_id: str, order_date: datetime = None,
                    status: str = "pending", total_amount: float = 0.0,
                    delivery_address: str = "", payment_method: str = "",
                    order_items: list = None) -> Order:
        return Order(
            order_id=order_id,
            user_id=user_id,
            order_date=order_date,
            status=status,
            total_amount=total_amount,
            delivery_address=delivery_address,
            payment_method=payment_method,
            order_items=order_items or []
        )
    
    @staticmethod
    def create_order_item_from_cart_item(cart_item: CartItem, order_id: str) -> OrderItem:
        return OrderItem(
            order_id=order_id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            unit_price=cart_item.unit_price,
            product_name=cart_item.product_name,
            product_image=cart_item.product_image,
            weight=cart_item.weight
        )
    
    @staticmethod
    def create_order_from_cart(cart: Cart, user_id: str, order_id: str,
                               delivery_address: str, payment_method: str = "",
                               status: str = "pending") -> Order:
        order_items = [
            OrderFactory.create_order_item_from_cart_item(cart_item, order_id)
            for cart_item in cart.get_items_list()
        ]
        
        subtotal = cart.get_subtotal()
        total_amount = cart.get_total()
        
        order = Order(
            order_id=order_id,
            user_id=user_id,
            order_date=datetime.now(),
            status=status,
            total_amount=total_amount,
            delivery_address=delivery_address,
            payment_method=payment_method,
            order_items=order_items
        )
        
        order.subtotal = subtotal
        order.delivery_charges = cart.delivery_charges
        order.discount_amount = cart.discount_amount
        order.applied_promo_code = cart.applied_promo_code
        
        return order
    
    @staticmethod
    def create_from_dict(data: dict) -> Order:
        order_date = None
        if data.get("order_date"):
            order_date = datetime.fromisoformat(data["order_date"]) if isinstance(data["order_date"], str) else data["order_date"]
        
        order_items = [
            OrderItem(
                order_id=data.get("order_id", ""),
                product_id=item_data.get("product_id", ""),
                quantity=item_data.get("quantity", 0),
                unit_price=item_data.get("unit_price", 0.0),
                product_name=item_data.get("product_name", ""),
                product_image=item_data.get("product_image", ""),
                weight=item_data.get("weight", "")
            )
            for item_data in data.get("order_items", [])
        ]
        
        order = Order(
            order_id=data.get("order_id", ""),
            user_id=data.get("user_id", ""),
            order_date=order_date,
            status=data.get("status", "pending"),
            total_amount=data.get("total_amount", 0.0),
            delivery_address=data.get("delivery_address", ""),
            payment_method=data.get("payment_method", ""),
            order_items=order_items
        )
        
        order.subtotal = data.get("subtotal", 0.0)
        order.delivery_charges = data.get("delivery_charges", 0.0)
        order.discount_amount = data.get("discount_amount", 0.0)
        order.applied_promo_code = data.get("applied_promo_code", "")
        
        return order
