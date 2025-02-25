## Flask Data Generator

## Overview
This is a Flask-based application that generates massive amounts of fake data and stores it in a PostgreSQL database. The application includes a frontend to monitor live data updates.

## Features
- Connect to a PostgreSQL database dynamically.
- Generate massive amounts of fake customer, transaction, and order data.
- View live data updates in the UI.
- Start/Stop data generation with buttons.
- Fully Dockerized with PostgreSQL support.

## Technologies Used
- **Backend:** Flask, Psycopg2, Faker
- **Frontend:** HTML, JavaScript, CSS
- **Database:** PostgreSQL
- **Containerization:** Docker, Docker Compose

---

## Setup & Installation
### 1️⃣ Clone the Repository
```sh
git clone <your-repo-url>
cd flask-data-generator
```

### 2️⃣ Setup Virtual Environment
```sh
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 4️⃣ Run Flask Application
```sh
python app.py
```
- Open your browser and go to **`http://127.0.0.1:5000/`**.

---

## Running with Docker

### 1️⃣ Build and Run Containers
```sh
docker-compose build
docker-compose up -d
```

### 2️⃣ Access the Application
- Open **`http://localhost:5000/`** in your browser.

### 3️⃣ Stop Containers
```sh
docker-compose down
```

---

## Environment Variables
These environment variables can be configured in `docker-compose.yml`:
```yaml
DB_HOST: db
DB_PORT: 5432
DB_NAME: fakedb
DB_USER: postgres
DB_PASSWORD: secret
```

---

## API Endpoints
| Method | Endpoint          | Description           |
|--------|------------------|----------------------|
| POST   | `/connect_db`      | Connect to PostgreSQL |
| POST   | `/start_generation` | Start generating data |
| POST   | `/stop_generation`  | Stop generating data |
| GET    | `/fetch_data`      | Fetch latest records |

---

## Contribution & Issues
Feel free to contribute to the project or report issues on GitHub.

---

## License
This project is licensed under the MIT License.

