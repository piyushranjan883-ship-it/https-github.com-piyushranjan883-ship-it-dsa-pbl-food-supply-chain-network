"""Unit 1 - AVL tree. Used as the batch-ID index."""


class AVLNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.height = 1


def height(node):
    return node.height if node else 0


def update_height(node):
    node.height = 1 + max(height(node.left), height(node.right))


def balance_factor(node):
    return height(node.left) - height(node.right) if node else 0


def rotate_right(y):
    x = y.left
    y.left = x.right
    x.right = y
    update_height(y)
    update_height(x)
    return x


def rotate_left(x):
    y = x.right
    x.right = y.left
    y.left = x
    update_height(x)
    update_height(y)
    return y


def insert(node, key, value):
    if node is None:
        return AVLNode(key, value)
    if key < node.key:
        node.left = insert(node.left, key, value)
    elif key > node.key:
        node.right = insert(node.right, key, value)
    else:
        node.value = value          # same key: just update
        return node
    update_height(node)
    bf = balance_factor(node)
    if bf > 1 and key < node.left.key:        # left-left
        return rotate_right(node)
    if bf < -1 and key > node.right.key:      # right-right
        return rotate_left(node)
    if bf > 1 and key > node.left.key:        # left-right
        node.left = rotate_left(node.left)
        return rotate_right(node)
    if bf < -1 and key < node.right.key:      # right-left
        node.right = rotate_right(node.right)
        return rotate_left(node)
    return node


def search(node, key):
    while node is not None:
        if key == node.key:
            return node.value
        node = node.left if key < node.key else node.right
    return None


def inorder(node, out=None):
    """In-order traversal (Unit 1): keys come out sorted."""
    if out is None:
        out = []
    if node:
        inorder(node.left, out)
        out.append(node.key)
        inorder(node.right, out)
    return out


def is_balanced(node):
    """True if every node has balance factor -1, 0 or 1."""
    if node is None:
        return True
    return (abs(balance_factor(node)) <= 1
            and is_balanced(node.left) and is_balanced(node.right))
