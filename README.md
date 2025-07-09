# Jims Calendar

## Starting

### Create a .env file with the following data
```
SECRET_TOKEN=super-secret-token-123
JIMS_EMAIL=example@gmail.com
JIMS_PASSWORD=password
```

```console
docker build -t gym-calendar .
```

```console
docker run -p 8000:8000 --env-file .env gym-calendar
```

## Accessing data
visit the following URL

http://localhost:8000/gym.ics?token={SECRET_TOKEN}