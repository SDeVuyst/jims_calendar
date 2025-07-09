# Jims Calendar

## Starting
```console
docker build -t gym-calendar .
```

```console
docker run -p 8000:8000 --env-file .env gym-calendar
```

## Accessing data
visit the following URL

http://localhost:8000/gym.ics?token={TOKEN}