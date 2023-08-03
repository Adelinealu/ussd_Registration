from flask import Flask, request
import mysql.connector

app = Flask(__name__)

# Database info
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="new password",
    database="ussd_database"
)

# Function to save registration data to the database
def save_registration_data(session_id, phonenumber, fullname, language, electoral_ward, national_id):
    cursor = db_connection.cursor()
    query = "INSERT INTO registrations (session_id, phonenumber, fullname, language, electoral_ward, national_id) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (session_id, phonenumber, fullname, language, electoral_ward, national_id)
    cursor.execute(query, values)
    db_connection.commit()

@app.route("/", methods=["POST"])
def ussd_handler():
    text = request.form.get('USSD_STRING', '')
    phonenumber = request.form.get('Phone_Number', '')
    session_id = request.form.get('Session_ID', '')

    # Check if the user is starting the registration process
    if text == "":
        response = "CON Welcome to the registration portal.\nPlease choose your language:\n1. English\n2. Kinyarwanda"
    elif text in ["1", "2"]:
        language_selection = text
        response = (
            "CON You selected English.\nPlease enter your full name"
            if language_selection == "1"
            else "CON Wahisemo Ikinyarwanda.\nAndika amazina yawe yose"
        )
    elif text:
        fullname = text

        # Assuming the next input is for the district name
        response = "CON Hi {}, enter your District name".format(fullname)
    elif text:
        district_name = text

        # Assuming the next input is for the national ID number
        response = "CON Please enter your national ID number"
    elif text:
        national_id = text

        # Assuming the registration process is complete, save data to the database
        save_registration_data(session_id, phonenumber, fullname, language_selection, district_name, national_id)

        response = (
            "END Thank you for registering.\nWe will keep you updated"
            if language_selection == "1"
            else "END Murakoze kwiyandikisha.\nTuzabamenyesha."
        )
    else:
        # Invalid input
        response = "END Invalid input. Please try again."

    return response, 200, {'Content-type': 'text/plain'}


if __name__ == "__main__":
    app.run(host="localhost", port=9000)
