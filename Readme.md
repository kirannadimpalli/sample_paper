# Sample API Application Documentation

## Overview

This FastAPI application provides a set of APIs to manage `SamplePaper` documents, process PDF files asynchronously using Celery, and interact with a MongoDB database and Redis cache.

### Key Components:
1. **MongoDB** - Used for storing paper and task data.
2. **Redis** - Used for caching paper data and task statuses.
3. **Celery** - Used for handling asynchronous background tasks like PDF extraction.
4. **FastAPI** - A web framework used to expose RESTful APIs.

## Table of Contents

- [API Endpoints](#api-endpoints)
  - [Health Check](#health-check)
  - [Paper Management](#paper-management)
  - [Task Management](#task-management)
  - [PDF Processing](#pdf-processing)


## API Endpoints

### Health Check

- **GET `/health`**
  
  This endpoint is used to check if the API is running.

  **Response:**
  ```json
  {
    "status": "ok"
  }
    ```

# API Documentation

## Paper Management

### GET `/papers/{paper_id}`

Fetches a paper by its ID. The application first checks if the paper is available in Redis cache. If not, it retrieves the paper from MongoDB and caches it.

**Parameters:**
- `paper_id`: The unique ID of the paper.

**Response:**
```json
{
  "paper_id": "string",
  "title": "string",
  "content": "string"
}
```
### POST `/papers`

Creates a new paper document in MongoDB.

**Request Body:**

*title*: The title of the paper.

*content*: The content of the paper.

**Response:**
```json
{
  "paper_id": "string",
  "title": "string",
  "content": "string"
}
```
## PUT `/papers/{paper_id}`

Updates an existing paper document in MongoDB.

### Request Parameters:
- `paper_id`: The unique ID of the paper.

### Request Body:
- JSON object containing fields to update.

### Response:
```json
{
  "message": "Paper updated successfully"
}
```

## DELETE `/papers/{paper_id}`

Deletes a paper from MongoDB based on its ID.

### Request Parameters:
- `paper_id`: The unique ID of the paper.

### Response:
```json
{
  "message": "Paper deleted successfully"
}
```

# Task Management

## GET `/tasks/{task_id}`

Retrieves the status of a specific task.

### Request Parameters:
- `task_id`: The unique ID of the task.

### Response:
```json
{
  "task_id": "string",
  "status": "pending|completed",
  "paper_id": "string|null"
}
```

# PDF Processing

## POST `/extract/pdf`

This endpoint accepts a PDF file, processes it asynchronously using a Celery task, and returns a task ID.

### Request Body:
- PDF file to be processed.

### Response:
```json
{
  "task_id": "string",
  "status": "pending"
}
```

## POST `/extract/text`

Accepts plain text input, processes it using a utility function (`extract_pdf_data`), and returns structured data in JSON format.

### Request Body:
```json
{
  "text": "string"
}
```

### Response:
``` json
{
  "title": "string",
  "content": "string"
}
```

# Running the Application (Setup Serve)

## Prerequisites
- Ensure you have Docker and Docker Compose installed on your machine.

## Steps
1. Clone the repository:
   ```bash
   git clone git@github.com:kirannadimpalli/sample_paper.git
   ```
2. Navigate to the project directory:
    ```bash
    cd sample_page
    ```
3. Build and start the services using Docker Compose:
    ```bash
    docker-compose up -d --build
    ```
4. Verify that the services are running by checking the logs:
    ``` bash
    docker-compose logs
    ```
5. Access the application via:
    ``` bash
    http://localhost:8000
    ```


# Sample Paper API - Postman Collection

## Importing the Postman Collection

To easily test the API endpoints, you can import the provided Postman collection.

1. Download the Postman collection JSON file:
   - [Download Postman Collection](Postman_collections\sample_paper.postman_collection.json)

2. Open Postman and click on the **Import** button in the top left corner.

3. Select the downloaded `.json` file or drag it into the Postman window.

4. The collection will now appear in your Postman under the **Collections** tab.

## Collection Details

The Postman collection contains the following requests:

- **Create Paper (POST)**: `POST /papers`
- **Get Paper by ID (GET)**: `GET /papers/{paper_id}`
- **Update Paper (PUT)**: `PUT /papers/{paper_id}`
- **Delete Paper (DELETE)**: `DELETE /papers/{paper_id}`
- **Get Task Status (GET)**: `GET /tasks/{task_id}`
- **Extract PDF (POST)**: `POST /extract/pdf`
- **Extract Text (POST)**: `POST /extract/text`

This collection covers all the major API endpoints for interacting with the sample paper service.


# Gemini API Setup

To set up the Gemini API, you'll need to create a `.env` file and add your Google Cloud credentials. Follow the steps below:

## Step 1: Create a `.env` File

1. Create a new file named `.env` in your project directory.
2. Add the following lines to the `.env` file, replacing `<file path>` and `<project id>` with your specific values:

   ```plaintext
   GOOGLE_APPLICATION_CREDENTIALS='<file path>'
   PROJECT_ID='<project id>'
   ```
## Step 2: Obtain Credentials File and Project ID

To obtain the necessary credentials and project ID, follow these steps:

### Access Google Cloud Console

1. Visit the [Google Cloud Console](https://console.cloud.google.com/projectselector2/home/dashboard).
2. If you do not have an account, create one and sign in.

### Create a New Project

1. Click on the **"Create Project"** button.
2. Fill in the required details and click **"Create"**.

### Enable the API

1. Navigate to the following link to enable the API (note that this may incur charges): [Enable AI Platform API](https://console.cloud.google.com/flows/enableapi?apiid=aiplatform.googleapis.com).

### Retrieve Your Project ID

1. Go to the project you just created.
2. Locate the **Project ID** displayed on the project dashboard and take note of it.

### Create Credentials

1. Navigate to **API & Services** > **Credentials**.
2. Click on **"Create Credentials"** and select **"Service Account"**.
3. Follow the prompts to generate a service account, which will download a JSON file containing your credentials.
4. Note the file path of the downloaded JSON file and update your `.env` file accordingly:

   ```plaintext
   GOOGLE_APPLICATION_CREDENTIALS='<file path to your downloaded JSON>'
    ```

After completing these steps, your Gemini API setup will be ready to use!

