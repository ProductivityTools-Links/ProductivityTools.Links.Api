from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
import logging
import json

from DTO.Link import Link as DTOLink
from DTO.Account import Account as DTOAccount
from DTO.Node import Node as DTONode



class Links():
    def __init__(self,uri,user,password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def getLinks(self, id):
        with self.driver.session(database="neo4j") as session:
            result = session.read_transaction(self._get_links, id)
            return result;

    def getTreeLinks(self,login):
        with self.driver.session(database="neo4j") as session:
            tree=session.read_transaction(self._get_json_tree,login);
            #account=session.read_transaction(self._get_links_for_account, login)
            return tree


    @staticmethod
    def _get_links_for_account(tx,login):
        account=Links._get_account(tx,login)
        #Links._get_json_tree(tx,login)
        Links._get_account_nodes(tx,account)
        for node in account.nodes:
            Links._process_nodes(tx,node)
        print(account)
        return account

    @staticmethod
    def _get_json_tree(tx,login):
        query = (
            'match path1=(a:account)-[k:CHILD*]->(r:Node) OPTIONAL MATCH path2=(r:Node)-[y:CHILD*]->(z:Link) WITH apoc.path.combine(path1, path2) AS path with collect (path) as paths  call apoc.convert.toTree(paths) YIELD value return value'
        )
        tempresult = tx.run(query, login=login)
        x=tempresult.single()[0]
        #x=json.dumps(tempresult.data())
        #result=tempresult.single()[0]
        #account = DTOAccount(result.id, result._properties['login'])
        return x


    @staticmethod
    def _get_account(tx,login):
        query = (
            'match(a:account{login:$login}) return a'
        )
        tempresult = tx.run(query, login=login)
        result=tempresult.single()[0]
        account = DTOAccount(result.id, result._properties['login'])
        return account

    @staticmethod
    def _get_account_nodes(tx,account):
        query = (
            'match(a:account)-[k:CHILD]->(n:Node) where ID(a)=$id return n'
        )
        result = tx.run(query, id=account.id)
        for node in result:
            newNode=DTONode(node[0].id,account.id,node[0]._properties['name'])
            account.add_node(newNode)
            print(node)



    @staticmethod
    def _process_nodes(tx, node):
        query =(
            'match(n:Node)-[k:CHILD]->(r:Node) where id(n)=$id return r'
        )
        nodes=tx.run(query,id=node.id)
        for childNode in nodes:
            newNode=DTONode(childNode[0].id,node.id,childNode[0]._properties['name'])
            node.add_sub_node(newNode)
            Links._process_nodes(tx,newNode)

        query = (
            'match(n:Node)-[k:CHILD]->(l:Link) where ID(n)=$id return l'
        )
        links = tx.run(query, id=node.id)
        for link in links:
            link = DTOLink(link[0].id, node.id, link[0]._properties['name'],link[0]._properties['description'],link[0]._properties['url'])
            node.add_link(link)

    @staticmethod
    def _get_links(tx,id):
        query = (
            'match (n)-[child*]->(l:Link) where ID(n)=$id return l'
        )
        links=[]
        result = tx.run(query,id=id)
        for element in result:
            link=DTOLink(element[0].id, 0, element[0]._properties['name'],element[0]._properties['description'],element[0]._properties['url'],element[0]._properties['authors'])
            links.append(link)
        return links;

    # return [{"id":row["k"][0].id,type:row["k"][0].type, "nodes":row["k"][0].nodes } for row in result]
    # return [{"node":{"id": row["idn"] ,"name":row["n"]["name"]}, "account":{ "id": row["ida"] ,"name":row["a"]["login"]},"relation":{"r":row["k"]}} for row in result]

    def create(self, name,url,description, authors):
        with self.driver.session(database="neo4j") as session:
            result=session.write_transaction(
                self._create_link, name, url, description, authors
            )

            for row in result:
                return row
    def delete(self, id):
        with self.driver.session(database="neo4j") as session:
            result=session.write_transaction(
                self._remove_link,id                
            )
            return result

    def close(self):
        self.driver.close()

    @staticmethod
    def _remove_link(tx, id):
        query=("MATCH (n) where id(n)=$id DETACH DELETE n")
        result = tx.run(query, id=id);

    @staticmethod
    def _create_link(tx, name,url,description, authors):
        query = (
        "CREATE (n:Link{name:$name,url:$url,description:$description,authors:$authors}) RETURN id(n) as id"
        )
        result = tx.run(query, name=name,url=url,description=description, authors=authors)
        try:
            return [row["id"] for row in result]
            # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
              query=query, exception=exception))
            raise

    def update(self, id, name,url,description, authors):
        with self.driver.session(database="neo4j") as session:
            result=session.write_transaction(
                self._update_link,id, name, url, description, authors
            )

            for row in result:
                return row

    @staticmethod
    def _update_link(tx, id, name, url, description,authors):
        query = (
            "MATCH (l:Link) WHERE id(l)=$id SET l.name=$name, l.description=$description, l.url=$url, l.authors=$authors"
        )
        result = tx.run(query,id=id, name=name, url=url, description=description, authors=authors)
        try:
            return [row["id"] for row in result]
            # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

