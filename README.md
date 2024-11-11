# README

## How to run the API locally

```
docker build -t flask-rest-api .
docker run -dp 5000:5000 -w /app -v "${current_dir}:/app" flask-rest-api sh -c "flask run --host 0.0.0.0"
```