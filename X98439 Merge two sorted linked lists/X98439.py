from typing import Any, Generic, Iterator, TypeVar, Union

from yogi import scan

T = TypeVar("T")
NT = TypeVar("NT")


class _DoublyLinkedBase(Generic[T]):
    """A base class providing a doubly linked list representation."""

    # -------------------------- nested _Node class --------------------------
    # nested _Node class
    class _Node(Generic[NT]):
        """Lightweight, nonpublic class for storing a doubly linked node."""

        __slots__ = "_element", "_prev", "_next"

        def __init__(
            self,
            element: NT,
            prev: Union["_DoublyLinkedBase._Node[NT]", None],
            next: Union["_DoublyLinkedBase._Node[NT]", None],
        ) -> None:
            self._element = element
            self._prev = prev
            self._next = next

    # -------------------------- list constructor --------------------------

    def __init__(self) -> None:
        """Create an empty list."""
        self._header = self._Node(None, None, None)
        self._trailer = self._Node(None, None, None)
        self._header._next = self._trailer
        self._trailer._prev = self._header
        self._size = 0

    # -------------------------- public accessors --------------------------

    def __len__(self) -> int:
        """Return the number of elements in the list."""
        return self._size

    def is_empty(self) -> bool:
        """Return True if list is empty."""
        return self._size == 0

    # -------------------------- nonpublic utilities --------------------------

    def _insert_between(self, e: T, predecessor: _Node[T], successor: _Node[T]) -> _Node[T]:
        """Add element e between two existing nodes and return new node."""
        newest = self._Node(e, predecessor, successor)
        predecessor._next = newest
        successor._prev = newest
        self._size += 1
        return newest

    def _delete_node(self, node: _Node[T]) -> T:
        """Delete non-sentinel node from the list and return its element."""
        predecessor = node._prev
        successor = node._next
        predecessor._next = successor
        successor._prev = predecessor
        self._size -= 1
        element = node._element
        node._prev = node._next = node._element = None
        return element


