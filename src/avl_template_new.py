# username - complete info
# id1      - complete info
# name1    - complete info
# id2      - complete info
# name2    - complete info
import random

"""A class represnting a node in an AVL tree"""


class AVLNode(object):
    """Constructor, you are allowed to add more fields.

    @type value: str
    @param value: data of your node
    """

    def __init__(self, value=None):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = -1  # Balance factor
        self.size = 0

    """returns the left child
    @rtype: AVLNode
    @returns: the left child of self, None if there is no left child
    """

    def getLeft(self):
        if self.getLeft().getHeight() == -1:
            return None
        return self.left

    """returns the right child

    @rtype: AVLNode
    @returns: the right child of self, None if there is no right child
    """

    def getRight(self):
        if self.getRight().getHeight() == -1:
            return None
        return self.right

    """returns the parent 

    @rtype: AVLNode
    @returns: the parent of self, None if there is no parent
    """

    def getParent(self):
        return self.parent

    """return the value

    @rtype: str
    @returns: the value of self, None if the node is virtual
    """

    def getValue(self):
        return self.value

    """returns the height

    @rtype: int
    @returns: the height of self, -1 if the node is virtual
    """

    def getHeight(self):
        return self.height

    """sets left child

    @type node: AVLNode
    @param node: a node
    """

    def setLeft(self, node):
        self.left = node

    """sets right child

    @type node: AVLNode
    @param node: a node
    """

    def setRight(self, node):
        self.right = node

    """sets parent

    @type node: AVLNode
    @param node: a node
    """

    def setParent(self, node):
        self.parent = node

    """sets value

    @type value: str
    @param value: data
    """

    def setValue(self, value):
        self.value = value

    """sets the balance factor of the node

    @type h: int
    @param h: the height
    """

    def setHeight(self, h):
        self.height = h

    def setSize(self, size):
        self.size = size

    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """

    def isRealNode(self):
        return self.height != -1


    def getSize(self):
        return self.size

    def updateSize(self):
        size = 1
        if self.getRight().isRealNode():
            size += self.getRight().getSize()
        if self.getLeft().isRealNode():
            size += self.getLeft().getSize()
        self.size = size

    def updateHeight(self):
        '''//TODO Update only on real nodes'''
        self.height = max(self.getRight().getHeight(), self.getLeft().getHeight()) + 1


"""
A class implementing the ADT list, using an AVL tree.
"""


class AVLTreeList(object):
    """
    Constructor, you are allowed to add more fields.

    """

    def __init__(self):
        self.size = 0
        self.root = None

    # add your fields here

    """returns whether the list is empty

    @rtype: bool
    @returns: True if the list is empty, False otherwise
    """

    def empty(self):
        return self.size == 0

    """retrieves the value of the i'th item in the list

    @type i: int
    @pre: 0 <= i < self.length()
    @param i: index in the list
    @rtype: str
    @returns: the the value of the i'th item in the list
    """

    def retrieve(self, i):
        def retrieve_rec(x, k):
            rank = x.getLeft().getSize() + 1
            if k == rank:
                return x
            elif k < rank:
                return retrieve_rec(x.getLeft(), k)
            else:
                return retrieve_rec(x.getRight(), k - rank)

        return retrieve_rec(self.root, i + 1)

    """inserts val at position i in the list

    @type i: int
    @pre: 0 <= i <= self.length()
    @param i: The intended index in the list to which we insert val
    @type val: str
    @param val: the value we inserts
    @rtype: list
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def insert(self, i, val):
        # 1. insert a new node

        new_node = AVLNode(val)
        new_node.setLeft(AVLNode())
        new_node.setRight(AVLNode())
        new_node.getRight().setParent(new_node)
        new_node.getLeft().setParent(new_node)
        new_node.updateHeight()
        new_node.updateSize()

        ## insert first node to empty tree
        if self.empty():
            self.root = new_node

        ## insert last node
        if i == self.size:
            node = self.most_right_node(self.root)
            new_node.setParent(node)
            node.setRight(new_node)
        else:
            node = self.retrieve(i+1)
            if not node.getLeft().isRealNode():
                node.setLeft(new_node)
                new_node.setParent(node)
            else:
                node_predesessor = self.getPredesessor(node)
                node_predesessor.setRight(new_node)
                new_node.setParent(node_predesessor)
        self.size += 1

        # 2. rebalance tree
        rotation_number = self.rebalanceTreeInsert(new_node)
        # 3. update size and height from inserted node to the root
        self.updateFromNodeToRoot(new_node)

        return rotation_number

    def updateFromNodeToRoot(self, x):
        while x.getParent() != None:
            x.getParent().updateHeight()
            x.getParent().updateSize()
            x = x.getParent()

    def rebalanceTreeInsert(self, x):
        rotation_number = 0
        y = x.parent
        while y != None:
            previous_height = y.height
            y.updateHeight()
            bf = y.left.height - y.right.height
            if abs(bf) < 2 and y.height == previous_height:
                break
            elif abs(bf) < 2 and y.height != previous_height:
                y = y.parent
            elif abs(bf) == 2:
                rotation_number = self.rotateTreeInsert(y)
                break
        return rotation_number


    def rotateTreeInsert(self, y):
        rotation_number = 0
        bf = y.left.height - y.right.height
        if bf == -2:
            bf_right = y.right.left.height - y.right.right.height
            if bf_right == -1:
                self.rotateLeft(y)
                rotation_number = 1
            elif bf_right == 1:
                self.rotateRight(y.right)
                self.rotateLeft(y)
                rotation_number = 2
        if bf == 2:
            bf_left = y.left.left.height - y.left.right.height
            if bf_left  == -1:
                self.rotateLeft(y.left)
                self.rotateRight(y)
                rotation_number = 2
            elif bf_left == 1:
                self.rotateRight(y)
                rotation_number = 1
        return rotation_number

    def rotateLeft(self, y):
        # 1. change pointers
        B = y
        A = y.getRight()
        B.setRight(A.getLeft())
        B.getRight().setParent(B)
        A.setLeft(B)
        A.setParent(B.getParent)
        if B.getParent() != None:
            if self.is_node_left_child(B):
                A.getParent.setLeft(A)
            else:
                A.getParent.setRight(A)
        ## B is root
        else:
            self.root = A
        B.setParent(A)

        # 2. update height and size only for A and B
        B.updateHeight()
        A.updateHeight()
        B.updateSize()
        A.updateSize()


    def rotateRight(self, y):
        # 1. change pointers
        B = y
        A = y.getLeft()
        B.setLeft(A.getRight())
        B.getleft().setParent(B)
        A.setRight(B)
        A.setParent(B.getParent())
        if B.getParent() != None:
            if self.is_node_left_child(B):
                A.getParent.setLeft(A)
            else:
                A.getParent.setRight(A)
        else:
            self.root = A
        B.setParent(A)
        # 2. update height and size only for A and B
        B.updateHeight()
        A.updateHeight()
        B.updateSize()
        A.updateSize()


    def getPredesessor(self, x):
        '''//TODO Detrmine what to do when no successor --- pointer to min and max??????????????????????????????????'''
        if x == self.most_left_node(x):
            return None
        if x.getLeft().isRealNode():
            return self.most_right_node(x.getLeft())
        y = x.getParent()
        while y != None and x == y.getLeft():
            x = y
            y = x.getParent()
        return y

    def getSucsessor(self, x):
        '''//TODO Detrmine what to do when no successor --- pointer to min and max??????????????????????????????????'''
        if x == self.most_right_node(x):
            return None
        if x.getRight().isRealNode():
            return self.most_left_node(x.getRight())
        y = x.getParent()
        while y != None and x == y.getRight():
            x = y
            y = x.getParent()
        return y

    def most_left_node(self, x):
        '''@returns the most left node in a tree'''
        while x.getLeft().isRealNode():
            x = x.getLeft()
        return x

    def most_right_node(self, x):
        '''@returns the most right node in a tree'''
        while x.getRight().isRealNode():
            x = x.getRight()
        return x

    """deletes the i'th item in the list

    @type i: int
    @pre: 0 <= i < self.length()
    @param i: The intended index in the list to be deleted
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def delete(self, i):
        if i >= self.size:
            return -1
        node = self.retrieve(i)
        self.size -= 1
        ### 1. delete node from tree:
        ## 1.1 node is leaf
        if node.getSize() == 1:
            self.deleteLeaf(node)
            num = self.rebalanceTreeDelete(node.getParent())
            return num

        # 1.2 node has only left child
        if node.getLeft().isRealNode() and not node.getRight().isRealNode():
            temp = node.getLeft()
            self.deleteNodeWithOnlyLeftChild(node)
            #rebalance tree
            num = self.rebalanceTreeDelete(temp)
            return num

        # 1.3 node has only right child
        if not node.getLeft().isRealNode() and node.getRight().isRealNode:
            temp = node.getRight()
            self.deleteNodeWithOnlyRightChild(node)
            # rebalance tree
            num = self.rebalanceTreeDelete(temp)
            return num

        # 1.4 node has left and right child
        else:
            successor = self.getSucsessor(node)
            node.setValue(successor.getValue())
            ## successor is a leaf
            if successor.getSize() == 0:
                self.deleteLeaf(successor)
                num = self.rebalanceTreeDelete(successor.getParent())
                return num

            #successor has only right child
            else:
                temp = successor.getRight()
                self.deleteNodeWithOnlyRightChild(successor)
                # rebalance tree
                num = self.rebalanceTreeDelete(temp)
                return num


    def deleteLeaf(self, node):
        if self.root == node:
            self.root = None
        else:
            node.setValue(None)
            node.setLeft(None)
            node.setRight(None)
            node.setHeight(-1)
            node.setSize(0)


    def deleteNodeWithOnlyRightChild(self, node):
        # case 1: if node is root
        if node == self.root:
            node.getRight().setParent(None)
            self.root = node.getRight()
        # case 2: connect node right child to node parent
        else:
            if self.is_node_left_child(node):
                node.getParent().setLeft(node.getRight())
            else:
                node.getParent().setRight(node.getRight())
            # change child's parent pointer
            node.getRight().setParent(node.getParent())
            node.setParent(None)

        node.setRight(None)

    def deleteNodeWithOnlyLeftChild(self, node):
        # case 1: if node is root
        if node == self.root:
            node.getLeft().setParent(None)
            self.root = node.getLeft()
        # case 2: connect node right child to node parent
        else:
            if self.is_node_left_child(node):
                node.getParent().setLeft(node.getLeft())
            else:
                node.getParent().setRight(node.getLeft())
            # change child's parent pointer
            node.getLeft().setParent(node.getParent())
            node.setParent(None)

        node.setLeft(None)


    def rebalanceTreeDelete(self, x):
        rotation_number = 0
        y = x.parent
        while y != None:
            previous_height = y.height
            y.updateHeight()
            y.updateSize()
            bf = y.left.height - y.right.height
            if abs(bf) < 2 and y.height == previous_height:
                break
            elif abs(bf) < 2 and y.height != previous_height:
                y = y.getParent()
            elif abs(bf) == 2:
                rotation_number += self.rotateTreeDelete(y)
                y = y.getParent()
        return rotation_number

    def rotateTreeDelete(self, y):
        rotation_number = 0
        bf = y.left.height - y.right.height
        if bf == -2:
            bf_right = y.right.left.height - y.right.right.height
            if bf_right == -1 or bf_right == 0:
                self.rotateLeft(y)
                rotation_number = 1
            elif bf_right == 1:
                self.rotateRight(y.right)
                self.rotateLeft(y)
                rotation_number = 2
        if bf == 2:
            bf_left = y.left.left.height - y.left.right.height
            if bf_left == -1:
                self.rotateLeft(y.left)
                self.rotateRight(y)
                rotation_number = 2
            elif bf_left == 1 or bf_left == 0:
                self.rotateRight(y)
                rotation_number = 1
        return rotation_number



    """works only when node has parent"""
    def is_node_left_child(self, node):
        if node.getParent().getLeft() == node:
            return True
        else:
            return False


    """returns the value of the first item in the list

    @rtype: str
    @returns: the value of the first item, None if the list is empty
    """

    def first(self):
        if self.empty():
            return None
        x = self.root
        while x.left != None:
            x = x.left
        return x.value

    """returns the value of the last item in the list

    @rtype: str
    @returns: the value of the last item, None if the list is empty
    """

    def last(self):
        if self.empty():
            return None
        x = self.root
        while x.right != None:
            x = x.right
        return x.value

    """returns an array representing list 

    @rtype: list
    @returns: a list of strings representing the data structure
    """

    def listToArray(self):
        x = self.root

        def rec_listToArray(x):
            if x == None:
                return []
            return rec_listToArray(x.left) + [x.value] + rec_listToArray(x.right)

        return rec_listToArray(x)

    """returns the size of the list 

    @rtype: int
    @returns: the size of the list
    """

    def length(self):
        return self.size

    """sort the info values of the list

    @rtype: list
    @returns: an AVLTreeList where the values are sorted by the info of the original list.
    """

    def sort(self):
        "//TODO fix this"
        l = self.listToArray().copy()
        return l.sort()

    """permute the info values of the list 

    @rtype: list
    @returns: an AVLTreeList where the values are permuted randomly by the info of the original list. ##Use Randomness
    """

    def permutation(self):
        l = self.listToArray().copy()

        random.shuffle(l)
        return

    """concatenates lst to self

    @type lst: AVLTreeList
    @param lst: a list to be concatenated after self
    @rtype: int
    @returns: the absolute value of the difference between the height of the AVL trees joined
    """

    def concat(self, lst):
        return None

    """searches for a *value* in the list

    @type val: str
    @param val: a value to be searched
    @rtype: int
    @returns: the first index that contains val, -1 if not found.
    """

    def search(self, val):
        return None

    """returns the root of the tree representing the list

    @rtype: AVLNode
    @returns: the root, None if the list is empty
    """

    def getRoot(self):
        return None




