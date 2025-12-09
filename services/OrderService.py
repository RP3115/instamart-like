from typing import List, Optional
from datetime import datetime
from models.Order import Order, OrderItem


class OrderService:
    def __init__(self, orders: List[Order] = None):
        self.orders = orders or []
        self._order_map = {o.order_id: o for o in self.orders}
        self._user_orders: dict = {}
        self._build_user_index()
    
    def _build_user_index(self):
        self._user_orders.clear()
        for order in self.orders:
            if order.user_id not in self._user_orders:
                self._user_orders[order.user_id] = []
            self._user_orders[order.user_id].append(order)
    
    def create_order(self, order: Order):
        if order.order_id not in self._order_map:
            self.orders.append(order)
            self._order_map[order.order_id] = order
            if order.user_id not in self._user_orders:
                self._user_orders[order.user_id] = []
            self._user_orders[order.user_id].append(order)
    
    def get_order_by_id(self, order_id: str) -> Optional[Order]:
        return self._order_map.get(order_id)
    
    def get_user_orders(self, user_id: str) -> List[Order]:
        user_orders = self._user_orders.get(user_id, [])
        return sorted(user_orders, key=lambda o: o.order_date, reverse=True)
    
    def get_recent_orders(self, user_id: str, limit: int = 5) -> List[Order]:
        return self.get_user_orders(user_id)[:limit]
    
    def get_order_by_status(self, user_id: str, status: str) -> List[Order]:
        return [o for o in self.get_user_orders(user_id) if o.status == status]
    
    def search_orders(self, user_id: str, query: str) -> List[Order]:
        user_orders = self.get_user_orders(user_id)
        query_lower = query.lower()
        results = []
        for order in user_orders:
            if query_lower in order.order_id.lower():
                results.append(order)
                continue
            for item in order.order_items:
                if query_lower in item.product_name.lower():
                    results.append(order)
                    break
        return results
    
    def get_previously_ordered_products(self, user_id: str) -> List[str]:
        product_ids = set()
        for order in self.get_user_orders(user_id):
            product_ids.update(order.get_ordered_product_ids())
        return list(product_ids)
    
    def get_quick_reorder_items(self, user_id: str) -> List[OrderItem]:
        recent_orders = self.get_recent_orders(user_id, limit=1)
        return recent_orders[0].order_items if recent_orders else []
    
    def get_orders_by_date_range(self, user_id: str, start_date: datetime, 
                                 end_date: datetime) -> List[Order]:
        return [
            o for o in self.get_user_orders(user_id)
            if start_date <= o.order_date <= end_date
        ]
    
    def get_total_orders_count(self, user_id: str) -> int:
        return len(self._user_orders.get(user_id, []))
    
    def get_total_spent(self, user_id: str) -> float:
        delivered_orders = [o for o in self.get_user_orders(user_id) if o.is_delivered()]
        return sum(o.total_amount for o in delivered_orders)
