# ussd_Registration

This is a simple USSD registration portal built using Flask, which allows users to register by providing their information via USSD prompts. The application stores the registration data in a MySQL database.

Requirements:

Python 3
Flask
MySQL database (I used XAMPP with PHPMyAdmin)

Usage:

The application exposes a simple USSD registration portal that can be accessed via POST requests to the root URL.

To initiate a new USSD session, send a POST request with the following parameters in the request body:

USSD_STRING: Leave this empty for the initial request.
Phone_Number: Set the user's phone number (e.g., +1234567890).
Session_ID: A unique session ID for the current USSD session.
The application will respond with a welcome message asking the user to choose their language (1. English or 2. Kinyarwanda).

Subsequent prompts will be displayed based on the user's language selection, and the user will be asked to provide the required information for registration.

The registration data will be saved to the MySQL database upon successful completion of the registration process.

