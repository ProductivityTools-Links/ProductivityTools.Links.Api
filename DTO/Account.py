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

    def add_sub_node(self,node):
        for element in self.nodes:
            element.add_sub_node(node);

