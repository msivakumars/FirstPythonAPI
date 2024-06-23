# CONTRIBUTING


## HOW TO RUN THE DOCKERFILE LOCALLY

```commandline
docker run -dp 5000:5000 -w /app -v "/c/Siva/Udemy/Python/FirstPythonAPI:/app" first-python-api sh -c "flask run --host 0.0.0.0"
```