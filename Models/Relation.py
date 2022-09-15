from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
import logging


class Relation():
    def __init__(self,uri,user,password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def create(self,parentId, childId):
        with self.driver.session(database="neo4j") as session:
            result=session.write_transaction(
                self._create_relation, parentId, childId
            )

            for row in result:
                return row

    def close(self):
        self.driver.close()

    @staticmethod
    def _create_relation(tx,parentId,childId):
        query=(
            "match (m),(n) where id(m)=$parentId and id(n)=$childId Create (m)-[r:CHILD]->(n) return type(r) as type"
        )
        result=tx.run(query,parentId=parentId,childId=childId)
        try:
            return [row["type"] for row in result]
            # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    @staticmethod
    def _remove_parent_relation(tx,id):
        query=(
            "match (n)-[d:CHILD]->(l:Link) where ID(l)=$id  return d"
        )
        result=tx.run(query,id=id)

