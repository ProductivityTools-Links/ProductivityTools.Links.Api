# ProductivityTools.Links.Api

## Development

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

GOOGLE_APPLICATION_CREDENTIALS="d:\GitHub\Home.Configuration\ProductivityTools.ProjectsWeb.Firebase.ServiceAccount.json"
GOOGLE_CLOUD_PROJECT=
```

> **Note on Paths**: The `PT.Links.env` file contains Windows paths for local development. In production (Ubuntu), the path for `GOOGLE_APPLICATION_CREDENTIALS` is overridden in the `links-api.service` file to point to the correct Linux location.

GOOGLE_APPLICATION_CREDENTIALS is used for the firebase authentication 

## Production

Application is deployed on an Ubuntu server and managed via systemd. The service configuration is defined in [links-api.service](links-api.service).

The service loads environment variables from `/home/pawel/github/Home.Configuration/PT.Links.env` using the `EnvironmentFile` directive.

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


# Deployment (CI/CD)

Proces wdrożenia jest zautomatyzowany za pomocą **Jenkins**. Każdy push na gałąź `main` uruchamia potok zdefiniowany w `Jenkinsfile`.

### Konfiguracja serwera (Jednorazowa)

Aby Jenkins mógł zarządzać usługą systemową bez interakcji, należy nadać mu odpowiednie uprawnienia `sudo` na serwerze docelowym.

1. Uruchom edytor `visudo`:
   ```bash
   sudo visudo
   ```

2. Dodaj na końcu pliku poniższą linię (pozwala ona Jenkinsowi na restartowanie aplikacji oraz aktualizację definicji usługi):
   ```text
   jenkins ALL=(ALL) NOPASSWD: /usr/bin/systemctl stop links-api, /usr/bin/systemctl start links-api, /usr/bin/systemctl daemon-reload, /usr/bin/systemctl enable links-api, /usr/bin/cp * /etc/systemd/system/links-api.service
   ```

### Debugowanie i Status
Aplikacja jest hostowana przez serwer **Gunicorn** na porcie `5005`. Aby sprawdzić status usługi lub przejrzeć logi bezpośrednio na serwerze, użyj komend:

* **Status usługi:**
  ```bash
  systemctl status links-api
  ```

* **Logi w czasie rzeczywistym:**
  ```bash
  journalctl -u links-api -f
  ```

* **Ręczny restart:**
  ```bash
  sudo systemctl restart links-api
  ```


## Firweall

```
sudo ufw allow 5005/tcp
```