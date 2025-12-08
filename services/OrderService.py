"""
OrderService - Business logic for order operations
"""

from typing import List, Optional
from datetime import datetime
from models.Order import Order, OrderItem
from models.Product import Product
from factories.OrderFactory import OrderFactory


class OrderService:
    def __init__(self, orders: List[Order] = None):
        self.orders = orders or []
        self._order_map = {o.order_id: o for o in self.orders}
        # Index: user_id -> List[Order]
        self._user_orders: dict = {}
        self._build_user_index()
    
    def _build_user_index(self):
        """Build index: user_id -> List[Order]"""
        self._user_orders.clear()
        for order in self.orders:
            if order.user_id not in self._user_orders:
                self._user_orders[order.user_id] = []
            self._user_orders[order.user_id].append(order)
    
    def create_order(self, order: Order):
        """Add a new order"""
        if order.order_id not in self._order_map:
            self.orders.append(order)
            self._order_map[order.order_id] = order
            
            # Update user index
            if order.user_id not in self._user_orders:
                self._user_orders[order.user_id] = []
            self._user_orders[order.user_id].append(order)
    
    def get_order_by_id(self, order_id: str) -> Optional[Order]:
        """Get order by ID"""
        return self._order_map.get(order_id)
    
    def get_user_orders(self, user_id: str) -> List[Order]:
        """Get all orders for a user (sorted by date, newest first)"""
        user_orders = self._user_orders.get(user_id, [])
        return sorted(user_orders, key=lambda o: o.order_date, reverse=True)
    
    def get_recent_orders(self, user_id: str, limit: int = 5) -> List[Order]:
        """Get recent orders for a user"""
        all_orders = self.get_user_orders(user_id)
        return all_orders[:limit]
    
    def get_order_by_status(self, user_id: str, status: str) -> List[Order]:
        """Get orders by status for a user"""
        user_orders = self.get_user_orders(user_id)
        return [o for o in user_orders if o.status == status]
    
    def search_orders(self, user_id: str, query: str) -> List[Order]:
        """Search orders by product name or order ID"""
        user_orders = self.get_user_orders(user_id)
        query_lower = query.lower()
        results = []
        
        for order in user_orders:
            # Search by order ID
            if query_lower in order.order_id.lower():
                results.append(order)
                continue
            
            # Search by product names in order
            for item in order.order_items:
                if query_lower in item.product_name.lower():
                    results.append(order)
                    break
        
        return results
    
    def get_previously_ordered_products(self, user_id: str) -> List[str]:
        """Get unique product IDs from all user orders"""
        user_orders = self.get_user_orders(user_id)
        product_ids = set()
        
        for order in user_orders:
            product_ids.update(order.get_ordered_product_ids())
        
        return list(product_ids)
    
    def get_quick_reorder_items(self, user_id: str) -> List[OrderItem]:
        """Get items from most recent order for quick reorder"""
        recent_orders = self.get_recent_orders(user_id, limit=1)
        if recent_orders:
            return recent_orders[0].order_items
        return []
    
    def get_orders_by_date_range(self, user_id: str, start_date: datetime, 
                                 end_date: datetime) -> List[Order]:
        """Get orders within a date range"""
        user_orders = self.get_user_orders(user_id)
        return [
            o for o in user_orders
            if start_date <= o.order_date <= end_date
        ]
    
    def get_total_orders_count(self, user_id: str) -> int:
        """Get total number of orders for a user"""
        return len(self._user_orders.get(user_id, []))
