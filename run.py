from flask import Flask, request
import hashlib, json
from datetime import datetime
app = Flask(__name__)

@app.route('/report', methods=['POST'])
def report_phishing():
    url = request.form['url']              # Get the URL submitted by user
    reason = request.form['reason']        # Get the selected reason
    comment = request.form['comment']      # Optional user comment
    timestamp = datetime.utcnow().isoformat()  # Get current UTC time

    # Hash the submitted URL using SHA-256
    hash_val = hashlib.sha256(url.strip().lower().encode()).hexdigest()

    # Create a structured dictionary to represent the report
    report_data = {
        "url": url,
        "hash": hash_val,
        "reason": reason,
        "comment": comment,
        "timestamp": timestamp
    }

    # Append this report to a file (acts like a simple database)
    with open('reports.json', 'a') as f:
        f.write(json.dumps(report_data) + "\n")  # Write as one JSON object per line

    # Return a simple thank-you page with confirmation
    return f"""
    <h2>Thank you!</h2>
    <p>Your report has been submitted.</p>
    <p><strong>SHA-256:</strong> {hash_val}</p>
    <p><strong>Reason:</strong> {reason}</p>
    <p><strong>Submitted at:</strong> {timestamp}</p>
    """
