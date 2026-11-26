"""Main logic: joins all structures. Rules R1 to R9."""
import heapq

from . import avl, planner
from .graph import TransportGraph
from .rbtree import RedBlackTree

DUPLICATE_LIMIT = 80        # percent similarity treated as duplicate


class FoodNetwork:
    def __init__(self):
        self.batches = {}                  # id -> record
        self.next_id = 1
        self.avl_root = None               # batch-ID index (AVL)
        self.name_index = RedBlackTree()   # product-name index (Red-Black)
        self.graph = TransportGraph()      # transport network

    # ---- R1, R2, R3 -------------------------------------------------
    def add_batch(self, product, location, kg, days_left, priority):
        product = (product or "").strip()
        location = (location or "").strip()
        if not product or not location:
            return False, "Product and location are required."               # R1
        if not isinstance(kg, int) or kg <= 0:
            return False, "Weight must be a positive whole number of kg."     # R1
        if not isinstance(days_left, int) or days_left < 0:
            return False, "Days left must be a whole number, 0 or more."     # R1
        if not isinstance(priority, int) or not 1 <= priority <= 10:
            return False, "Priority must be a whole number from 1 to 10."    # R1
        for r in self.batches.values():                                       # R2
            if r["location"] == location:
                sim = planner.lcs_similarity(product, r["product"])
                if sim >= DUPLICATE_LIMIT:
                    return False, (f"Possible duplicate of #{r['id']} "
                                   f"'{r['product']}' ({sim:.0f}% similar).")
        bid = self.next_id                                                    # R3
        self.next_id += 1
        record = {"id": bid, "product": product, "location": location,
                  "kg": kg, "days_left": days_left, "priority": priority}
        self.batches[bid] = record
        self.avl_root = avl.insert(self.avl_root, bid, record)
        self.name_index.insert(product.lower(), record)
        return True, f"Saved as batch #{bid}."

    # ---- R4, R5 -----------------------------------------------------
    def find_by_id(self, bid):
        return avl.search(self.avl_root, bid)

    def find_by_name(self, product):
        return self.name_index.search(" ".join(product.lower().split()))

    # ---- R6 ---------------------------------------------------------
    def most_urgent(self, k=3):
        """Fewest days left first, using a heap."""
        return heapq.nsmallest(k, self.batches.values(),
                               key=lambda r: (r["days_left"], -r["priority"]))

    # ---- R7 ---------------------------------------------------------
    def load_plan(self, location, truck_kg):
        items = [(r["product"], r["kg"], r["priority"])
                 for r in self.batches.values() if r["location"] == location]
        return planner.knapsack(items, truck_kg)

    # ---- R8 ---------------------------------------------------------
    def exact_load_plans(self, location, truck_kg):
        items = [(r["product"], r["kg"])
                 for r in self.batches.values() if r["location"] == location]
        return planner.sum_of_subsets(items, truck_kg)

    # ---- R9 ---------------------------------------------------------
    def nearby_places(self, place, steps=2):
        return self.graph.nearby(place, steps)

    def best_route(self, src, dst):
        return self.graph.shortest_route(src, dst)
