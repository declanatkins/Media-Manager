# Media Manager App

A frontend/backend application for managing your media!


## Running Instructions

This app is deployed through docker-compose.
```bash
docker-compose up
```

You can then access the frontend at http://localhost

You can see the backend swagger-ui at http://localhost:5000/ui



## Backend Tests

To run the backend tests:
```
cd backend
pip install -r requirements.txt
pytest -vv
```