# Flask Resend Email Service

A Flask-based REST API service for sending emails using the Resend email delivery platform. This service provides a simple and reliable way to send HTML emails through a RESTful interface.

## Features

- Send HTML emails via REST API
- Environment-based configuration
- CORS support
- Health check endpoint
- Comprehensive error handling
- Type-safe implementation

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.7+
- pip (Python package manager)
- A Resend account and API key (get one at [resend.com](https://resend.com))

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/flask-resend-service.git
cd flask-resend-service
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install flask flask-cors python-dotenv resend
```

4. Create a `.env` file in the project root:

```plaintext
RESEND_API_KEY=your_resend_api_key_here
DEFAULT_FROM_EMAIL=Your Name <your@email.com>
PORT=5000
FLASK_DEBUG=True
```

## Configuration

The application can be configured using environment variables:

| Variable           | Description                      | Default                        |
| ------------------ | -------------------------------- | ------------------------------ |
| RESEND_API_KEY     | Your Resend API key              | Required                       |
| DEFAULT_FROM_EMAIL | Default sender email address     | "Acme <onboarding@resend.dev>" |
| PORT               | Port number for the Flask server | 5000                           |
| FLASK_DEBUG        | Enable debug mode                | False                          |

## API Endpoints

### Send Email

Send an HTML email to one or more recipients.

**Endpoint:** `POST /send-email`

**Request Body:**

```json
{
  "to": "recipient@example.com", // String or Array of strings
  "subject": "Email Subject",
  "html": "<h1>Email Content</h1>",
  "from": "optional@sender.com" // Optional
}
```

**Success Response:**

```json
{
  "status": "success",
  "data": {
    "id": "email_id"
    // Additional Resend response data
  }
}
```

**Error Response:**

```json
{
  "status": "error",
  "message": "Error description"
}
```

### Health Check

Check the service status and configuration.

**Endpoint:** `GET /health`

**Response:**

```json
{
  "status": "healthy",
  "api_configured": true
}
```

## Running the Application

1. Activate the virtual environment:

```bash
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

2. Start the server:

```bash
python app.py
```

The server will start on `http://localhost:5000` (or your configured PORT).

## Testing

You can test the API using curl:

```bash
curl -X POST http://localhost:5000/send-email \
  -H "Content-Type: application/json" \
  -d '{
    "to": "recipient@example.com",
    "subject": "Test Email",
    "html": "<h1>Hello World!</h1><p>This is a test email.</p>"
  }'
```

## Error Handling

The API handles various error cases:

- Missing required fields
- Invalid email addresses
- Resend API errors
- Server errors

All errors return appropriate HTTP status codes and descriptive messages.

## Security Considerations

- Never commit your `.env` file to version control
- Use HTTPS in production
- Consider implementing rate limiting for production use
- Review Resend's security recommendations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
