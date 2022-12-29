class Node:
    def __init__(self,  former, value, next):
        self.former = former
        self.value = value
        self.next = next


class LinkList:
    first = None
    last = None

    def __init__(self, value):
        self.first = Node(None, value,  None)
        self.last = self.first

    def add(self, value):
        self.last.next = Node(self.last, value, None)
        self.last = self.last.next

    def edit(self, value, newValue):
        temp = self.get(value)
        if (temp == False):
            return False
        else:
            temp.value = newValue

    def delete(self, value):
        node = self.get(value)
        if (node == None):
            return None
        else:
            node.former.next = node.next
            node.next.former = node.former

    def get(self, value):
        node = self.first
        while (node != None):
            if (node.value == value):
                return node
            elif (node == None):
                return None
            else:
                node = node.next

    def display(self):
        node = self.first
        while (node != None):
            print(f'{node.former}\t{node.value}\t{node.next}\n')
            node = node.next


# tests
b = LinkList('a')
b.add('b')
b.add('c')
b.add('d')
b.add('e')

b.edit('c','cc')

# b.delete('c')

b.display()



#chap d= F0
#rast b= 50