from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import random

app = Flask(__name__)

# Dictionary to store course details
courses = {
    "1": {
        "name": "Web Development",
        "details": "Learn HTML, CSS, JavaScript, and frameworks like React and Node.js. Duration: 3 months.",
        "academy": "Jurong Academy"
    },
    "2": {
        "name": "Data Science",
        "details": "Master Python, Pandas, NumPy, and Machine Learning basics. Duration: 4 months.",
        "academy": "Jurong Academy"
    },
    "3": {
        "name": "Machine Learning",
        "details": "Deep dive into ML algorithms, TensorFlow, and neural networks. Duration: 5 months.",
        "academy": "Jurong Academy"
    }
}

# Dictionary to store user data
user_data = {}

@app.route("/webhook", methods=['POST'])
def webhook():
    incoming_message = request.form.get('Body').strip().lower()
    from_number = request.form.get('From')  # User's WhatsApp number
    resp = MessagingResponse()

    if from_number not in user_data:
        # New user: Ask for their name
        user_data[from_number] = {"step": "ask_name"}
        resp.message("Welcome to Jurong Academy! 🎉\nWhat is your name?")
    else:
        step = user_data[from_number].get("step")

        if step == "ask_name":
            # Save the user's name and show the menu
            user_data[from_number]["name"] = incoming_message
            user_data[from_number]["step"] = "show_menu"
            resp.message(
                f"Hi {incoming_message.capitalize()}! 😊\n\n"
                "📋 *Menu*\n"
                "Please select a course by typing the corresponding number:\n\n"
                "1️⃣ Web Development\n"
                "2️⃣ Data Science\n"
                "3️⃣ Machine Learning\n\n"
                "Type the number (1, 2, or 3) to see more details."
            )
        elif step == "show_menu":
            if incoming_message in courses:
                # Save the selected course and show details
                user_data[from_number]["course"] = courses[incoming_message]
                user_data[from_number]["step"] = "confirm_booking"
                resp.message(
                    f"✅ *Course Selected:* {courses[incoming_message]['name']}\n\n"
                    f"📚 *Details:* {courses[incoming_message]['details']}\n\n"
                    f"🏫 *Academy:* {courses[incoming_message]['academy']}\n\n"
                    "Type 'confirm' to book this course."
                )
            else:
                # Handle invalid input
                resp.message("❌ Invalid option. Please type a number (1, 2, or 3) to select a course.")
        elif step == "confirm_booking":
            if incoming_message == "confirm":
                # Generate a receipt number and thank the user
                receipt_number = random.randint(100000, 999999)
                user_data[from_number]["receipt_number"] = receipt_number
                resp.message(
                    f"🎉 *Booking Confirmed!*\n\n"
                    f"👤 Name: {user_data[from_number]['name'].capitalize()}\n"
                    f"📚 Course: {user_data[from_number]['course']['name']}\n"
                    f"📝 Receipt Number: {receipt_number}\n\n"
                    "Thank you for booking with Jurong Academy! �\n"
                    "We will contact you shortly with further details."
                )
                # Reset user data for the next interaction
                del user_data[from_number]
            else:
                # Handle invalid input
                resp.message("❌ Please type 'confirm' to book the course.")
        else:
            # Handle unexpected errors
            resp.message("❌ Something went wrong. Please type 'hi' to start again.")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)