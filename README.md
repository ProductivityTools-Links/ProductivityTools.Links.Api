# ProductivityTools.Links.Api

## Installation

```
pip install -r requirements.txt
python -m flask run
or
$env:PORT=5005; python app.py
```

## Variables

In .vscode directory there is a file launch.json that defines debug properties.

In this file we see path for the environment variables "d:/GitHub/Home.Configuration/Neo4j.env"

In the configuration we have
```
NEO4J_URI=
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=
AURA_INSTANCENAME=

GOOGLE_APPLICATION_CREDENTIALS="d:\GitHub\Home.Configuration\ProductivityTools.Links.ServiceAccountKey.json"
GOOGLE_CLOUD_PROJECT=
```

GOOGLE_APPLICATION_CREDENTIALS is used for the firebase authentication 

### Where it is placed 

Aplication is deployed on the AppEngine in the PTLinksProd project.

### Deployment

I think Cloud build is not working, I can deploy it with the 
```
gcloud app deploy --no-cache
```

I am not providing any env variables but it is working.


## queries

```
match(n:Node)-[k:CHILD*]->(r:Node) where id(n)=1040 return r,n,k
```
Match all childs of given parent


match (a:account) return a

match(a:account)-[k:CHILD*]->(r:Node) return a,k,r

This won't return data if there is no childs (it blocks creating new trees)
match path=(a:account)-[k:CHILD*]->(r:Node)-[m:CHILD*]-(l:Link) with collect(path) as paths call apoc.convert.toTree(paths) YIELD value return value
match path=(a:account)-[k:CHILD*]->(r:Node) OPTIONAL MATCH (r)-[m:CHILD*]->(l:Link) with collect(path) as paths call apoc.convert.toTree(paths) YIELD value return value


This will return also empty items, but without links
match path=(a:account)-[k:CHILD*]->(r:Node) with collect(path) as paths call apoc.convert.toTree(paths) YIELD value return value


match (a:account)-[k:CHILD*]->(r:Node)with collect(path) return a,k,r


match (n:Node)-[k:CHILD]->(r:Node) where id(n)=14 return n,k,r

This returns everything but I do not know how to convert it to json
match (a:account)-[k:CHILD*]->(r:Node) OPTIONAL MATCH (r:Node)-[y:CHILD*]->(z:Link)  return a,k,r,y,z


match path1=(a:account)-[k:CHILD*]->(r:Node) OPTIONAL MATCH path2=(r:Node)-[y:CHILD*]->(z:Link) WITH apoc.path.combine(path1, path2) AS path return path


match path1=(a:account)-[k:CHILD*]->(r:Node) OPTIONAL MATCH path2=(r:Node)-[y:CHILD*]->(z:Link) WITH apoc.path.combine(path1, path2) AS path with collect (path) as paths  call apoc.convert.toTree(paths) YIELD value return value


Select node with child nodes
match (n:Node {name:'Evolution'})-[l:CHILD]->(m:Node) return n,l,m

Remove relationship

match (n:Node {name:'Evolution'})-[l:CHILD]->(m:Node) delete l

match (n:Node {name:'2024.S1'})-[l:CHILD]->(m:Node{name:'Evolution'}) delete l


## Ubuntu deployment

[tutorial](https://www.techrepublic.com/article/how-to-install-neo4j-ubuntu-server/)


```
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install wget curl nano software-properties-common dirmngr apt-transport-https gnupg gnupg2 ca-certificates lsb-release ubuntu-keyring unzip -y
curl -fsSL https://debian.neo4j.com/neotechnology.gpg.key | sudo gpg --dearmor -o /usr/share/keyrings/neo4j.gpg
echo "deb [signed-by=/usr/share/keyrings/neo4j.gpg] https://debian.neo4j.com stable latest" | sudo tee -a /etc/apt/sources.list.d/neo4j.list

sudo apt-get update

sudo apt-get install neo4j -y

```