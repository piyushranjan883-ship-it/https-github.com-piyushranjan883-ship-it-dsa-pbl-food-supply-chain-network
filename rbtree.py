"""Unit 5 - Red-Black tree. Used as the product-name index."""
RED, BLACK = "R", "B"


class RBNode:
    def __init__(self, key, value, color, nil=None):
        self.key = key
        self.value = value
        self.color = color
        self.left = nil
        self.right = nil
        self.parent = nil


class RedBlackTree:
    def __init__(self):
        self.nil = RBNode(None, None, BLACK)    # one shared leaf
        self.root = self.nil
        self.size = 0

    def _rotate_left(self, x):
        y = x.right
        x.right = y.left
        if y.left is not self.nil:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is self.nil:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _rotate_right(self, x):
        y = x.left
        x.left = y.right
        if y.right is not self.nil:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is self.nil:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def insert(self, key, value):
        node = self.root
        parent = self.nil
        while node is not self.nil:
            parent = node
            if key == node.key:
                node.value = value      # same key: update only
                return
            node = node.left if key < node.key else node.right
        z = RBNode(key, value, RED, self.nil)
        z.parent = parent
        if parent is self.nil:
            self.root = z
        elif key < parent.key:
            parent.left = z
        else:
            parent.right = z
        self.size += 1
        self._fix_insert(z)

    def _fix_insert(self, z):
        # repair if the parent is also red
        while z.parent.color == RED:
            gp = z.parent.parent
            if z.parent == gp.left:
                uncle = gp.right
                if uncle.color == RED:              # case 1: recolour
                    z.parent.color = BLACK
                    uncle.color = BLACK
                    gp.color = RED
                    z = gp
                else:
                    if z == z.parent.right:         # case 2: turn into case 3
                        z = z.parent
                        self._rotate_left(z)
                    z.parent.color = BLACK          # case 3: rotate
                    gp.color = RED
                    self._rotate_right(gp)
            else:
                uncle = gp.left
                if uncle.color == RED:
                    z.parent.color = BLACK
                    uncle.color = BLACK
                    gp.color = RED
                    z = gp
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self._rotate_right(z)
                    z.parent.color = BLACK
                    gp.color = RED
                    self._rotate_left(gp)
        self.root.color = BLACK

    def search(self, key):
        node = self.root
        while node is not self.nil:
            if key == node.key:
                return node.value
            node = node.left if key < node.key else node.right
        return None

    def inorder(self):
        out = []

        def walk(n):
            if n is not self.nil:
                walk(n.left)
                out.append(n.key)
                walk(n.right)
        walk(self.root)
        return out

    def height(self):
        def h(n):
            return 0 if n is self.nil else 1 + max(h(n.left), h(n.right))
        return h(self.root)

    def check_rules(self):
        """Checks: root black, no red node with red child, equal black height."""
        if self.root.color != BLACK:
            return False

        def walk(n):
            if n is self.nil:
                return 1
            if n.color == RED and (n.left.color == RED or n.right.color == RED):
                return -1
            l, r = walk(n.left), walk(n.right)
            if l == -1 or r == -1 or l != r:
                return -1
            return l + (1 if n.color == BLACK else 0)
        return walk(self.root) != -1
