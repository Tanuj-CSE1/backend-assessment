# backend-assessment
A backend data pipeline project built with Flask, FastAPI, and PostgreSQL.  Features include REST APIs, pagination, data ingestion with upsert logic, and full Docker integration.

Author

Tanuj Kumar   |    Tanujk95681@gmail.com
B.Tech CSE | Backend Developer

All implementation, design, and testing were done by me.

Project Overview-------------

This project implements a data pipeline:

Flask API - > FastAPI -> PostgreSQL

Services---------

Flask (Port 5000) - Mock data API
FastAPI (Port 8000) - Data ingestion + APIs
PostgreSQL (Port 5432) - Database

 Run Project-------------

docker-compose up --build

 API Endpoints----------

Flask
GET /api/customers?page=1&limit=5
GET /api/customers/{id}
GET /api/health

FastAPI
POST /api/ingest
GET /api/customers?page=1&limit=5
GET /api/customers/{id}

 Test
http://localhost:5000/api/customers?page=1&limit=5
http://localhost:8000/docs

 Notes
Uses pagination
Implements upsert logic
Fully dockerized setup
