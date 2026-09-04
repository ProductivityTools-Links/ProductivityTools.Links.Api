# ProductivityTools.Links.Api

## Development

After installing Python and the Python Debugger extension in VS Code, press **F5** to run and debug the application.

### Variables

In `.vscode/launch.json`, the configuration points to the environment file: `d:/GitHub/Home.Configuration/PT.Links.env`.

The environment file defines:
```ini
NEO4J_URI=
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=
AURA_INSTANCENAME=
```

Google Cloud / Firebase environment variables:
```ini
GOOGLE_APPLICATION_CREDENTIALS="d:\GitHub\Home.Configuration\ProductivityTools.ProjectsWeb.Firebase.ServiceAccount.json"
GOOGLE_CLOUD_PROJECT=
```

> **Note on Paths**: The `PT.Links.env` file contains Windows paths for local development. In production (Ubuntu), the path for `GOOGLE_APPLICATION_CREDENTIALS` is set in the `links-api.service` file to point to the Linux location.

---

## Production

The application is deployed on an Ubuntu server and managed via systemd. The service configuration is defined in [links-api.service](links-api.service).

The service loads environment variables from `/home/pawel/github/Home.Configuration/PT.Links.env` using the `EnvironmentFile` directive.

---

# Deployment (CI/CD)

The deployment process is automated using **GitHub Actions**. Every push to the `main` branch (or manual workflow dispatch) triggers the deployment workflow defined in [.github/workflows/deploy.yml](.github/workflows/deploy.yml).

### Debugging and Status
The application is hosted by the **Gunicorn** server on port `5005`. To check the service status or view logs directly on the server, use:

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
```bash
sudo ufw allow 5005/tcp
```

---

## Troubleshooting & Common Issues

- **CORS error**: Verify that the domain redirect to the server and reverse proxy routing to the Ubuntu server are properly configured.
- **Firebase Auth error** (*"A project ID is required to access the auth service"*): Ensure `GOOGLE_CLOUD_PROJECT` and `GOOGLE_APPLICATION_CREDENTIALS` are set or debug using the VS Code launch configuration.

---

## Neo4j Cypher Queries

### Match all children of a given parent
```cypher
match(n:Node)-[k:CHILD*]->(r:Node) where id(n)=1040 return r,n,k
```

### Match account and children
```cypher
match (a:account) return a

match(a:account)-[k:CHILD*]->(r:Node) return a,k,r
```

### Convert tree with links (APOC)
```cypher
MATCH path = (a:account {login: $login})-[:CHILD*]->(target)
WHERE ALL(n IN nodes(path) WHERE coalesce(n.deleted, 0) <> 1)
WITH collect(path) AS paths
CALL apoc.convert.toTree(paths) YIELD value
RETURN value
```

### Select node with child nodes
```cypher
match (n:Node {name:'Evolution'})-[l:CHILD]->(m:Node) return n,l,m
```

### Remove relationships
```cypher
match (n:Node {name:'Evolution'})-[l:CHILD]->(m:Node) delete l

match (n:Node {name:'2024.S1'})-[l:CHILD]->(m:Node{name:'Evolution'}) delete l
```
