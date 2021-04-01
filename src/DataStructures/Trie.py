"""
Implementation of a trie, AKA prefix tree/digital tree. Includes the implementation of Trie Node and Trie itself.
Supports insertion of any

This implementation uses a traditional tree, not the space optimized radix tree. It only supports insert and search,
does not have an implementation of delete.

More details at:
    https://en.wikipedia.org/wiki/Trie
"""
from src.DataStructures.Node import Node


class Trie:
    """
    Implementation of the trie.

    Stores the root of the trie. Contains implementation for insert and search, no implementation of delete.
    """
    def __init__(self):
        """
        The initializer.
        """
        # The root of the trie, this is where the tree will begin
        self.root = Node("-1")

    def insert(self, to_insert):
        """
        Inserts the given to_insert into the trie if it is not already there.
        :param to_insert:
        :return:
        """
        # The iterator that will be used to navigate the tree
        current = self.root

        # Traverse the tree
        for c in to_insert:
            # Check if the current letter can be found, if not add it into the children
            node = Node(c)
            if c not in current.children_index:
                current.children.append(node)
                current.children_index[c] = len(current.children) - 1
            # Now fetch the child
            current = current.children[current.children_index[c]]

        # Mark the end of the work
        current.leaf = True

    def query(self, prefix):
        """
        Searches through the trie to find the words that start with this prefix.

        Returns the results, all the words that start with the prefix.
        :param prefix:
        :return:
        """
        # If the prefix is nothing, an empty string is passed in, just return and empty list
        if len(prefix) < 1:
            return set()
        # The iterator that will be used to navigate the tree
        current = self.root

        # Traverse the tree
        for c in prefix:
            # Check if the prefix is in the tree, if yes, keep digging down
            if c in current.children_index:
                current = current.children[current.children_index[c]]
            else:
                # If not found, the word does not exist in the tree, return and empty list
                return set()

        # At this point, we are at the end of the prefix in the tree, need to traverse the tree to get all the words
        return self.dfs(prefix, current)

    def dfs(self, prefix, node):
        """
        Traverse the tree from the node passed in to grab all the words that should be suggested.
        :param prefix:
        :param node:
        :return:
        """
        # The set of words to return
        words = []
        # Will be used to traverse the stack
        stack = [node]
        # Add the node to the stack
        # Holds the children of the nodes that have been visited, children visited tracker(cvt)
        cvt = {}
        # The current word
        word = prefix

        # Iterate until the stack becomes empty
        while len(stack) > 0:
            # If there are no children, cannot go any deeper, pop this item from the stack and assign the last item to
            # node
            if len(node.children) == 0:
                if node.leaf:
                    words.append(word)

                # Has no children, remove from stack and decrease the word length
                stack.pop()
                word = word[:-1]
                # If the stack is not empty, assign the last element from the stack
                if len(stack) > 0:
                    node = stack[-1]
            else:
                # The node has not been visited before, add a cvt and continue
                if node.unique_id not in cvt:
                    if node.leaf:
                        words.append(word)
                    # Assign cvt
                    cvt[node.unique_id] = 0
                    # Add to stack
                    stack.append(node.children[0])
                    # Change the current node to th first child
                    node = node.children[0]
                    # Add the letter to the word if it is not the root node
                    if node.value != -1:
                        word += node.value
                # Node is in cvt, check if the incremented value is in range of index
                elif cvt[node.unique_id] < len(node.children) - 1:
                    # Increment the value
                    cvt[node.unique_id] += 1
                    # Use the value for the child
                    stack.append(node.children[cvt[node.unique_id]])
                    # Change the node to the child
                    node = node.children[cvt[node.unique_id]]
                    # Add the letter to the word if it is not the root node
                    if node.value != -1:
                        word += node.value
                # Node has been visited before and all the children have been explored, time to remove from stack and
                # move on
                else:
                    stack.pop()
                    word = word[:-1]
                    if len(stack) > 0:
                        node = stack[-1]

        return words
