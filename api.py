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
    values = (session_id, phonenumber, fullname,
              language, electoral_ward, national_id)
    cursor.execute(query, values)
    db_connection.commit()


@app.route("/", methods=["POST"])
def ussd_handler():
    text = request.form.get('USSD_STRING', '')
    phonenumber = request.form.get('Phone_Number', '')
    session_id = request.form.get('Session_ID', '')

    # Retrieve the current user's language selection and registration progress from the database (if available)
    cursor = db_connection.cursor()
    cursor.execute(
        "SELECT language, progress FROM registrations WHERE session_id = %s", (session_id,))
    row = cursor.fetchone()
    if row:
        language_selection, progress = row
    else:
        language_selection, progress = None, 0

    if text == "":
        response = "CON Welcome to the registration portal.\nPlease choose your language:\n1. English\n2. Kinyarwanda"
    elif text in ["1", "2"]:
        language_selection = text
        progress = 1

        if language_selection == "1":
            response = "CON You selected English.\nPlease enter your full name"
        elif language_selection == "2":
            response = "CON Wahisemo Ikinyarwanda.\nAndika amazina yawe yose"
        else:
            response = "END invalid input try again later!"

    elif progress == 1 and text:
        fullname = text
        progress = 2

        if language_selection == "1":
            response = "CON Hi {}, enter your District name".format(fullname)
        else:
            response = "CON Muraho {}, andika akarere utuyemo".format(fullname)
    elif progress == 2 and text:
        district_name = text
        progress = 3

        if language_selection == "1":
            response = "CON Please enter your national ID number"
        else:
            response = "CON Andika numero y'indangamuntu yawe"
    elif progress == 3 and text:
        national_id = text
        save_registration_data(session_id, phonenumber, fullname,
                               language_selection, district_name, national_id)
        progress = 4

        if language_selection == "1":
            response = "CON Registration successful. Thank you!"
        else:
            response = "CON Kwiyandikisha byagenze neza. Murakoze!"
    elif progress == 4 and text == "1":
        progress = 0
        response = "CON Welcome back. Please choose your language:\n1. English\n2. Kinyarwanda"
    elif progress == 4 and text == "0":
        progress = -1
        response = "END Thank you for using our service."

    # Update progress in the database
    if progress >= 0:
        cursor.execute(
            "UPDATE registrations SET progress = %s WHERE session_id = %s", (progress, session_id))
        db_connection.commit()

    return response, 200, {'Content-type': 'text/plain'}


if __name__ == "__main__":
    app.debug = False
    app.run(host="localhost", port=5000)
