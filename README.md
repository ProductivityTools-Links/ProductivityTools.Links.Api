# ProductivityTools.Links.Api

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


match path=(a:account)-[k:CHILD*]->(r:Node)with collect(path) as paths call apoc.convert.toTree(paths) YIELD value return value