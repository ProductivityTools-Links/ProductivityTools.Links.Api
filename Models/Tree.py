from neo4j import  GraphDatabase
from DTO.Account import Account
from DTO.Node import Node

class Tree():
    def __init__(self, uri, user, password):
        self.driver=GraphDatabase.driver(uri,auth=(user,password))
    # def getTree(self, login):
    #     with self.driver.session(database="neo4j") as session:
    #         result=session.read_transaction(self._get_tree, login)
    #         return result;
    #
    # @staticmethod
    # def _get_tree(tx, login):
    #     account=Tree._get_account(tx,login)
    #
    #     query=(
    #             'MATCH(a:account{login:$login})-[k:CHILD *]->(n:Node) return id(n) as idn, n, id(a) as ida, a, k'
    #     )
    #     #read the account information
    #     #read the nodes what is done and start creating a tree
    #     result=tx.run(query,login=login)
    #     lastNodeAdded=None
    #     for element in result:
    #         parent=Tree._find_parent(element)
    #         node=Node(element[0],parent,element[1]._properties['name'])
    #
    #         if lastNodeAdded is not None and parent==lastNodeAdded.id:
    #             lastNodeAdded.add_sub_node(node)
    #             lastNodeAdded = node
    #         else:
    #             account.add_node(node)
    #             lastNodeAdded = node
    #
    #         print(element[0])
    #         print(element[1]._properties['name'])
    #         print('is a child of')
    #         print(element[2])
    #         print(element)
    #     return account;
    #    # return [{"id":row["k"][0].id,type:row["k"][0].type, "nodes":row["k"][0].nodes } for row in result]
    #     #return [{"node":{"id": row["idn"] ,"name":row["n"]["name"]}, "account":{ "id": row["ida"] ,"name":row["a"]["login"]},"relation":{"r":row["k"]}} for row in result]
    #
    # def _find_parent(element):
    #     for relation in element[4]:
    #         if(relation.nodes[1].id==element[0]):
    #             parent=relation.nodes[0].id
    #             print (parent)
    #             return parent

    @staticmethod
    def _get_account(tx, login):
        query=(
            "match (a:account {login:'pwujczyk1'}) return a"
        )
        tempresult=tx.run(query,login=login);
        result=tempresult.single()[0]
        account=Account(result.id,result._properties['login'])
        return account


    def close(self):
        self.driver.close()
