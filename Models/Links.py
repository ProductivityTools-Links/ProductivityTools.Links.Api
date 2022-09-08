from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
import logging

from DTO.Link import Link



class Links():
    def __init__(self,uri,user,password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def getLinks(self, id):
        with self.driver.session(database="neo4j") as session:
            result = session.read_transaction(self._get_links, id)
            return result;

    @staticmethod
    def _get_links(tx,id):
        query = (
            'match (n:Node)-[child*]->(l:Link) where ID(n)=$id return l'
        )
        links=[]
        result = tx.run(query,id=id)
        for element in result:
            link=Link(element[0].id, 0, element[0]._properties['name'],element[0]._properties['description'],element[0]._properties['url'])
            links.append(link)
        return links;

    # return [{"id":row["k"][0].id,type:row["k"][0].type, "nodes":row["k"][0].nodes } for row in result]
    # return [{"node":{"id": row["idn"] ,"name":row["n"]["name"]}, "account":{ "id": row["ida"] ,"name":row["a"]["login"]},"relation":{"r":row["k"]}} for row in result]

    def create(self, name,url,description):
        with self.driver.session(database="neo4j") as session:
            result=session.write_transaction(
                self._create_link, name, url, description
            )

            for row in result:
                return row

    def close(self):
        self.driver.close()

    @staticmethod
    def _create_link(tx, name,url,description):
        query = (
        "CREATE (n:Link{name:$name,url:$url,description:$description}) RETURN id(n) as id"
        )
        result = tx.run(query, name=name,url=url,description=description)
        try:
            return [row["id"] for row in result]
            # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
              query=query, exception=exception))
            raise
