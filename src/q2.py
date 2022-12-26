import timeit
import collections
from src.avl_template_new import AVLTreeList
import math
import random

def avltreeinsertion(number):

    avl_tree = AVLTreeList()
    start = timeit.default_timer()
    for i in range(number):
        avl_tree.insert(0, i)
    stop = timeit.default_timer()
    executation_time = stop - start
    # print("total time: " + str(executation_time))
    # print(math.log2(number))
    return executation_time / number

def avltreeinsertionRandomIndex(number):
    t1 = AVLTreeList()
    start = timeit.default_timer()
    for i in range(number):
        random_index = random.randint(0, t1.size)
        t1.insert(random_index, i)
    stop = timeit.default_timer()
    executation_time = stop - start
    # print("total time: " + str(executation_time))
    # print(math.log2(number))
    return executation_time / number

def avltreeinsertionLast(number):
    t1 = AVLTreeList()
    start = timeit.default_timer()
    for i in range(number):
        t1.insert(t1.size, i)
    stop = timeit.default_timer()
    executation_time = stop - start
    # print("total time: " + str(executation_time))
    # print(math.log2(number))
    return executation_time / number


def linkedlistInsertion(number):
    linked_list = collections.deque()
    start = timeit.default_timer()
    for i in range(number):
        linked_list.appendleft(i)
    stop = timeit.default_timer()
    executation_time = stop - start
    # print("total time: " + str(executation_time))
    return executation_time / number

def linkedlistInsertionRandomIndex(number):
    linked_list = collections.deque()
    start = timeit.default_timer()
    for i in range(number):
        random_index = random.randint(0, i)
        linked_list.insert(random_index, i)
    stop = timeit.default_timer()
    executation_time = stop - start
    # print("total time: " + str(executation_time))
    return executation_time / number

def linkedlistInsertionLast(number):
    linked_list = collections.deque()
    start = timeit.default_timer()
    for i in range(number):
        linked_list.append(i)
    stop = timeit.default_timer()
    executation_time = stop - start
    # print("total time: " + str(executation_time))
    return executation_time / number


def ListInsertionFirst(number):
    lst = []
    start = timeit.default_timer()
    for i in range(number):
        lst.insert(0, i)
    stop = timeit.default_timer()
    executation_time = stop - start
    # print("total time: " + str(executation_time))
    return executation_time / number

def ListInsertionLast(number):
    lst = []
    start = timeit.default_timer()
    for i in range(number):
        lst.append(i)
    stop = timeit.default_timer()
    executation_time = stop - start
    # print("total time: " + str(executation_time))
    return executation_time / number

def ListInsertionRandomIndex(number):
    lst = []
    start = timeit.default_timer()
    for i in range(number):
        random_index = random.randint(0, len(lst))
        lst.insert(random_index, i)

    stop = timeit.default_timer()
    executation_time = stop - start
    # print("total time: " + str(executation_time))
    return executation_time / number





def printing():
    print("array insert first")
    for i in range(1,11):
        print(ListInsertionFirst(i*1500))

printing()
# print(ListInsertionRandomIndex(1500*(2**1)))
# print(ListInsertionRandomIndex(1500*(2**2)))
# print(ListInsertionRandomIndex(1500*(2**3)))
# print(ListInsertionRandomIndex(1500*(2**4)))
# print(ListInsertionRandomIndex(1500*(2**5)))
# print(ListInsertionRandomIndex(1500*(2**6)))
# print(ListInsertionRandomIndex(1500*(2**7)))
# print(ListInsertionRandomIndex(1500*(2**8)))
# print(ListInsertionRandomIndex(1500*(2**9)))
# print(ListInsertionRandomIndex(1500*(2**10)))
# print(updatedListInsertionRandomIndex(1500*(2**1)))
# print(updatedListInsertionRandomIndex(1500*(2**2)))
# print(updatedListInsertionRandomIndex(1500*(2**3)))
# print(updatedListInsertionRandomIndex(1500*(2**4)))
# print(updatedListInsertionRandomIndex(1500*(2**5)))
# print(updatedListInsertionRandomIndex(1500*(2**6)))
# print(updatedListInsertionRandomIndex(1500*(2**7)))
# print(updatedListInsertionRandomIndex(1500*(2**8)))
# print(updatedListInsertionRandomIndex(1500*(2**9)))
# print(updatedListInsertionRandomIndex(1500*(2**10)))


