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

install forum
```
git clone https://github.com/e6000000000/forum.git
cd forum
```

create file `forum/mysite/secret_settings.py` and configure it
```python
SECRET_KEY = 'your secret key'
DATABASE_PASSWORD = 'your database password'
EMAIL_HOST_USER = 'your@mail.com'
EMAIL_HOST_PASSWORD = 'yourpassword'
```

build and start server
```
docker build -t forum .
docker run --net=host forum
```

# Configuration
To setup default user avatar you should add `default.png` file to your media dir (default is `forum/media/`)
