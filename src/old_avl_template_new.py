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

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = -1  # Balance factor
        self.size = 1

    """returns the left child
    @rtype: AVLNode
    @returns: the left child of self, None if there is no left child
    """

    def getLeft(self):
        return self.left

    """returns the right child

    @rtype: AVLNode
    @returns: the right child of self, None if there is no right child
    """

    def getRight(self):
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
        return None

    """sets the balance factor of the node

    @type h: int
    @param h: the height
    """

    def setHeight(self, h):
        self.height = h

    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """

    def isRealNode(self):
        return False


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
            rank = x.left.size + 1
            if k == rank:
                return x
            elif k < rank:
                return retrieve_rec(x.left, k)
            else:
                return retrieve_rec(x.right, k - rank)

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
        self.size += 1
        new_node = AVLNode(val)
        new_node.height = 0
        if i == self.size:
            node = self.most_left_node(self.root)
            new_node.parent = node
            node.right = new_node
        else:
            node = self.retrieve(i+1)
            if node.left == None:
                node.left = new_node
                new_node.parent = node
            else:
                node_predesessor = self.getPredesessor(node)
                node_predesessor.right = new_node
                new_node.parent = node_predesessor

        # 2. rebalance tree
        rotation_number = self.rebalanceTree(new_node)
        # 3. update size and height from inserted node to the root
        self.updateFromNodeToRoot(new_node)
        return rotation_number

    def updateFromNodeToRoot(self, x):
        while x.parent != None:
            self.updateHeight(x.parent)
            self.updateSize(x.parent)
            x = x.parent

    def rebalanceTree(self, x):
        rotation_number = 0
        y = x.parent
        while y != None:
            previous_height = y.height
            self.updateHeight(y)
            bf = y.left.height - y.right.height
            if abs(bf) < 2 and y.height == previous_height:
                break
            elif abs(bf) < 2 and y.height != previous_height:
                y = y.parent
            elif abs(bf) == 2:
                rotation_number = self.rotateTree(y)
        return rotation_number


    def rotateTree(self, y):
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
        # *1. change pointers
        B = y
        A = y.right
        B.right = A.left
        B.right.parent = B
        A.left = B
        A.parent = B.parent
        if B.parent != None:
            if B.parent.right == B:
                A.parent.right = A
            else:
                A.parent.left = A
        B.parent = A
        # 2. update height and size only for A and B
        self.updateHeight(B)
        self.updateHeight(A)
        self.updateSize(B)
        self.updateSize(A)

        return None


    def rotateRight(self, y):
        # 1. change pointers
        B = y
        A = y.left
        B.left = A.right
        B.left.parent = B
        A.right = B
        A.parent = B.parent
        if B.parent != None:
            if B.parent.right == B:
                A.parent.right = A
            else:
                A.parent.left = A
        B.parent = A
        # 2. update height and size only for A and B
        self.updateHeight(B)
        self.updateHeight(A)
        self.updateSize(B)
        self.updateSize(A)



        return None



    def getPredesessor(self, x):
        '''//TODO Detrmine what to do when no successorFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF'''
        if x.left != None:
            return self.most_right_node(x.left)
        y = x.parent
        while y != None and x == y.left:
            x = y
            y = x.parent
        return y

    def getSucsessor(self, x):
        '''//TODO Detrmine what to do when no successorFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF '''
        if x.right != None:
            return self.most_left_node(x.right)
        y = x.parent
        while y != None and x == y.right:
            x = y
            y = x.parent
        return y

    def most_left_node(self, x):
        '''@returns the most left node in a tree'''
        while x.left != None:
            x = x.left
        return x

    def most_right_node(self, x):
        '''@returns the most right node in a tree'''
        while x.right != None:
            x = x.right
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
        if node.left == node.right == None:
            if node.parent.right == node:
                node.parent.right = None
            else:
                node.parent.left = None
            node.parent = None
        if node.left != None and node.right == None:
            if node.parent.right == node:
                node.parent.right = node.left
            else:
                node.parent.left = node.left
            node.left.parent = node.parent
            node.parent = None

        return -1

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

    def updateSize(self, x):
        size = 1
        if x.right != None:
            size += x.right.size
        if x.left != None:
            size += x.left.size
        x.size = size

        # while x.parent != None:
        #     x.parent.size += 1
        #     x = x.parent

    def updateHeight(self,x):
        if x.right == None:
            x.height = x.left.height + 1
        elif x.left == None:
            x.height = x.right.height + 1
        else:
            x.height = max(x.right.height, x.left.height) + 1


