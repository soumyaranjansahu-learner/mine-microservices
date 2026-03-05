# MINE - API Based Microservices Super App

MINE is a Chrome-based modern web application that acts as an API Gateway to three independent back-end microservices, integrating them seamlessly into a "Super App" Dashboard.

## Architecture Diagram (Text-based)

```text
                  +-----------------------+
                  |                       |
                  |    CLIENT (Browser)   |
                  |    (Bootstrap 5)      |
                  |                       |
                  +-----------+-----------+
                              |
                     (HTTP Requests & JWT)
                              |
                              v
             +----------------+-----------------+
             |                                  |
             |       MAIN GATEWAY (Port 8000)   |
             |       ( mine_main Django App )   |
             |       Handles Auth & Routing     |
             |                                  |
             +--------+---------------+---------+
                      |               |         
           +----------+      +--------+       +---------+
           |                 |                |
(Internal REST API Calls using JWT Token in Authorization Header)
           |                 |                |
           v                 v                v
+-----------------+ +-----------------+ +-----------------+
|  KITCHEN SERVICE| |   SHOP SERVICE  | |  MUSIC SERVICE  |
|  (Port 8001)    | |  (Port 8002)    | |  (Port 8003)    |
|  (mine_kitchen) | |  (mine_shop)    | |  (mine_music)   |
+--------+--------+ +--------+--------+ +--------+--------+
         |                   |                   |
         v                   v                   v
  [ SQLite DB 1 ]     [ SQLite DB 2 ]     [ SQLite DB 3 ]
```

## Features
Each microservice is entirely independent. They each have their own models, views, generic URLs, Django admin panel, and unique SQLite database. Communication only happens via REST APIs!

1. **Main Gateway**: Central auth, issues JWT, renders Bootstrap UI.
2. **Mine Kitchen**: Lists Food Items, manages Cart, handles Orders.
3. **Mine Shop**: Lists Products and Categories, manages Cart, handles Orders.
4. **Mine Music**: Lists Songs, allows music streaming incrementing play count.

## Project Explanation for Viva
- **Microservice Architecture**: A monolithic app splits everything into smaller apps, but they share the database. We built *true Microservices*. Each service is an isolated Django codebase with its own Database. There's zero direct DB sharing. They only expose `JSON REST APIs`.
- **API Gateway**: The `mine_main` Gateway acts as the bridge. It holds the HTML templates and accepts user traffic. When a user requests data, the Gateway makes `requests.get/post()` calls via HTTP to the appropriate backend microservice port.
- **JWT Auth**: We use stateless `JWT` tokens. The Gateway issues the token upon login and stores it in the user's session. The Gateway then attaches this `Bearer <token>` back into the HTTP Headers when talking to the kitchen, shop, and music APIs, authenticating the user seamlessly.

## Running the Application
Ensure Python 3.10+ is installed.

1. Open a terminal in the project root.
2. **Run the initial setup scripts:** (This creates venv, installs requirements, scaffolds projects, and runs migrations. We have already run this during development via `setup.ps1`).
3. Simply execute the Batch file:
```bash
./run_all.bat
```
This will pop up 4 command prompt windows, starting all 4 Django servers on their assigned ports.
4. Open Chrome and navigate to: `http://192.168.0.106:8000`
5. Since there hasn't been data created, go to the respective admin panels `http://127.0.0.1:8001/admin/` etc., and create some sample entries!

## Created By
Developed via Antigravity AI Agent.
