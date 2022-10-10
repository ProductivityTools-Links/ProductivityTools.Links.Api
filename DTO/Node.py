class Node:
    def __init__(self,id,parent_id,name):
        self.id=id
        self.parent_id=parent_id
        self.name=name
        self.nodes=[]
        self.links=[]

    def add_sub_node(self,node):
        self.nodes.append(node)
        print(node.parent_id)

    def add_link(self,link):
        self.links.append(link)