# WebGuard — Web Vulnerability Scanner

WebGuard is a full-stack web application for running lightweight vulnerability checks against a target URL, storing scan history in MongoDB Atlas, and exporting results as a PDF report.

## Features

- Port scan with a limited range for faster, safer analysis
- SSL certificate inspection and expiry warnings
- HTTP security header review
- Basic SQLi and XSS probe checks
- WHOIS lookup for domain metadata
- MongoDB-backed scan history
- PDF report export with reportlab

## Tech Stack

- Frontend: Next.js 14, TypeScript, Tailwind CSS
- Backend: Python FastAPI
- Database: MongoDB Atlas with pymongo
- PDF Export: reportlab
- Additional libraries: python-nmap, python-whois, requests

## Project Structure

```text
webguard/
├── frontend/
│   ├── app/
│   └── components/
├── backend/
│   ├── main.py
│   ├── scanner/
│   ├── db/
│   └── utils/
└── README.md
```

## Setup

### Backend

1. Create and activate a Python virtual environment.
2. Install dependencies:

```bash
cd backend
pip install -r requirements.txt
```

3. Create a `.env` file from `.env.example` and set your MongoDB Atlas connection string.
4. Start the API:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

1. Install dependencies:

```bash
cd frontend
npm install
```

2. Create a `.env.local` file from `.env.local.example`.
3. Start the app:

```bash
npm run dev
```

## Screenshots

Add screenshots of the home page, results dashboard, and history page here.

## Notes

- CORS is configured in FastAPI to allow requests from `http://localhost:3000`.
- Scanner functions are wrapped with error handling and return safe defaults on failure.
- Localhost and private IP targets are blocked from port scanning.

## Built By

Built by Nitin Gupta

- GitHub: https://github.com/nitingupta
- LinkedIn: https://www.linkedin.com/in/nitingupta