class PositionalList(_DoublyLinkedBase[T]):
    """A sequential container of elements allowing positional access."""

    # -------------------------- nested Position class --------------------------
    class Position(Generic[NT]):
        """An abstraction representing the location of a single element.

        Note that two position instances may represent the same inherent
        location in the list.  Therefore, users should always rely on
        syntax 'p == q' rather than 'p is q' when testing equivalence of
        positions.
        """

        def __init__(self, container: "PositionalList[NT]", node: "_DoublyLinkedBase._Node[NT]") -> None:
            """Constructor should not be invoked by user."""
            self._container = container
            self._node = node

        def element(self) -> NT:
            """Return the element stored at this Position."""
            return self._node._element

        def __eq__(self, other: Any) -> bool:
            """Return True if other is a Position representing the same location."""
            return type(other) is type(self) and other._node is self._node

        def __ne__(self, other: Any) -> bool:
            """Return True if other does not represent the same location."""
            return not (self == other)  # opposite of __eq__

    # ------------------------------- utility methods -------------------------------
    def _validate(self, p: "PositionalList.Position[T]") -> "_DoublyLinkedBase._Node[T]":
        """Return position's node, or raise appropriate error if invalid."""
        if not isinstance(p, self.Position):
            raise TypeError("p must be proper Position type")
        if p._container is not self:
            raise ValueError("p does not belong to this container")
        if p._node._next is None:  # convention for deprecated nodes
            raise ValueError("p is no longer valid")
        return p._node

    def _make_position(self, node: "_DoublyLinkedBase._Node[T]") -> "PositionalList.Position[T]":
        """Return Position instance for given node (or None if sentinel)."""
        if node is self._header or node is self._trailer:
            return None
        else:
            return self.Position(self, node)

    # ------------------------------- accessors -------------------------------
    def first(self) -> "PositionalList.Position[T]":
        """Return the first Position in the list (or None if list is empty)."""
        return self._make_position(self._header._next)

    def last(self) -> "PositionalList.Position[T]":
        """Return the last Position in the list (or None if list is empty)."""
        return self._make_position(self._trailer._prev)

    def before(self, p: "PositionalList.Position[T]") -> "PositionalList.Position[T]":
        """Return the Position just before Position p (or None if p is first)."""
        node = self._validate(p)
        return self._make_position(node._prev)

    def after(self, p: "PositionalList.Position[T]") -> "PositionalList.Position[T]":
        """Return the Position just after Position p (or None if p is last)."""
        node = self._validate(p)
        return self._make_position(node._next)

    def __iter__(self) -> Iterator[T]:
        """Generate a forward iteration of the elements of the list."""
        cursor = self.first()
        while cursor is not None:
            yield cursor.element()
            cursor = self.after(cursor)

    # ------------------------------- mutators -------------------------------
    # override inherited version to return Position, rather than Node
    def _insert_between(
        self, e: T, predecessor: "_DoublyLinkedBase._Node[T]", successor: "_DoublyLinkedBase._Node[T]"
    ) -> "PositionalList.Position[T]":
        """Add element between existing nodes and return new Position."""
        node = super()._insert_between(e, predecessor, successor)
        return self._make_position(node)

    def add_first(self, e: T) -> "PositionalList.Position[T]":
        """Insert element e at the front of the list and return new Position."""
        return self._insert_between(e, self._header, self._header._next)

    def add_last(self, e: T) -> "PositionalList.Position[T]":
        """Insert element e at the back of the list and return new Position."""
        return self._insert_between(e, self._trailer._prev, self._trailer)

    def add_before(self, p: "PositionalList.Position[T]", e: T) -> "PositionalList.Position[T]":
        """Insert element e into list before Position p and return new Position."""
        original = self._validate(p)
        return self._insert_between(e, original._prev, original)

    def add_after(self, p: "PositionalList.Position[T]", e: T) -> "PositionalList.Position[T]":
        """Insert element e into list after Position p and return new Position."""
        original = self._validate(p)
        return self._insert_between(e, original, original._next)

    def delete(self, p: "PositionalList.Position[T]") -> T:
        """Remove and return the element at Position p."""
        original = self._validate(p)
        return self._delete_node(original)

    def replace(self, p: "PositionalList.Position[T]", e: T) -> T:
        """Replace the element at Position p with e.

        Return the element formerly at Position p.
        """
        original = self._validate(p)
        old_value = original._element
        original._element = e
        return old_value

    def merge(self, other: "PositionalList[T]") -> None:
        """
        Pre: self and other are two lists sorted in ascending order.
        Post: After the merge operation 'self' contains its previous
              elements and all the elements in 'other' is ascending
              order. Furthermore, 'other' is empty.
        Observation: Because 'other' must be empty after carrying out
           the merge operation, there is no need to create new modes.
        """
        write_current = self._header  # The node to which we will write
        # Our result will be stored in self. That's why write_current starts at self._header
        self_current = self._header._next  # The node we are currently looking at in "self"
        # We could remove the pointers from self._header to self_current and from self_current to self._header,
        # but it is not necessary as we will later set them to some node in the updated self.
        other_current = other._header._next  # The node we are currently looking at in "other"
        other._header._next = other._trailer  # Disconnect the start of "other"
        # We could also have removed the pointer from other_current to other._header, but it is not necessary
        # as we will later set it to some node in the updated self.
        while self_current is not self._trailer and other_current is not other._trailer:
            # While we have not reached the end of either list
            if self_current._element < other_current._element:
                # We must add the self_current node to the result
                # Update pointers
                write_current._next = self_current
                self_current._prev = write_current
                # Move to the next node
                write_current = self_current
                self_current = self_current._next
                # We don't update sizes here, because we are "removing" a node from self
                # and adding it back to self, so the size remains the same
            else:
                # We must add the other_current node to the result
                # Update pointers
                write_current._next = other_current
                other_current._prev = write_current
                # Move to the next node
                write_current = other_current
                other_current = other_current._next
                # Update sizes from both lists
                other._size -= 1
                self._size += 1
                # We update sizes here, because if at the end there are still elements in "other",
                # we want to know how many without having to traverse the list.

        if self_current is not self._trailer:
            # If we have reached the end of "other" but not of "self", we must add the
            # remaining nodes of "self".
            # Update pointers
            write_current._next = self_current
            self_current._prev = write_current
            # We don't update trailer here, because the last node in the result is the last node in "self",
            # so self._trailer already points to the last node in the result.
        elif other_current is not other._trailer:
            # If we have reached the end of "self" but not of "other", we must add the
            # remaining nodes of "other".
            # Update pointers
            write_current._next = other_current
            other_current._prev = write_current
            # Because all the remaining nodes are from "other", the last node in the result
            # is the last node in "other", so we must set self._trailer to the last node in "other".
            self._trailer._prev = other._trailer._prev
            # Whatever the last node in "other" was pointing to, it must be now pointing to self._trailer
            other._trailer._prev._next = self._trailer
            # Update sizes
            self._size += other._size

        # At the end, we must set the size of "other" to 0 and finish disconnecting the nodes
        # from other. Other's header was already updated to point to other's trailer.
        other._trailer._prev = other._header
        other._size = 0


if __name__ == "__main__":
    n = scan(int)
    t1 = PositionalList()
    for i in range(n):
        t1.add_last(scan(float))
    n = scan(int)
    t2 = PositionalList()
    for i in range(n):
        t2.add_last(scan(float))
    t1.merge(t2)
    print("t1", end="")
    for e in t1:
        print(" ", e, end="")
    print("\nt2", end="")
    for e in t2:
        print(" ", e, end="")
