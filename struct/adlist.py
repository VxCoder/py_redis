# -*- coding: utf-8 -*-
from platform import node


class listIter(object):

    def __init__(self, next, direction):
        self.next = next
        self.direction = direction


class listNode(object):

    def __init__(self, value, prev=None, next=None):
        self.prev = prev
        self.next = next
        self.value = value

    def listPrevNode(self):
        """ 返回给定节点的前置节点 """
        return self.prev

    def listNextNode(self):
        """ 返回给定节点的后置节点 """
        return self.next

    def listNodeValue(self):
        return self.value


class list(object):
    """ 双端链表结构  """

    def __init__(self):
        self.head = None
        self.tail = None
        self.len = 0
        self.match_func = None

    def listLength(self):
        """ 返回给定链表所包含的节点数量 """
        return self.len

    def listFirst(self):
        """ 返回给定链表的表头节点 """
        return self.head

    def listLast(self):
        """ 返回给定链表的表尾节点 """
        return self.tail

    def listSetMatchMethod(self, match_func):
        """ 将链表 l 的值复制函数设置为 m """
        self.match_func = match_func

    def listGetMatchMethod(self):
        """ 返回给定链表的值对比函数 """
        return self.match_func

    def listAddNodeHead(self, value):
        """ 将一个包含有给定值指针 value 的新节点添加到链表的表头 """
        node = listNode(value)

        if self.len == 0:
            self.head = self.tail = node
            node.prev = node.next = None
        else:
            node.prev = None
            node.next = self.head
            self.head.prev = node
            self.head = node

        self.len += 1

        return self

    def listAddNodeTail(self, value):
        """ 将一个包含有给定值指针 value 的新节点添加到链表的表尾  """

        node = listNode(value)

        if self.len == 0:
            self.head = self.tail = node
            node.prev = node.next = None
        else:
            node.prev = self.tail
            node.next = None
            self.tail.next = node
            self.tail = node

        self.len += 1

        return self
