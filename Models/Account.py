from neo4j import GraphDatabase
from DTO.Account import Account as DTOAccount
import logging
import sys

class Account():
    def __init__(self,uri,user,password):
        # driver logging
        # handler = logging.StreamHandler(sys.stdout)
        # handler.setLevel(logging.DEBUG)
        # logging.getLogger("neo4j").addHandler(handler)
        # logging.getLogger("neo4j").setLevel(logging.DEBUG)
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def create(self,name):
        with self.driver.session(database="neo4j") as session:
            result=session.write_transaction(
                self._create_account, name
            )
    def checkIfAccountCreated(self,name):
        with self.driver.session(database="neo4j") as session:
            result = session.write_transaction(
                self._checkIfAccountCreated, name
            )
            return result;

    def getList(self):
        with self.driver.session(database="neo4j") as session:
            result = session.write_transaction(
                self._get_account_list
            )
            return result;

    @staticmethod
    def _create_account(tx,name):
        query=(
            "CREATE (a:account{login:$name})"
            "RETURN a"
        )
        tempresult=tx.run(query,name=name)
        result = tempresult.single()[0]


    @staticmethod
    def _checkIfAccountCreated(tx,name):
        query = (
            "match (a:account) where a.login=$name return a"
        )
        result = tx.run(query, name=name)
        print(result)
        if result.peek() is None:
            return False
        else:
            return True

    @staticmethod
    def _get_account_list(tx):
        query = (
            "match (a:account) return a"
        )
        accounts = []
        result = tx.run(query)
        for element in result:
            link = DTOAccount(element[0].id, element[0]._properties['login'])
            accounts.append(link)
        return accounts;

    def close(self):
        self.driver.close()