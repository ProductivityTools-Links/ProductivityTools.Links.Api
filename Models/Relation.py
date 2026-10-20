from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
import logging


class Relation():
    def __init__(self,uri,user,password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def create(self, parentId, childId):
        parent_id = int(parentId)
        child_id = int(childId)
        if parent_id == child_id:
            raise ValueError("Cannot create relation from a node to itself")
        with self.driver.session(database="neo4j") as session:
            result = session.execute_write(
                self._create_relation, parent_id, child_id
            )

            for row in result:
                return row

    def move(self, parentId, childId):
        parent_id = int(parentId)
        child_id = int(childId)
        if parent_id == child_id:
            raise ValueError("Cannot move node into itself")
        with self.driver.session(database="neo4j") as session:
            result = session.execute_write(
                self._move_relation, parent_id, child_id
            )

            for row in result:
                return row
        return None

    def remove(self, id):
        with self.driver.session(database="neo4j") as session:
            result = session.execute_write(
                self._remove_parent_relation, int(id)
            )

    def close(self):
        self.driver.close()

    @staticmethod
    def _create_relation(tx, parentId, childId):
        query = (
            "match (m),(n) where id(m)=$parentId and id(n)=$childId and id(m)<>id(n) Create (m)-[r:CHILD]->(n) return type(r) as type"
        )
        result = tx.run(query, parentId=int(parentId), childId=int(childId))
        try:
            return [row["type"] for row in result]
            # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    @staticmethod
    def _move_relation(tx, parentId, childId):
        query = (
            "MATCH (m), (n) "
            "WHERE id(m) = $parentId AND id(n) = $childId "
            "AND id(m) <> id(n) "
            "AND (m:account OR m:Node) "
            "AND (n:Node OR n:Link) "
            "AND coalesce(m.deleted, 0) <> 1 "
            "AND coalesce(n.deleted, 0) <> 1 "
            "AND NOT (n)-[:CHILD*1..]->(m) "
            "OPTIONAL MATCH ()-[d:CHILD]->(n) "
            "DELETE d "
            "WITH DISTINCT m, n "
            "CREATE (m)-[r:CHILD]->(n) "
            "RETURN type(r) AS type"
        )
        result = tx.run(query, parentId=int(parentId), childId=int(childId))
        try:
            return [row["type"] for row in result]
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    @staticmethod
    def _remove_parent_relation(tx, id):
        query = (
            "match (n)-[d:CHILD]->(l) where ID(l)=$id  delete d"
        )
        result = tx.run(query, id=int(id))

