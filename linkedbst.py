"""
File: linkedbst.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from linkedqueue import LinkedQueue
from math import log
import random
import time
import sys
sys.setrecursionlimit(100000)


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            str_ = ""
            if node != None:
                str_ += recurse(node.right, level + 1)
                str_ += "| " * level
                str_ += str(node.data) + "\n"
                str_ += recurse(node.left, level + 1)
            return str_

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1


    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftmaxinleftsubtreetotop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentnode = top.left
            while not currentnode.right == None:
                parent = currentnode
                currentnode = currentnode.right
            top.data = currentnode.data
            if parent == top:
                top.left = currentnode.left
            else:
                parent.right = currentnode.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        itemremoved = None
        preroot = BSTNode(None)
        preroot.left = self._root
        parent = preroot
        direction = 'L'
        currentnode = self._root
        while not currentnode == None:
            if currentnode.data == item:
                itemremoved = currentnode.data
                break
            parent = currentnode
            if currentnode.data > item:
                direction = 'L'
                currentnode = currentnode.left
            else:
                direction = 'R'
                currentnode = currentnode.right

        # Return None if the item is absent
        if itemremoved == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentnode.left == None \
                and not currentnode.right == None:
            liftmaxinleftsubtreetotop(currentnode)
        else:

            # Case 2: The node has no left child
            if currentnode.left == None:
                newchild = currentnode.right

                # Case 3: The node has no right child
            else:
                newchild = currentnode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newchild
            else:
                parent.right = newchild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preroot.left
        return itemremoved

    def replace(self, item, newitem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                olddata = probe.data
                probe.data = newitem
                return olddata
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top is None:
                return 0
            if top.left is None and top.right is None:
                return 0

            left_sum = height1(top.left)
            right_sum = height1(top.right)

            return max(left_sum, right_sum) + 1

        return height1(self._root)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        return self.height() < 2 * log(len(list(self.inorder())) + 1) - 1

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        return list(self.inorder())\
            [list(self.inorder()).index(low):list(self.inorder()).index(high)+1]

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        def func(items):
            if not items:
                return None
            mid = len(items) // 2
            return BSTNode(items[mid], func(items[:mid]), func(items[mid + 1:]))

        items = list(self.inorder())
        self._root = func(items)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        if item not in list(self.inorder()):
            if item > list(self.inorder())[-1]:
                return None
            elem = min(list(self.inorder()), key=lambda x:abs(x-item))
            return list(self.inorder())[list(self.inorder()).index(elem) + 1:][0]
        return list(self.inorder())[list(self.inorder()).index(item)+1:][0]\
            if item != list(self.inorder())[-1] else None

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        if item not in list(self.inorder()):
            if item < list(self.inorder())[0]:
                return None
            elem = min(list(self.inorder()), key=lambda x:abs(x-item))
            return list(self.inorder())[:list(self.inorder()).index(elem) + 1][-1]
        return list(self.inorder())[:list(self.inorder()).index(item)][-1]\
            if item != list(self.inorder())[0] else None


    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        words_from_file = []
        with open(path, 'r', encoding="utf-8") as new_file:
            for string_ in new_file:
                string_ = string_.strip()
                words_from_file.append(string_)

        # 1
        start = time.time()
        for _ in range(10000):
            random_word = random.choice(words_from_file)
            words_from_file.index(random_word)
        end = time.time()
        time_ = end - start
        print(f"Time needed for searching in list: {time_} seconds")
        print()

        # 2
        tree = LinkedBST()
        for item in words_from_file[:25000]:
            tree.add(item)

        start = time.time()
        for word in random.sample(words_from_file[:25000], 10000):
            tree.find(word)
        end = time.time()
        time_ = end - start
        print(f"Time needed for searching in sorted-alphabetically tree: {time_} seconds")
        print("The chosen number of elements is 25000 elements due to the restriction")
        print()

        #3
        tree1 = LinkedBST()
        random.shuffle(words_from_file)
        for item in words_from_file:
            tree1.add(item)

        start = time.time()
        for word in random.sample(words_from_file, 10000):
            tree1.find(word)
        end = time.time()
        time_ = end - start
        print(f"Time needed for searching in not sorted tree: {time_} seconds")
        print()

        #4
        tree1.rebalance()
        start = time.time()
        for word in random.sample(words_from_file, 10000):
            tree1.find(word)
        end = time.time()
        time_ = end - start
        print(f"Time needed for searching in rebalanced tree: {time_} seconds")


tree = LinkedBST()
print(tree.demo_bst("words.txt"))
