# GitHub Webhook Detection Application

This application detects and notifies suspicious behavior in an integrated GitHub organization using webhooks. It is implemented in Python with Flask.

## Installation

To run this application, you need to have Python and Flask installed on your machine. You can install Flask using pip:

```bash
pip install Flask
```

## Usage
Go to the Smee website(given in the assignment) and start a new channel to get the URL.

Open your terminal or command prompt and navigate to the directory where you have downloaded the files for this application.

Run the following command to forward webhooks to your local server:

```bash
smee -u https://smee.io/<your_generated_smee_code> -t http://127.0.0.1:3000/webhook
Replace <your_generated_smee_code> with the code generated for your Smee channel.
```
Create Webhook

go to the organiztion settings -> webhooks -> Add webhook

in the Payload URL put the smee URL, and in the trigger events select the relevant events for the task, such as Pushes, Repositories and Teams.

Navigate to the server directory:
```bash
cd <the path where you downloaded the assignment>/server
```
Run the Python script to start the server:
```bash
python main.py
```
The application is now running and ready to receive webhook events.

## Webhook Endpoints
/webhook: This endpoint receives webhook events from GitHub and processes them to detect suspicious behavior.
## Dependencies
Flask: The web framework used for handling HTTP requests and responses.
