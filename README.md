# Forum
The default internet forum. Coded with python django.


# Installation

First of all we should run a [postgresql server](https://hub.docker.com/_/postgres).
Then create a database named `forum` (by default) and configure it.
```bash
psql -h localhost -p 5432 -U postgres
CREATE DATABASE forum;
CREATE EXTENSION unaccent;
CREATE EXTENSION pg_trgm;
```

Clone forum.
```bash
git clone https://github.com/e6000000000/forum.git
cd forum
```

Set variables in `env.list` file.
You can get recaptcha site key and recapthca private key [there](https://www.google.com/recaptcha/about/).

Now you can build and start server.
```bash
docker build -t forum:1 .
docker run --net=host --env-file env.list -v ~/forummedia:/code/media ~/forumlogs:/code/logs forum:1
```

# Configuration
To setup default user avatar add `default.png` file to your media dir (default is `forum/media/`).

If your email host is not gmail change some variables below `# email server` in `forum/mysite/settings.py`.
