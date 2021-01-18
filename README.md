# forum
the default internet forum. coded with python django.


# Quick start

first of all we should run a postgresql server
```
docker run --net=host rostgres
```

then create a database named forum (by default)
```
docker exec -it <container id> bash
psql -h localhost -p 5432 -U postgres
CREATE DATABASE forum;
```

and start django server
```
git clone https://github.com/e6000000000/forum.git
cd forum
docker build -t forum .
docker run --net=host forum
```