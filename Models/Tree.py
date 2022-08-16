from neo4j import  GraphDatabase

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
        query=(
            'MATCH(a:account{login:$login}) - [k:CHILD *]->(n:Node) return id(n) as idn, n, id(a) as ida, a, k'
        )
        result=tx.run(query,login=login)
        return [{"id":row["k"][0].id,type:row["k"][0].type, "nodes":row["k"][0].nodes } for row in result]
        #return [{"node":{"id": row["idn"] ,"name":row["n"]["name"]}, "account":{ "id": row["ida"] ,"name":row["a"]["login"]},"relation":{"r":row["k"]}} for row in result]




    def close(self):
        self.driver.close()
