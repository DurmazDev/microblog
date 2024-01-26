# Microblog with Flask & Vue

A micro-blogging platform with Flask & Vue

## Run Locally

Clone the project

```bash
  git clone https://github.com/DurmazDev/microblog
```

## Run with Docker-Compose

```
  cd microblog
```

```
  docker-compose up --build
```

## Run manually (not recommended)

> **Start MongoDB & Redis and reconfigure `app/config.py` file.**

### Start the back-end firstly

Enter directory

```bash
  cd microblog/backend/
```

Create Virtual Environment & Install Dependencies

```bash
  python3 -m venv venv
  source venv/bin/activate
  python3 -m pip install -r requirements.txt
```

Start the server

```bash
  python3 run.py
```

To see API documentation, look README file under the backend folder.

### Start the front-end

Enter directory

```bash
  cd microblog/frontend/
```

Rename config.template.js to config.js and check configurations.

```bash
  mv src/config.template.js src/config.js
```

Install Dependencies

```bash
  npm install
```

Start in dev mode

```bash
  npm run dev
```

## License

This repo is licensed under the [MIT](https://choosealicense.com/licenses/mit/) licence.
