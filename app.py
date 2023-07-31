from flask import Flask, request
import mysql.connector

app = Flask(__name__)

# Replace the connection parameters with your database info
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="new password",
    database="ussd_database"
)

def save_registration_data(phonenumber, fullname, language, electoral_ward, national_id):
    cursor = db_connection.cursor()
    query = "INSERT INTO registrations (phonenumber, fullname, language, electoral_ward, national_id) VALUES (%s, %s, %s, %s, %s)"
    values = (phonenumber, fullname, language, electoral_ward, national_id)
    cursor.execute(query, values)
    db_connection.commit()

@app.route("/", methods=["POST"])
def ussd_handler():
    text = request.form.get('USSD_STRING', '')
    phonenumber = request.form.get('MSISDN', '')

    level = text.split("*")

    # Check if user is at the initial screen
    if text == "":
        response = "CON Welcome to the registration portal.\nPlease choose your language:\n1. English\n2. Kinyarwanda"

    # Check user's progress and handle the response accordingly
    elif len(level) == 1:
        if level[0] == "1":
            response = "CON You selected English.\nPlease enter your full name"
        elif level[0] == "2":
            response = "CON Wahisemo Ikinyarwanda.\nAndika amazina yawe yose"
        else:
            response = "END Invalid input. Please try again."

    elif len(level) == 2:
        language_selection = level[0]
        fullname = level[1]
        if language_selection == "1":
            response = "CON Hi {}, enter your ward name".format(fullname)
        elif language_selection == "2":
            response = "CON {}, Andika akarere utuyemo".format(fullname)
        else:
            response = "END Invalid language selection. Please try again."

    elif len(level) == 3:
        language_selection = level[0]
        fullname = level[1]
        ward_name = level[2]
        if language_selection == "1":
            response = "CON Please enter your national ID number"
        elif language_selection == "2":
            response = "CON Andika numero y'indangamuntu"
        else:
            response = "END Invalid input. Please try again."

    elif len(level) == 4:
        language_selection = level[0]
        fullname = level[1]
        ward_name = level[2]
        national_id = level[3]
        save_registration_data(phonenumber, fullname, language_selection, ward_name, national_id)
        if language_selection == "1":
            response = "END Thank you for registering.\nWe will keep you updated"
        elif language_selection == "2":
            response = "END Murakoze kwiyandikisha.\nTuzabamenyesha."

    else:
        response = "END Invalid input. Please try again."

    return response

if __name__ == "__main__":
    app.run(host="localhost", port=9000)
