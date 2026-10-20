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

    def getLinks(self, id, include_archived=False):
        with self.driver.session(database="neo4j") as session:
            result = session.execute_read(self._get_links, int(id), bool(include_archived))
            return result;

    def getTreeLinks(self, login, include_archived=False):
        with self.driver.session(database="neo4j") as session:
            tree=session.execute_read(self._get_json_tree, login, bool(include_archived));
            #account=session.execute_read(self._get_links_for_account, login)
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
    def _normalize_tree(node):
        if not isinstance(node, dict):
            return node
        if node.get("_type") == "Node":
            raw_archived = node.get("archived", False)
            node["archived"] = bool(raw_archived) if raw_archived not in ("false", "False", "0", 0, None) else False
        children = node.get("child")
        if isinstance(children, list):
            for child in children:
                Links._normalize_tree(child)
        return node

    @staticmethod
    def _get_json_tree(tx, login, include_archived=False):
        if include_archived:
            query = (
                "MATCH path = (a:account {login: $login})-[:CHILD*]->(target) "
                "WHERE ALL(n IN nodes(path) WHERE coalesce(n.deleted, 0) <> 1) "
                "WITH collect(path) AS paths "
                "CALL apoc.convert.toTree(paths) YIELD value "
                "RETURN value"
            )
        else:
            query = (
                "MATCH path = (a:account {login: $login})-[:CHILD*]->(target) "
                "WHERE ALL(n IN nodes(path) WHERE coalesce(n.deleted, 0) <> 1 AND coalesce(n.archived, false) <> true) "
                "WITH collect(path) AS paths "
                "CALL apoc.convert.toTree(paths) YIELD value "
                "RETURN value"
            )
        tempresult = tx.run(query, login=login)
        record = tempresult.single()
        if not record or not record[0] or "_id" not in record[0]:
            account_record = tx.run("MATCH (a:account {login: $login}) RETURN a", login=login).single()
            if account_record:
                acc = account_record[0]
                return {"_id": acc.id, "_type": "account", "login": acc["login"], "child": []}
            return {}
        x = record[0]
        if isinstance(x, dict):
            if "child" not in x:
                x["child"] = []
            Links._normalize_tree(x)
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
            props = node[0]._properties
            newNode=DTONode(node[0].id,account.id,props.get('name'),bool(props.get('archived', False)))
            account.add_node(newNode)
            print(node)



    @staticmethod
    def _process_nodes(tx, node):
        query =(
            'match(n:Node)-[k:CHILD]->(r:Node) where id(n)=$id return r'
        )
        nodes=tx.run(query,id=node.id)
        for childNode in nodes:
            props = childNode[0]._properties
            newNode=DTONode(childNode[0].id,node.id,props.get('name'),bool(props.get('archived', False)))
            node.add_sub_node(newNode)
            Links._process_nodes(tx,newNode)

        query = (
            'match(n:Node)-[k:CHILD]->(l:Link) where ID(n)=$id return l'
        )
        links = tx.run(query, id=node.id)
        for link in links:
            props = link[0]._properties
            link = DTOLink(link[0].id, node.id, props.get('name'),props.get('description'),props.get('url'),props.get('authors'))
            node.add_link(link)

    @staticmethod
    def _get_links(tx, id, include_archived=False):
        if include_archived:
            query = (
                'match path = (n)-[child*]->(l:Link) '
                'where ID(n)=$id and ALL(x IN nodes(path) WHERE coalesce(x.deleted, 0) <> 1) '
                'return l'
            )
        else:
            query = (
                'match path = (n)-[child*]->(l:Link) '
                'where ID(n)=$id and ALL(x IN nodes(path) WHERE coalesce(x.deleted, 0) <> 1 AND coalesce(x.archived, false) <> true) '
                'return l'
            )
        links=[]
        result = tx.run(query,id=id)
        for element in result:
            props = element[0]._properties
            link=DTOLink(element[0].id, 0, props.get('name'),props.get('description'),props.get('url'),props.get('authors'))
            links.append(link)
        return links;

    # return [{"id":row["k"][0].id,type:row["k"][0].type, "nodes":row["k"][0].nodes } for row in result]
    # return [{"node":{"id": row["idn"] ,"name":row["n"]["name"]}, "account":{ "id": row["ida"] ,"name":row["a"]["login"]},"relation":{"r":row["k"]}} for row in result]

    def create(self, name,url,description, authors):
        with self.driver.session(database="neo4j") as session:
            result=session.execute_write(
                self._create_link, name, url, description, authors
            )

            for row in result:
                return row
    def delete(self, id):
        raise Exception("It should not be called anymore, use setAsDeleted")
        with self.driver.session(database="neo4j") as session:
            result=session.execute_write(
                self._remove_link,id                
            )
            return result
        
    def setAsDeleted(self, id):
        with self.driver.session(database="neo4j") as session:
            result=session.execute_write(
                self._set_as_deleted,id
            )

    def close(self):
        self.driver.close()

    @staticmethod
    def _remove_link(tx, id):
        raise Exception("It should not be called anymore, use _set_as_deleted")
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
            result=session.execute_write(
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
        
    @staticmethod
    def _set_as_deleted(tx,id):
        query=(
            "MATCH (l:Link) where id(l)=$id set l.deleted=1"
        )
        result=tx.run(query,id=id)
        return [row["id"] for row in result]

