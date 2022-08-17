from neo4j import  GraphDatabase
from DTO.Account import Account


class Tree():
    def __init__(self, uri, user, password):
        self.driver=GraphDatabase.driver(uri,auth=(user,password))
    def getTree(self, login):
        with self.driver.session(database="neo4j") as session:
            result=session.read_transaction(self._get_tree, login)
            for row in result:
                print(row)

    @staticmethod
    def _get_tree(tx, login):
        Tree._get_account(tx,login)
        query=(
            'MATCH(a:account{login:$login}) - [k:CHILD *]->(n:Node) return id(n) as idn, n, id(a) as ida, a, k'
        )
        #read the account information
        #read the nodes what is done and start creating a tree
        result=tx.run(query,login=login)
        for element in result:
            print(element[0])
            print(element[1]._properties['name'])
            print('is a child of')
            print(element[2])
            print(element)
        return [{"id":row["k"][0].id,type:row["k"][0].type, "nodes":row["k"][0].nodes } for row in result]
        #return [{"node":{"id": row["idn"] ,"name":row["n"]["name"]}, "account":{ "id": row["ida"] ,"name":row["a"]["login"]},"relation":{"r":row["k"]}} for row in result]

    @staticmethod
    def _get_account(tx, login):
        query=(
            "match (a:account {login:'pwujczyk1'}) return a"
        )
        tempresult=tx.run(query,login=login);
        result=tempresult.single()[0]
        account=Account(result.id,result._properties['login'])

        print(id)


    def close(self):
        self.driver.close()
