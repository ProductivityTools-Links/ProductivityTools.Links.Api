from neo4j import GraphDatabase

class Account():
    def __init__(self,uri,user,password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def create(self,name):
        with self.driver.session(database="neo4j") as session:
            result=session.write_transaction(
                self._create_account, name
            )

    @staticmethod
    def _create_account(tx,name):
        query=(
            "CREATE (a:Account{name:$name})"
            "RETURN a"
        )
        result=tx.run(query,name=name)
        
    def close(self):
        self.driver.close()