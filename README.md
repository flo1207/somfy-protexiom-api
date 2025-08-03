# Somfy Protexiom Web API

## Table of Contents

- [Project Overview](#project-overview)
- [Environment Requirements](#environment-requirements)
- [Project Structure](#project-structure)
- [Setup and Running](#setup-and-running)
  - [Automated launch (recommended)](#automated-launch-recommended)
  - [Manual launch](#manual-launch)
- [Access](#access)
- [Notes](#notes)
- [Available API Endpoints](#available-api-endpoints)
- [Contact](#contact)

---

## Project Overview

This project is a lightweight REST API for remotely controlling and monitoring a Somfy alarm protexium system via its local web interface.

It includes:

- **Backend:** A Flask-based HTTP API that wraps an interface to the Somfy HTML panel using Python, `requests`, and `BeautifulSoup`.

With this tool, you can:
- Log in and out automatically
- Activate or deactivate alarm zones (A, B, C)
- Retrieve general system state (battery, door status, GSM...)
- Retrieve alarm status per zone (active/inactive, alert/no alert)

---

## Environment Requirements

- **Python 3.8+**
- Tested on **Linux** and **Windows** (local interface required)
- **Somfy alarm panel accessible via local IP (HTTPS)**

---

## Project Structure

```bash
root/
├── app.py               # Flask API with routes to control the alarm
├── somfy.py             # Main class that handles interaction with the Somfy web interface
├── config.json          # Contains local URL, password, and one-time codes
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

---

## Setup and Running

### Automated launch (recommended)

Run the shell script to setup and start both backend and frontend:

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
````
This script will:

- Set up a virtual environment

- Install required Python packages

- Launch the Flask API server


### Manual launch


1 - Install dependencies:
```bash
pip install -r requirements.txt
```

2 - Run the Flask server:

```bash
python app.py
```

## Access
By default, the Flask API runs on: http://127.0.0.1:5000

You can test the API with tools like curl, Postman, or from your browser.

## Available API Endpoints

| Method | Endpoint            | Description                          |
|--------|---------------------|--------------------------------------|
| GET    | `/api/ping`         | Check if the API is alive            |
| GET    | `/api/state`        | Retrieve general system state        |
| GET    | `/api/zones`        | Get status of all alarm zones        |
| POST   | `/api/zones/A/on`   | Activate alarm zone A                |
| POST   | `/api/zones/B/on`   | Activate alarm zone B                |
| POST   | `/api/zones/C/on`   | Activate alarm zone C                |
| POST   | `/api/zones/ABC/on` | Activate zones A, B, and C           |
| POST   | `/api/zones/A/off`  | Deactivate alarm zone A              |
| POST   | `/api/zones/B/off`  | Deactivate alarm zone B              |
| POST   | `/api/zones/C/off`  | Deactivate alarm zone C              |
| POST   | `/api/zones/ABC/off`| Deactivate zones A, B, and C         |

## Notes

- Make sure your Somfy device is accessible via HTTPS (you may need to disable SSL verification).

- All credentials and key codes must be set in config.json.

- This project disables SSL warnings (not suitable for production).

- No frontend is provided – this is purely a backend API.

- For remote use, port-forwarding or VPN access is required.



## Contact

Feel free to fork the project, open issues, or submit pull requests.

For help or feedback, open an issue directly on this repository.