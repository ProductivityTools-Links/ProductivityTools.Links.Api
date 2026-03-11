# ProductivityTools.Links.Api

## Development

But when application is used this way the environemt variables that are in the launch.json are not taken into account, so more env variables is needed to be provided to run application
```
pip install -r requirements.txt
python -m flask run
or
$env:PORT=5005; python app.py
```

### Variables

In .vscode directory there is a file launch.json that defines debug properties.

In this file we see path for the environment variables "d:/GitHub/Home.Configuration/PT.Links.env"

In the configuration we have
```
NEO4J_URI=
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=
AURA_INSTANCENAME=

```
We also need to provide two google env variables directly in the file:
```
GOOGLE_APPLICATION_CREDENTIALS="d:\GitHub\Home.Configuration\ProductivityTools.ProjectsWeb.Firebase.ServiceAccount.json"
GOOGLE_CLOUD_PROJECT=
```
> **Note on Paths**: The `PT.Links.env` file contains Windows paths for local development. In production (Ubuntu), the path for `GOOGLE_APPLICATION_CREDENTIALS` is overridden in the `links-api.service` file to point to the correct Linux location.

GOOGLE_APPLICATION_CREDENTIALS is used for the firebase authentication 

## Production

Application is deployed on an Ubuntu server and managed via systemd. The service configuration is defined in [links-api.service](links-api.service).

The service loads environment variables from `/home/pawel/github/Home.Configuration/PT.Links.env` using the `EnvironmentFile` directive.

# Deployment (CI/CD)

The deployment process is automated using **Jenkins**. Every push to the `main` branch triggers the pipeline defined in `Jenkinsfile`.

### Server Configuration (One-time)

To allow Jenkins to manage the system service without interaction, you need to grant it appropriate `sudo` permissions on the target server.

1. Run the `visudo` editor:
   ```bash
   sudo visudo
   ```

2. Add the following line at the end of the file (this allows Jenkins to restart the application and update the service definition):
   ```text
   jenkins ALL=(ALL) NOPASSWD: /usr/bin/systemctl stop links-api, /usr/bin/systemctl start links-api, /usr/bin/systemctl daemon-reload, /usr/bin/systemctl enable links-api, /usr/bin/cp * /etc/systemd/system/links-api.service
   ```

### Debugging and Status
The application is hosted by the **Gunicorn** server on port `5005`. To check the service status or view logs directly on the server, use the commands:

* **Service Status:**
  ```bash
  systemctl status links-api
  ```

* **Real-time logs:**
  ```bash
  journalctl -u links-api -f
  ```

* **Manual restart:**
  ```bash
  sudo systemctl restart links-api
  ```


### Firewall

```
sudo ufw allow 5005/tcp
```

### Errors that I faced
- [CORS error] Redirect domain to the server
- [CORS error] In the reverse proxy check if the redirection to ubuntu server is correct 
- [A project ID is required to access the auth service.\n 1. Use a service account credential, or\n 2. set the project ID explicitly via Firebase App options, or\n 3. set the project ID via the GOOGLE_CLOUD_PROJECT environment variable] Lanuch.json is not used when running application with ```python -m flask run``` you need to debug it in vscode 

## Queries

```
match(n:Node)-[k:CHILD*]->(r:Node) where id(n)=1040 return r,n,k
```
Match all childs of given parent

```
match (a:account) return a

match(a:account)-[k:CHILD*]->(r:Node) return a,k,r
```
This won't return data if there is no childs (it blocks creating new trees)
```
match path=(a:account)-[k:CHILD*]->(r:Node)-[m:CHILD*]-(l:Link) with collect(path) as paths call apoc.convert.toTree(paths) YIELD value return value
match path=(a:account)-[k:CHILD*]->(r:Node) OPTIONAL MATCH (r)-[m:CHILD*]->(l:Link) with collect(path) as paths call apoc.convert.toTree(paths) YIELD value return value
```

This will return also empty items, but without links
```
match path=(a:account)-[k:CHILD*]->(r:Node) with collect(path) as paths call apoc.convert.toTree(paths) YIELD value return value


match (a:account)-[k:CHILD*]->(r:Node)with collect(path) return a,k,r


match (n:Node)-[k:CHILD]->(r:Node) where id(n)=14 return n,k,r
```

This returns everything but I do not know how to convert it to json
```
match (a:account)-[k:CHILD*]->(r:Node) OPTIONAL MATCH (r:Node)-[y:CHILD*]->(z:Link)  return a,k,r,y,z


match path1=(a:account)-[k:CHILD*]->(r:Node) OPTIONAL MATCH path2=(r:Node)-[y:CHILD*]->(z:Link) WITH apoc.path.combine(path1, path2) AS path return path


match path1=(a:account)-[k:CHILD*]->(r:Node) OPTIONAL MATCH path2=(r:Node)-[y:CHILD*]->(z:Link) WITH apoc.path.combine(path1, path2) AS path with collect (path) as paths  call apoc.convert.toTree(paths) YIELD value return value
```

Select node with child nodes
```
match (n:Node {name:'Evolution'})-[l:CHILD]->(m:Node) return n,l,m
```
Remove relationship
```
match (n:Node {name:'Evolution'})-[l:CHILD]->(m:Node) delete l

match (n:Node {name:'2024.S1'})-[l:CHILD]->(m:Node{name:'Evolution'}) delete l
```

