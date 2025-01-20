import os
import resend
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from typing import Dict, Any, List, Union

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure Resend
resend.api_key = os.getenv("RESEND_API_KEY")
if not resend.api_key:
    raise ValueError("RESEND_API_KEY not found in environment variables")

# Configuration
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "Acme <onboarding@resend.dev>")

class EmailError(Exception):
    """Custom exception for email-related errors"""
    pass

def send_email(
    to: Union[str, List[str]],
    subject: str,
    html_content: str,
    from_email: str = DEFAULT_FROM_EMAIL
) -> Dict[str, Any]:
    """
    Send an email using Resend
    
    Args:
        to: Recipient email address or list of addresses
        subject: Email subject
        html_content: HTML content of the email
        from_email: Sender email address (optional)
    
    Returns:
        Dict containing the Resend API response
    
    Raises:
        EmailError: If there's an error sending the email
    """
    try:
        # Convert single email to list
        to_emails = [to] if isinstance(to, str) else to
        
        params: resend.Emails.SendParams = {
            "from": from_email,
            "to": to_emails,
            "subject": subject,
            "html": html_content,
        }
        
        response = resend.Emails.send(params)
        return response
    except Exception as e:
        raise EmailError(f"Failed to send email: {str(e)}")

@app.route("/send-email", methods=["POST"])
def send_email_endpoint():
    """Endpoint to send emails"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ["to", "subject", "html"]
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "status": "error",
                    "message": f"Missing required field: {field}"
                }), 400
        
        # Send email
        response = send_email(
            to=data["to"],
            subject=data["subject"],
            html_content=data["html"],
            from_email=data.get("from", DEFAULT_FROM_EMAIL)
        )
        
        return jsonify({
            "status": "success",
            "data": response
        })
        
    except EmailError as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred"
        }), 500

@app.route("/health")
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "api_configured": bool(resend.api_key)
    })

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    
    app.run(host="0.0.0.0", port=port, debug=debug)