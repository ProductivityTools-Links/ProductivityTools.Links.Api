class Node:
    def __init__(self,id,parent_id,name):
        self.id=id
        self.parent_id=parent_id
        self.name=name
        self.nodes=[]

    def add_sub_node(self,node):
        print(node.parent_id)