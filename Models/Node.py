from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
import logging


class Node():
    def __init__(self,uri,user,password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def create(self, name):
        with self.driver.session(database="neo4j") as session:
            result=session.write_transaction(
                self._create_node, name
            )

            for row in result:
                return row

    def close(self):
        self.driver.close()

    @staticmethod
    def _create_node(tx,name):
        query=(
            "CREATE (n:Node{name:$name}) RETURN id(n) as id"
        )
        result=tx.run(query,name=name)
        try:
            return [row["id"] for row in result]
            # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise
