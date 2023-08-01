from flask import Flask, request
import mysql.connector

app = Flask(__name__)

# database info
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
    state = request.form.get('State', 'language_selection')  # Set the default state to 'language_selection' if not provided.

    # Check if user is at the initial screen
    if text == "" and state == 'language_selection':
        response = "CON Welcome to the registration portal.\nPlease choose your language:\n1. English\n2. Kinyarwanda"
        state = 'language_selection'

    # Check user's progress and handle the response accordingly
    elif state == 'language_selection':
        if text == "1":
            response = "CON You selected English.\nPlease enter your full name"
            state = 'fullname_input'
        elif text == "2":
            response = "CON Wahisemo Ikinyarwanda.\nAndika amazina yawe yose"
            state = 'fullname_input_kinyarwanda'
        else:
            response = "CON Invalid input. Please try again."

    elif state == 'fullname_input':
        fullname = text
        response = "CON Hi {}, enter your District name".format(fullname)
        state = 'district_input'

    elif state == 'fullname_input_kinyarwanda':
        fullname = text
        response = "CON Muraho {}, andika akarere utuyemo".format(fullname)
        state = 'district_input_kinyarwanda'

    elif state == 'district_input':
        district_name = text
        response = "CON Please enter your national ID number"
        state = 'national_id_input'

    elif state == 'district_input_kinyarwanda':
        district_name = text
        response = "CON Andika numero y'indangamuntu"
        state = 'national_id_input_kinyarwanda'

    elif state == 'national_id_input':
        language_selection = '1' if state == 'language_selection' else '2'
        fullname = text
        district_name = text
        national_id = text
        save_registration_data(session_id, phonenumber, fullname,
                               language_selection, district_name, national_id)
        if language_selection == "1":
            response = "END Thank you for registering.\nWe will keep you updated"
        elif language_selection == "2":
            response = "END Murakoze kwiyandikisha.\nTuzabamenyesha."

        # Add a binary (0/1) request to know if registration is continuous or ending
        # You can handle this request as per your specific requirements.
        new_request = request.form.get('Request', '')
        if new_request == "0":
            # Handle continuous registration logic here
            pass
        elif new_request == "1":
            # Handle ending registration logic here
            pass
        else:
            # Handle invalid request type here
            pass

    else:
        response = "END Invalid input. Please try again."

    return response, 200, {'Content-type': 'text/plain'}


if __name__ == "__main__":
    app.run(host="localhost", port=9000)
