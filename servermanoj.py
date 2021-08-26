"""
A sample Flask app for sending SMS messages.
"""

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for
import nexmo

from util import env_var, extract_error

# Load environment variables from a .env file:
#load_dotenv('.env')
load_dotenv('.env')

# Load in configuration from environment variables:
NEXMO_API_KEY ='96ee6f3e' #env_var('96ee6f3e')
NEXMO_API_SECRET ='tQe3v3w5PDJVhC8s' #env_var('tQe3v3w5PDJVhC8s')
NEXMO_NUMBER = '8074345685'#env_var('8074345685')

# Create a new Nexmo Client object:
nexmo_client = nexmo.Client(
    api_key=NEXMO_API_KEY, api_secret=NEXMO_API_SECRET
)

# Initialize Flask:
app = Flask(__name__)
app.config['SECRET_KEY'] = env_var('FLASK_SECRET_KEY')


@app.route('/')
def index():
    """ A view that renders the Send SMS form. """
    return render_template('index.html')


@app.route('/send_sms', methods=['POST'])
def send_sms():
    """ A POST endpoint that sends an SMS. """

    # Extract the form values:
    to_number = "+91 8074345685" #request.form['to_number']
    message = request.form['message']

    # Send the SMS message:
    result = nexmo_client.send_message({
        'from': NEXMO_NUMBER,
        'to': to_number,
        'text': message,
    })

    # Set a message for the user to see on the next view:
    err = extract_error(result)
    if err is not None:
        flash("There was a problem sending your message: " + err, 'error')
    else:
        flash("You just sent a message to " + to_number)

    # Redirect the user back to the form:
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
