"This solution is the one proposed by the teacher. Not mine."

from collections.abc import MutableMapping

from yogi import scan


class Map_AVL(MutableMapping):
    """Sorted map implementation using an AVL binary search tree."""

    # -------------------------- nested _Node class --------------------------
    class _Node:
        """Node class for AVL maintains height value for balancing.

        We use convention that a "None" child has height 0, thus a leaf has height 1.
        """

        __slots__ = "_element", "_parent", "_left", "_right", "_height"

        def __init__(self, element, parent=None, left=None, right=None):
            self._element = element
            self._parent = parent
            self._left = left
            self._right = right
            self._height = 0

        def left_height(self):
            return self._left._height if self._left is not None else 0

        def right_height(self):
            return self._right._height if self._right is not None else 0

    # ------------------------------- nested _Item class ---------------------
    class _Item:
        """Lightweight composite to store key-value pairs as map items."""

        __slots__ = "_key", "_value"

        def __init__(self, k, v):
            self._key = k
            self._value = v

        def __eq__(self, other):
            return self._key == other._key  # compare items based on their keys

        def __ne__(self, other):
            return not (self == other)  # opposite of __eq__

        def __lt__(self, other):
            return self._key < other._key  # compare items based on their keys

    # -------------------------- nested Position class --------------------------
    class Position:
        """An abstraction representing the location of a single element."""

        __slots__ = "_container", "_node"

        def __init__(self, container, node):
            """Constructor should not be invoked by user."""
            self._container = container
            self._node = node

        def element(self):
            """Return the element stored at this Position."""
            return self._node._element

        def key(self):
            """Return key of map's key-value pair."""
            return self.element()._key

        def value(self):
            """Return value of map's key-value pair."""
            return self.element()._value

        def __eq__(self, other):
            """Return True if other is a Position representing the same location."""
            return type(other) is type(self) and other._node is self._node

        def __ne__(self, other):
            """Return True if other does not represent the same location."""
            return not (self == other)  # opposite of __eq__

    # --------------------- nonpublic methods providing "positional" support ----
    def _validate(self, p):
        """Return associated node, if position is valid."""
        if not isinstance(p, self.Position):
            raise TypeError("p must be proper Position type")
        if p._container is not self:
            raise ValueError("p does not belong to this container")
        if p._node._parent is p._node:  # convention for deprecated nodes
            raise ValueError("p is no longer valid")
        return p._node

    def _make_position(self, node):
        """Return Position instance for given node (or None if no node)."""
        return self.Position(self, node) if node is not None else None

    # -------------------------- constructor --------------------------
    def __init__(self):
        """Create an initially empty AVL tree map tree."""
        self._root = None
        self._size = 0

    def __len__(self):
        """Return the total number of elements in the tree."""
        return self._size

    def is_empty(self):
        """Return True if the tree is empty."""
        return len(self) == 0

    # ------------------------------- nonpublic utilities ---------------------

    def _subtree_search_n(self, p, k):  # node versions end in '_n'
        """Return Node of p's subtree having key k, or last node searched. p is a node"""
        if k == p._element._key:
            return p
        elif k < p._element._key:
            if p._left is not None:
                return self._subtree_search_n(p._left, k)
        else:
            if p._right is not None:
                return self._subtree_search_n(p._right, k)
        return p

    def _subtree_first_position_n(self, p):
        """Return Node of first item in subtree rooted at p."""
        walk = p
        while walk._left is not None:
            walk = walk._left
        return walk

    def _subtree_last_position_n(self, p):
        """Return Node of last item in subtree rooted at p."""
        walk = p
        while walk._right is not None:
            walk = walk._right
        return walk

    # -------------------------- public accessors --------------------------

    def first(self):
        """Return the first Position in the tree (or None if empty)."""
        if len(self) == 0:
            return None
        node = self._subtree_first_position_n(self._root)
        return self._make_position(node)

    def last(self):
        """Return the last Position in the tree (or None if empty)."""
        if len(self) == 0:
            return None
        node = self._subtree_last_position_n(self._root)
        return self._make_position(node)

    def before(self, p):
        """Return the Position just before p in the natural order.

        Return None if p is the first position.
        """
        node = self._validate(p)
        if node._left:
            n = self._subtree_last_position_n(node._left)
            return self._make_position(n)
        else:
            # walk upward
            walk = node
            above = walk._parent
            while above is not None and walk == above._left:
                walk = above
                above = walk._parent
            return self._make_position(above)

    def after(self, p):
        """Return the Position just after p in the natural order.

        Return None if p is the last position.
        """
        node = self._validate(p)
        if node._right:
            n = self._subtree_first_position_n(node._right)
            return self._make_position(n)
        else:
            walk = node
            above = walk._parent
            while above is not None and walk == above._right:
                walk = above
                above = walk._parent
            return self._make_position(above)

    def find_position_n(self, k):
        """Return Position with key k, or else neighbor (or None if empty)."""
        if self.is_empty():
            return None
        else:
            p = self._subtree_search_n(self._root, k)
            return self._make_position(p)

    def _delete_n(self, p):
        """Remove the item at given Node."""
        # self._validate(p)
        if p._left and p._right:  # p has two children
            replacement = self._subtree_last_position_n(p._left)
            self._replace(p, replacement._element)
            p = replacement
        # now p has at most one child
        parent = p._parent
        self._delete1_n(p)
        self._rebalance_delete(parent)  # if root deleted, parent is None

    def _recompute_height(self, node):
        node._height = 1 + max(node.left_height(), node.right_height())

    def _isbalanced(self, node):
        return abs(node.left_height() - node.right_height()) <= 1

    def _tall_child(self, node, favorleft=False):  # parameter controls tiebreaker
        if node.left_height() + (1 if favorleft else 0) > node.right_height():
            return node._left
        else:
            return node._right

    def _tall_grandchild(self, p):
        child = self._tall_child(p)
        # if child is on left, favor left grandchild; else favor right grandchild
        alignment = child == p._left
        return self._tall_child(child, alignment)

    def _rebalance(self, p):
        while p is not None:
            old_height = p._height  # trivially 0 if new node
            if not self._isbalanced(p):  # imbalance detected!
                # perform trinode restructuring, setting p to resulting root,
                # and recompute new local heights after the restructuring
                p = self._restructure(self._tall_grandchild(p))
                self._recompute_height(p._left)
                self._recompute_height(p._right)
            self._recompute_height(p)  # adjust for recent changes
            if p._height == old_height:  # has height changed?
                p = None  # no further changes needed
            else:
                p = p._parent  # repeat with parent

    def _rebalance_insert(self, p):
        self._rebalance(p)

    def _rebalance_delete(self, p):
        self._rebalance(p)

    # --------------------- nonpublic methods to support tree balancing -----

    def _relink(self, parent, child, make_left_child):
        """Relink parent node with child node (we allow child to be None)."""
        if make_left_child:  # make it a left child
            parent._left = child
        else:  # make it a right child
            parent._right = child
        if child is not None:  # make child point to parent
            child._parent = parent

    def _rotate(self, p):
        """Rotate Position p above its parent.

    Switches between these configurations, depending on whether p==a or p==b.

          b                  a
         / \                /  \
        a  t2             t0   b
       / \                     / \
      t0  t1                  t1  t2

    Caller should ensure that p is not the root.
    """
        """Rotate Position p above its parent."""
        x = p
        y = x._parent  # we assume this exists
        z = y._parent  # grandparent (possibly None)
        if z is None:
            self._root = x  # x becomes root
            x._parent = None
        else:
            self._relink(z, x, y == z._left)  # x becomes a direct child of z
        # now rotate x and y, including transfer of middle subtree
        if x == y._left:
            self._relink(y, x._right, True)  # x._right becomes left child of y
            self._relink(x, y, False)  # y becomes right child of x
        else:
            self._relink(y, x._left, False)  # x._left becomes right child of y
            self._relink(x, y, True)  # y becomes left child of x

    def _restructure(self, x):
        """Perform a trinode restructure among Position x, its parent, and its grandparent.

    Return the Position that becomes root of the restructured subtree.

    Assumes the nodes are in one of the following configurations:

        z=a                 z=c           z=a               z=c  
       /  \                /  \          /  \              /  \  
      t0  y=b             y=b  t3       t0   y=c          y=a  t3 
         /  \            /  \               /  \         /  \     
        t1  x=c         x=a  t2            x=b  t3      t0   x=b    
           /  \        /  \               /  \              /  \    
          t2  t3      t0  t1             t1  t2            t1  t2   

    The subtree will be restructured so that the node with key b becomes its root.

              b
            /   \
          a       c
         / \     / \
        t0  t1  t2  t3

    Caller should ensure that x has a grandparent.
    """
        """Perform trinode restructure of Position x with parent/grandparent."""
        y = x._parent
        z = y._parent
        if (x == y._right) == (y == z._right):  # matching alignments
            self._rotate(y)  # single rotation (of y)
            return y  # y is new subtree root
        else:  # opposite alignments
            self._rotate(x)  # double rotation (of x)
            self._rotate(x)
            return x  # x is new subtree root

    # -------------------------- nonpublic mutators --------------------------

    def _add_root_n(self, e):
        """Place element e at the root of an empty tree and return new Node.

        Raise ValueError if tree nonempty.
        """
        if self._root is not None:
            raise ValueError("Root exists")
        self._size = 1
        self._root = self._Node(e)
        return self._root

    def _add_left_n(self, node, e):
        """Create a new left child for Node p, storing element e.

        Return the new node.
        Raise ValueError if Position p is invalid or p already has a left child.
        """
        if node._left is not None:
            raise ValueError("Left child exists")
        self._size += 1
        node._left = self._Node(e, node)
        return node._left

    def _add_right_n(self, node, e):
        """Create a new right child for Node p, storing element e.

        Return the new node.
        Raise ValueError if Position p is invalid or p already has a right child.
        """
        if node._right is not None:
            raise ValueError("Right child exists")
        self._size += 1
        node._right = self._Node(e, node)
        return node._right

    def _replace(self, p, e):
        """Replace the element at Node p with e, and return old element."""
        old = p._element
        p._element = e
        return old

    def _delete1_n(self, p):
        """Delete the node p, and replace it with its child, if any.

        Return the element that had been stored at Node p.
        Raise ValueError if p has two children.
        """
        if p._left and p._right:
            raise ValueError("Position has two children")
        child = p._left if p._left else p._right  # might be None
        if child is not None:
            child._parent = p._parent  # child's grandparent becomes parent
        if p is self._root:
            self._root = child  # child becomes root
        else:
            parent = p._parent
            if p is parent._left:
                parent._left = child
            else:
                parent._right = child
        self._size -= 1
        p._parent = p  # convention for deprecated node
        return p._element

    def _attach(self, p, t1, t2):
        """Attach trees t1 and t2, respectively, as the left and right subtrees of the external Node p.

        As a side effect, set t1 and t2 to empty.
        Raise TypeError if trees t1 and t2 do not match type of this tree.
        Raise ValueError if Position p is invalid or not external.
        """
        if p._left or p._right:
            raise ValueError("position must be leaf")
        if not type(self) is type(t1) is type(t2):
            raise TypeError("Tree types must match")
        self._size += len(t1) + len(t2)
        if not t1.is_empty():
            t1._root._parent = p
            p._left = t1._root
            t1._root = None
            t1._size = 0
        if not t2.is_empty():
            t2._root._parent = p
            p._right = t2._root
            t2._root = None
            t2._size = 0

    # --------------------- public methods for (standard) map interface ---------

    def __delitem__(self, k):
        """Remove item associated with key k (raise KeyError if not found)."""
        if not self.is_empty():
            p = self._subtree_search_n(self._root, k)
            if k == p._element._key:
                self._delete_n(p)  # rely on positional version
                return  # successful deletion complete
        raise KeyError("Key Error: " + repr(k))

    def __iter__(self):
        """Generate an iteration of all keys in the map in order."""
        p = self.first()
        while p is not None:
            yield p.key()
            p = self.after(p)

    # --------------------- public methods for sorted map interface -------------

    def __reversed__(self):
        """Generate an iteration of all keys in the map in reverse order."""
        p = self.last()
        while p is not None:
            yield p.key()
            p = self.before(p)

    def find_min(self):
        """Return (key,value) pair with minimum key (or None if empty)."""
        if self.is_empty():
            return None
        else:
            p = self.first()
            return (p.key(), p.value())

    def find_max(self):
        """Return (key,value) pair with maximum key (or None if empty)."""
        if self.is_empty():
            return None
        else:
            p = self.last()
            return (p.key(), p.value())

    ### --------------- METHODS FOR NEW VERSION, HOPEFULLY EFFICIENT --------

    def __getitem__(self, k):  # @
        """Return value associated with key k (raise KeyError if not found)."""
        if self.is_empty():
            raise KeyError("Key Error: " + repr(k))
        else:
            p = self._subtree_search_n(self._root, k)
            if k != p._element_key:
                raise KeyError("Key Error: " + repr(k))
            return p._element._value

    def __setitem__(self, k, v):  # @
        """Assign value v to key k, overwriting existing value if present."""
        if self.is_empty():
            leaf = self._add_root_n(self._Item(k, v))
        else:
            p = self._subtree_search_n(self._root, k)
            if p._element._key == k:
                p._element._value = v
                return
            else:
                item = self._Item(k, v)
                if p._element._key < k:
                    leaf = self._add_right_n(p, item)
                else:
                    leaf = self._add_left_n(p, item)
        self._rebalance_insert(leaf)


if __name__ == "__main__":
    st = scan(str)
    if st != "END":
        s = Map_AVL()  # We use the map as a set, storing key-value pairs of the form (key, None).
        s[st] = None
        p = s.first()
        print(p.key())
        st = scan(str)
        while st != "END":
            s[st] = None
            if p.key() < st:
                if len(s) % 2 == 1:
                    p = s.after(p)
            elif p.key() > st:
                if len(s) % 2 == 0:
                    p = s.before(p)
            print(p.key())
            st = scan(str)
