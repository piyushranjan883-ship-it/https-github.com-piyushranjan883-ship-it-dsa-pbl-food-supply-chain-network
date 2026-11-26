"""Unit 2 - transport graph (adjacency list), BFS and Dijkstra."""
import heapq
from collections import deque


class TransportGraph:
    def __init__(self):
        self.adj = {}                    # place -> list of (neighbour, km)

    def add_place(self, name):
        self.adj.setdefault(name, [])

    def add_road(self, a, b, km):
        self.add_place(a)
        self.add_place(b)
        self.adj[a].append((b, km))
        self.adj[b].append((a, km))

    def nearby(self, start, steps=2):
        """BFS: places reachable within `steps` roads. None if unknown place."""
        if start not in self.adj:
            return None
        seen = {start: 0}
        queue = deque([start])
        while queue:
            cur = queue.popleft()
            if seen[cur] == steps:
                continue
            for nxt, _ in self.adj[cur]:
                if nxt not in seen:
                    seen[nxt] = seen[cur] + 1
                    queue.append(nxt)
        return sorted(p for p in seen if p != start)

    def shortest_route(self, src, dst):
        """Dijkstra. Returns (total_km, [places]) or (None, []) if no route."""
        if src not in self.adj or dst not in self.adj:
            return None, []
        dist = {src: 0}
        prev = {}
        heap = [(0, src)]
        while heap:
            d, cur = heapq.heappop(heap)
            if d > dist.get(cur, float("inf")):
                continue
            if cur == dst:
                break
            for nxt, km in self.adj[cur]:
                nd = d + km
                if nd < dist.get(nxt, float("inf")):
                    dist[nxt] = nd
                    prev[nxt] = cur
                    heapq.heappush(heap, (nd, nxt))
        if dst not in dist:
            return None, []
        path = [dst]
        while path[-1] != src:
            path.append(prev[path[-1]])
        return dist[dst], path[::-1]
