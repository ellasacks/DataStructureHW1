# username - ellas3
# id1      - 207332727
# name1    - dor ivanir
# id2      - 206446007
# name2    - ella sacks
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

    """returns the size

      @rtype: int
      @returns: the size of self, 0 if the node is virtual
      """
    def getSize(self):
        return self.size

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

    """sets the size of the node

    @type h: int
    @param size: the size
    """
    def setSize(self, size):
        self.size = size

    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """
    def isRealNode(self):
        return self.height != -1

    """calculates the size of the node based on the size of his real sons

    """
    def updateSize(self):
        size = 1
        if self.right.isRealNode():
            size += self.right.getSize()
        if self.left.isRealNode():
            size += self.left.getSize()
        self.size = size

    """calculates the height of the node based on the height of his sons

    """
    def updateHeight(self):
        '''//TODO Update only on real nodes'''
        self.height = max(self.right.getHeight(), self.left.getHeight()) + 1


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
        self.firstItem = None
        self.lastItem = None

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
        if i < 0 or i >= self.size:
            return None
        return self.treeSelect(i).getValue()

    def treeSelect(self, i):
        def treeSelect_rec(node, k):
            rank = node.getLeft().getSize() + 1
            if k == rank:
                return node
            elif k < rank:
                return treeSelect_rec(node.getLeft(), k)
            else:
                return treeSelect_rec(node.getRight(), k - rank)

        return treeSelect_rec(self.root, i + 1)

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
        # 1. create a new node with virtual sons, his size = 1, height = 0.
        new_node = AVLNode(val)
        new_node.setLeft(AVLNode())
        new_node.setRight(AVLNode())
        new_node.right.setParent(new_node)
        new_node.left.setParent(new_node)
        new_node.updateHeight()
        new_node.updateSize()

        # 2. connect new node to tree:

        ##case1: tree is empty
        if self.empty():
            self.root = new_node
            self.lastItem = new_node
            self.firstItem = new_node

        ##case2: insert at the end of the list
        elif i == self.size:
            node = self.lastItem
            new_node.setParent(node)
            node.setRight(new_node)
            self.lastItem = new_node

        ##case3: insert elsewhere
        else:
            node = self.treeSelect(i)
            if not node.getLeft().isRealNode():
                node.setLeft(new_node)
                new_node.setParent(node)
            else:
                node_predesessor = self.getPredesessor(node)
                node_predesessor.setRight(new_node)
                new_node.setParent(node_predesessor)

        # 3. maintain tree fields: (root is maintained in the rotation funcs)
        if i == 0:
            self.firstItem = new_node
        self.size += 1

        # 4. rebalance tree:
        rotation_number = self.rebalanceTreeAfterInsert(new_node)

        # 5. update nodes size from inserted node to the root
        self.updateFromNodeToRoot(new_node)

        return rotation_number

    """updates the size and height of nodes in the route from node to tree root.

    @type node: AVLNode
    @param node: The node we want to start travel from
    """
    def updateFromNodeToRoot(self, node):
        while node != None:
            node.updateHeight()
            node.updateSize()
            node = node.getParent()

    """help method fpr Insert: AVL rebalancing after insertion of a new node to tree
    
    @pre: x is the new node inserted to tree
    @type x: AVLNode
    @param x: the node we start rebalancing tree from, the new node inserted
    @returns: the number of rebalancing operation due to AVL rebalancing
    """
    def rebalanceTreeAfterInsert(self, x):
        rotation_number = 0
        y = x.getParent()
        while y != None:
            previous_height = y.getHeight()
            y.updateHeight()
            y.updateSize()
            y_bf = y.left.getHeight() - y.right.getHeight()     ##calc balance factor of node y
            if abs(y_bf) < 2 and y.getHeight() == previous_height:
                break
            elif abs(y_bf) < 2 and y.getHeight() != previous_height:
                y = y.getParent()
            elif abs(y_bf) == 2:
                rotation_number = self.rotateTreeInsert(y, y_bf)  ##preform rotaions on y
                break         ##insert algo: we can stop after fixing the first bf violator. tree is balanced.
        return rotation_number

    """help method for rebalanceTreeAfterInsert:
     preforms rotations on node y to fix his balance factor and rebalence tree
    
    @pre: abs(bf) == 2
    @type y: AVLNode
    @type bf_y: int
    @param y: node with balance factor 2 or -2
    @param y_bf: balance factor of node y, is 2 or -2.
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    """
    def rotateTreeInsert(self, y, y_bf):
        rotation_number = 0
        if y_bf == -2:
            bf_of_right_child = y.right.left.getHeight() - y.right.right.getHeight()
            if bf_of_right_child == -1:
                self.rotateLeft(y)
                rotation_number = 1
            elif bf_of_right_child == 1:
                self.rotateRight(y.right)
                self.rotateLeft(y)
                rotation_number = 2
        if y_bf == 2:
            bf_pf_left_child = y.left.left.getHeight() - y.left.right.getHeight()
            if bf_pf_left_child == -1:
                self.rotateLeft(y.left)
                self.rotateRight(y)
                rotation_number = 2
            elif bf_pf_left_child == 1:
                self.rotateRight(y)
                rotation_number = 1

        return rotation_number

    """help method for rotateTreeInsert:
     rotates AVLNode y and his right son in left direction 
    
    @pre: y has real right child
    @type y: AVLNode
    """
    def rotateLeft(self, y):
        # 1. preform rotation: change pointers
        B = y
        A = y.getRight()
        B.setRight(A.left)
        B.right.setParent(B)
        A.setLeft(B)
        A.setParent(B.getParent())
        ##B is not the root of the tree:
        if B.getParent() != None:
            if self.is_node_left_child(B):
                A.getParent().setLeft(A)
            else:
                A.getParent().setRight(A)
        ##B is root: after rotation the new root is A
        else:
            self.root = A
        B.setParent(A)
        # 2. update height and size only for nodes A and B
        B.updateHeight()
        A.updateHeight()
        B.updateSize()
        A.updateSize()

    """help method for rotateTreeInsert:
     rotates AVLNode y and his left son in right direction 
    
    @pre: y has real left child
    @type y: AVLNode
    """
    def rotateRight(self, y):
        # 1. preform rotation: change pointers
        B = y
        A = y.getLeft()
        B.setLeft(A.getRight())
        B.left.setParent(B)
        A.setRight(B)
        A.setParent(B.getParent())
        ##B is not the root of the tree:
        if B.getParent() != None:
            if self.is_node_left_child(B):
                A.getParent().setLeft(A)
            else:
                A.getParent().setRight(A)
        ##B is root: after rotation the new root is A
        else:
            self.root = A
        B.setParent(A)
        # 2. update height and size only for nodes A and B
        B.updateHeight()
        A.updateHeight()
        B.updateSize()
        A.updateSize()


    """returns  the AVLNode who is the predesessor of AVLNode x

    @type x: AVLNode
    @param x: node we want to return his predesessor
    @rtype: AVLNode
    @returns: the predesessor node of x, None if x does not have predesessor. 
    """
    def getPredesessor(self, x):
        if x == self.firstItem: ##if x does not have predesessor return None
            return None
        if x.getLeft().isRealNode():
            return self.right_travel(x.getLeft())
        y = x.getParent()
        while y != None and x == y.getLeft():
            x = y
            y = x.getParent()
        return y

    """returns  the AVLNode who is the sucsessor of AVLNode x

    @type x: AVLNode
    @param x: node we want to return his sucsessor
    @rtype: AVLNode
    @returns: the sucsessor node of x, None if x does not have sucsessor. 
    """
    def getSucsessor(self, x):
        if x == self.lastItem: ##if x does not have sucsessor return None
            return None
        if x.getRight().isRealNode():
            return self.left_travel(x.getRight())
        y = x.getParent()
        while y != None and x == y.getRight():
            x = y
            y = x.getParent()
        return y

    """help method: travel left from node x. stop when getting to node with no left child and return it. 

    @type x: AVLNode
    @param x: node start traveling from
    @rtype: AVLNode
    """
    def left_travel(self, x):
        '''@returns the most left node in a tree'''
        while x.getLeft().isRealNode():
            x = x.getLeft()
        return x

    """help method: travel right from node x. stop when getting to node with no right child and return it. 

    @type x: AVLNode
    @param x: node start traveling from
    @rtype: AVLNode
    """
    def right_travel(self, x):
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
        if i < 0:
            return -1

        node = self.treeSelect(i)   # find node to delete
        self.size -= 1    # maintain tree size

        ## case1: node is leaf
        if node.getSize() == 1:
            self.deleteLeaf(node)
            num = self.rebalanceTreeAfterDelete(node)

        # case2: node has only left child
        elif node.getLeft().isRealNode() and not node.getRight().isRealNode():
            temp = node.getLeft()
            self.deleteNodeWithOnlyLeftChild(node)
            # rebalance tree:
            num = self.rebalanceTreeAfterDelete(temp)

        # case3: node has only right child
        elif not node.getLeft().isRealNode() and node.getRight().isRealNode:
            temp = node.getRight()
            self.deleteNodeWithOnlyRightChild(node)
            # rebalance tree:
            num = self.rebalanceTreeAfterDelete(temp)

        # case4: node has both left and right child
        else:
            successor = self.getSucsessor(node)
            node.setValue(successor.getValue())
            ## successor is a leaf
            if successor.getSize() == 0:
                self.deleteLeaf(successor)
                num = self.rebalanceTreeAfterDelete(successor)

            #successor has only right child
            else:
                temp = successor.getRight()
                self.deleteNodeWithOnlyRightChild(successor)
                # rebalance tree
                num = self.rebalanceTreeAfterDelete(temp)

        # maintain tree fields (root is maintained in deletion help funcs):
        if self.size == 0:
            self.firstItem = None
            self.lastItem = None
        else:
            self.firstItem = self.left_travel(self.root)
            self.lastItem = self.right_travel(self.root)

        return num

    """help method for Delete: remove node from tree when node is leaf

    @type node: AVLNode
    @pre: node.getSize() == 1   ##node is leaf
    @param node: The node to delete from tree
    """
    def deleteLeaf(self, node):
        if self.root == node:
            self.root = None
        else:
            node.setValue(None)
            node.setLeft(None)
            node.setRight(None)
            node.setHeight(-1)
            node.setSize(0)

    """help method for Delete: remove node from tree when node had only right child

    @type node: AVLNode
    @pre: node.getRight().isRealNode() and not node.getleft().isRealNode():
    @param node: The node to delete from tree
    """
    def deleteNodeWithOnlyRightChild(self, node):
        if node == self.root: #if node is tree root
            node.getRight().setParent(None)
            self.root = node.getRight()

        else:
            # connect node right child to node parent:
            if self.is_node_left_child(node):
                node.getParent().setLeft(node.getRight())
            else:
                node.getParent().setRight(node.getRight())

            node.getRight().setParent(node.getParent()) # change node child's parent pointer
            node.setParent(None)

        node.setRight(None)

    """help method for Delete: remove node from tree when node had only left child

    @type node: AVLNode
    @pre: node.getLeft().isRealNode() and not node.getRight().isRealNode():
    @param node: The node to delete from tree
    """
    def deleteNodeWithOnlyLeftChild(self, node):
        if node == self.root:  #if node is tree root
            node.getLeft().setParent(None)
            self.root = node.getLeft()

        else:
            # connect node right child to node parent:
            if self.is_node_left_child(node):
                node.getParent().setLeft(node.getLeft())
            else:
                node.getParent().setRight(node.getLeft())

            node.getLeft().setParent(node.getParent()) # change node child's parent pointer
            node.setParent(None)

        node.setLeft(None)

    """help method for Delete: AVL rebalancing after deletion of a tree node

    @type x: AVLNode
    @param x: the node we start rebalancing tree from
    @returns: the number of rebalancing operation due to AVL rebalancing
    """
    def rebalanceTreeAfterDelete(self, x):
        rotation_number = 0
        y = x.getParent()
        while y != None:                     ##travel from node to root
            previous_height = y.height
            y.updateHeight()                 ##update node fields when visiting node - important for O(log(n))
            y.updateSize()
            y_bf = y.left.getHeight() - y.right.getHeight()       ##calc node balance factor
            if abs(y_bf) < 2 and y.getHeight() == previous_height:
                y = y.getParent()
            elif abs(y_bf) < 2 and y.getHeight() != previous_height:
                y = y.getParent()
            elif abs(y_bf) == 2:
                rotation_number += self.rotateTreeDelete(y, y_bf)
                y = y.getParent()

        return rotation_number

    """help method for rebalanceTreeAfterDelete:
     preforms rotations on node y to fix his balance factor and rebalence tree

    @pre: abs(y_bf) == 2
    @type y: AVLNode
    @type bf_y: int
    @param y: node with balance factor 2 or -2
    @param y_bf: balance factor of node y, is 2 or -2.
    @rtype: int
    @returns: the number of rotation operation due to AVL rebalancing
    """
    def rotateTreeDelete(self, y, y_bf):
        rotation_number = 0
        if y_bf == -2:
            bf_right = y.right.left.getHeight() - y.right.right.getHeight()
            if bf_right == -1 or bf_right == 0:
                self.rotateLeft(y)
                rotation_number = 1
            elif bf_right == 1:
                self.rotateRight(y.right)
                self.rotateLeft(y)
                rotation_number = 2
        if y_bf == 2:
            bf_left = y.left.left.getHeight() - y.left.right.getHeight()
            if bf_left == -1:
                self.rotateLeft(y.left)
                self.rotateRight(y)
                rotation_number = 2
            elif bf_left == 1 or bf_left == 0:
                self.rotateRight(y)
                rotation_number = 1
        return rotation_number

    """help method, returns true if node is the left child of his parent
       
      @pre: node.getParent() != None
      @type y: AVLNode
      @rtype: boolean
      @returns: true if node is left child of his parent 
      """
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
        return self.firstItem.getValue()


    """returns the value of the last item in the list

    @rtype: str
    @returns: the value of the last item, None if the list is empty
    """

    def last(self):
        if self.empty():
            return None
        return self.lastItem.getValue()

    """returns an array representing list 

    @rtype: list
    @returns: a list of strings representing the data structure
    """
    def listToArray(self):
        lst = []
        if self.empty():
            return lst
        ## add values to lst by doing n sucsessor operations from firstItem:
        min_node = self.firstItem
        for i in range(self.root.size):
            lst.append(min_node.getValue())
            min_node = self.getSucsessor(min_node)
        return lst

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
        array = self.listToArray()
        none_lst = []
        value_lst = []
        for value in array:
            if value == None:
                none_lst.append(value)
            else:
                value_lst.append(value)
        sorted_array = self.quicksort(value_lst)
        return self.create_tree_from_array(sorted_array + none_lst)

    """Sorts array by the quicksort algorithm 
    
    @type lst: list
    @rtype: list
    @returns: sorted list
    """
    def quicksort(self, lst):
        """ quick sort of lst """
        if len(lst) <= 1:
            return lst
        else:
            pivot = lst[0]  # for a deterministic quicksort
            smaller = [elem for elem in lst if elem < pivot]
            equal = [elem for elem in lst if elem == pivot]
            greater = [elem for elem in lst if elem > pivot]
            return self.quicksort(smaller) + equal + self.quicksort(greater)

    """help method for Sort. creates AVLTreeList from list

          @type array: list
          @rtype: AVLTreeList
          @returns: AVLTreeList that matches list
          """
    def create_tree_from_array(self, array):
        if len(array) == 0:
            return AVLTreeList()
        root_node = self.rec_create_tree_from_array(0, len(array)-1, array)
        ## Create AVLTreeList from root_node tree
        tree = AVLTreeList()
        tree.size = root_node.getSize()
        tree.root = root_node
        tree.firstItem = tree.left_travel(tree.root)
        tree.lastItem = tree.right_travel(tree.root)
        return tree

    """rec func for create_tree_from_array. creates recursively a AVL tree

          @type array: list
          @type left: int
          @type right: int
          @rtype: AVLNode
          @returns: AVLNode root representing AVL tree that matches list 
          """
    def rec_create_tree_from_array(self, left, right, array):
        if left > right:
            # return a leaf with virtual node
            virtualNode = AVLNode()
            return virtualNode
        mid = (left + right) // 2
        mid_node = AVLNode(array[mid])

        left_sub_tree = self.rec_create_tree_from_array(left, mid - 1, array)
        right_sub_tree = self.rec_create_tree_from_array(mid + 1, right, array)

        mid_node.setLeft(left_sub_tree)
        mid_node.setRight(right_sub_tree)
        left_sub_tree.setParent(mid_node)
        right_sub_tree.setParent(mid_node)
        mid_node.updateHeight()
        mid_node.updateSize()
        return mid_node

    """permute the info values of the list 

    @rtype: list
    @returns: an AVLTreeList where the values are permuted randomly by the info of the original list. ##Use Randomness
    """
    def permutation(self):
        array = self.listToArray()
        shuffled_array = self.shuffle_list(array)
        return self.create_tree_from_array(shuffled_array)

    """help func for permutation. shuffles lst by the Fisher-Yates algorithm

    @rtype: list
    @returns: random permutation of lst
    """
    def shuffle_list(self, lst):
        lst_len = len(lst)
        for i in range(lst_len-1, 0, -1):
            rand_index = random.randint(0, i+1)
            lst[i], lst[rand_index] = lst[rand_index], lst[i]
        return lst

    """concatenates lst to self

    @type lst: AVLTreeList
    @param lst: a list to be concatenated after self
    @rtype: int
    @returns: the absolute value of the difference between the height of the AVL trees joined
    """

    def concat(self, lst):
        #1. edge cases for empty lists:
        if self.empty() or lst.empty():
            if self.empty() and lst.empty():
                return 0
            elif self.empty() and not lst.empty():
                # turn self to lst:
                self.root = lst.root
                self.firstItem = lst.firstItem
                self.lastItem = lst.lastItem
                self.size = lst.size
                return abs(-1 - lst.root.getHeight())
            else:
                return abs(self.root.getHeight() - (-1))
        # 2. edge cases for tree with only one node: use insert:
        elif self.size == 1 or lst.size == 1:
            self_height_origin = self.root.getHeight()
            lst_height_origin = lst.root.getHeight()
            if lst.size == 1:
                self.insert(self.size, lst.root.value)
            else:
                lst.insert(0, self.root.value)
                #turn self to lst:
                self.root = lst.root
                self.firstItem = lst.firstItem
                self.lastItem = lst.lastItem
                self.size = lst.size

        # 3. normal concat: concat trees according to height difference:
        else:
            self_height_origin = self.root.getHeight()
            lst_height_origin = lst.root.getHeight()
            if self_height_origin < lst_height_origin:
                self.concat_small_self_to_big_list(lst) #help method
            else:
                self.concat_big_self_to_small_list(lst) #help method

        return abs(self_height_origin - lst_height_origin)

    """concatenates higher self to lower list
        1. delete firstItem of lst
        2. concat lst to self using deleted node value that maintains order: self -> deleted node -> lst
        3. rebalance self

        @type lst: AVLTreeList
        @param lst: a list to be concatenated after self
        """
    def concat_big_self_to_small_list(self, lst):
        deleted_min_node = AVLNode(lst.firstItem.getValue()) #create new node with lst.firstItem value
        lst.delete(0)

        self_node = self.root
        #travel from root down to first node with height <= lst height:
        while self_node.getHeight() > lst.root.getHeight():
            self_node = self_node.getRight()

        #concat trees using deleted_min_node:set pointers:
        deleted_min_node.setRight(lst.root)
        lst.root.setParent(deleted_min_node)
        deleted_min_node.setLeft(self_node)
        deleted_min_node.setParent(self_node.getParent())
        if not self_node == self.root:
            self_node.getParent().setRight(deleted_min_node)
        else:
            self.root = deleted_min_node
        self_node.setParent(deleted_min_node)

        #update tree fields:
        self.lastItem = lst.lastItem
        self.size += lst.size + 1

        #rebalance tree
        deleted_min_node.updateHeight()
        deleted_min_node.updateSize()
        self.rebalanceTreeAfterDelete(deleted_min_node)

    """concatenates higher list to lower self
        1. delete lastItem of self
        2. concat lst to self using deleted node value that maintains order: self -> deleted node -> lst
        3. rebalance self

        @type lst: AVLTreeList
        @param lst: a list to be concatenated after self
        """
    def concat_small_self_to_big_list(self, lst):
        deleted_max_node = AVLNode(self.lastItem.getValue()) #create new node with lst.firstItem value
        self.delete(self.size - 1)

        lst_node = lst.root
        # travel from root down to first node with height <= self height:
        while lst_node.getHeight() > self.root.getHeight():
            lst_node = lst_node.getLeft()

        # concat trees using deleted_min_node:set pointers:
        deleted_max_node.setLeft(self.root)
        self.root.setParent(deleted_max_node)
        deleted_max_node.setRight(lst_node)
        deleted_max_node.setParent(lst_node.getParent())
        if not lst_node == lst.root:
            lst_node.getParent().setLeft(deleted_max_node)
        else:
            lst.root = deleted_max_node
        lst_node.setParent(deleted_max_node)

        # update tree fields:
        self.root = lst.root
        self.lastItem = lst.lastItem
        self.size += lst.size + 1

        # rebalance tree:
        deleted_max_node.updateHeight()
        deleted_max_node.updateSize()
        self.rebalanceTreeAfterDelete(deleted_max_node)

    """searches for a *value* in the list

    @type val: str
    @param val: a value to be searched
    @rtype: int
    @returns: the first index that contains val, -1 if not found.
    """
    def search(self, val):
        if self.empty():
            return -1
        array = self.listToArray()
        for i in range(len(array)):
            if array[i] == val:
                return i
        return -1


    """returns the root of the tree representing the list

    @rtype: AVLNode
    @returns: the root, None if the list is empty
    """
    def getRoot(self):
        return self.root

    "//TODO deleteeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
    def append(self, val):
        self.insert(self.length(), val)

    def getTreeHeight(self):
        if self.root == None:
            return -1
        return self.root.getHeight()



    def printt(self):
        out = ""
        for row in self.printree(self.root):  # need printree.py file
            out = out + row + "\n"
        print("\t \t \t root: v=" + str(self.root.getValue()) + " H=" + str(self.root.getHeight()) + " S=" + str(self.root.getSize()))
        print(out)

    def printree(self, t, bykey=True):
        # for row in trepr(t, bykey):
        #        print(row)
        return self.trepr(t, False)

    def trepr(self, t, bykey=False):
        if t == None:
            return ["#"]

        thistr = str(t.key) if bykey else "v=" + str(t.getValue()) + " H=" + str(t.getHeight()) + " S=" + str(t.getSize())

        return self.conc(self.trepr(t.left, bykey), thistr, self.trepr(t.right, bykey))

    def conc(self, left, root, right):

        lwid = len(left[-1])
        rwid = len(right[-1])
        rootwid = len(root)

        result = [(lwid+1)*" " + root + (rwid+1)*" "]

        ls = self.leftspace(left[0])
        rs = self.rightspace(right[0])
        result.append(ls*" " + (lwid-ls)*"_" + "/" + rootwid *
                        " " + "\\" + rs*"_" + (rwid-rs)*" ")

        for i in range(max(len(left), len(right))):
            row = ""
            if i < len(left):
                row += left[i]
            else:
                row += lwid*" "

            row += (rootwid+2)*" "

            if i < len(right):
                row += right[i]
            else:
                row += rwid*" "

            result.append(row)

        return result

    def leftspace(self, row):
        # row is the first row of a left node
        # returns the index of where the second whitespace starts
        i = len(row)-1
        while row[i] == " ":
            i -= 1
        return i+1

    def rightspace(self, row):
        # row is the first row of a right node
        # returns the index of where the first whitespace ends
        i = 0
        while row[i] == " ":
            i += 1
        return i


