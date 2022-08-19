class Account:
    def __init__(self,id,login):
        self.id=id;
        self.login=login
        self.nodes=[]

    def add_node(self,node):
        if(node.parent_id==self.id):
            self.nodes.append(node)
        else:
            Account.add_sub_node(self,node);

    def add_sub_node(self,new_node):
        for node in self.nodes:
            if (node.id==new_node.parent_id):
                node.add_sub_node(new_node);

