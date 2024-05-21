# File Transcoding Service

This project provides a file transcoding service using a Flask REST API and a Kafka message queue for processing. The service allows users to upload files for transcoding, which are then processed by Kafka consumers.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Kafka Message Queue](#kafka-message-queue)
- [Docker Setup](#docker-setup)
- [Contributing](#contributing)
- [License](#license)

## Features

- Upload files via a REST API.
- Transcode uploaded files to multiple quality formats.
- Download transcoded files as a zip archive.

## Prerequisites

- Docker and Docker Compose
- Python 3.8+

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/haithanh079/transcoding-service.git
    cd transcoding-service
    ```

2. Set up a virtual environment and install dependencies:

    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

## Usage

### REST API

1. Start the Flask server:

    ```bash
    python app.py
    ```

2. Upload a file using the `/upload` endpoint.
Use the form-data with file

#### POST /upload
Uploads a file for transcoding.

- **URL**: `/upload`
- **Method**: `POST`
- **Form Data**:
  - `file`: The file to be uploaded.
- **Success Response**:
  - **Code**: 200
  - **Content**: `Downloadable Zip File`
- **Error Response**:
  - **Code**: 400
  - **Content**: `{ "error": "No file part" }`
  - **Code**: 400
  - **Content**: `{ "error": "No selected file" }`

#### Sample use
Curl format - Use directly in Terminal or import into Postman
```bash
curl --location 'http://localhost:3001/upload' \
--form 'file=@"/path/to/file.mp3"'
```

Sample 
```bash
curl --location 'http://localhost:3001/upload' \
--form 'file=@"./Chandelier_Sia_fix.mp3"'
```

### Async processing with Kafka
Updating...

## Docker Setup

Use Docker Compose to set up the environment:

1. Build and start the containers:

    ```bash
    docker-compose up --build
    ```

2. The Flask server will be accessible at `http://localhost:3001`.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss any changes.

## License

This project is licensed under the MIT License.
