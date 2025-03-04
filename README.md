Parted
======


Open Source Christian music app that is similar to BandCamp.com


## Running commands

Container must be running
```
docker-compose exec web <insert commands>
```
eg

```
docker-compose exec web ./manage.py makemigrations
```

## Adding packages

Simply use Poetry command in venv


## Running tests

```
docker-compose exec web pytest
```
