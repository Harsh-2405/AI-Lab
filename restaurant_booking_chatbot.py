import re
import json
import os
from datetime import datetime

# File to store bookings
BOOKINGS_FILE = "bookings.json"

# Restaurant configuration
TABLES = 10  # Total tables
SLOTS = ["12:00 PM", "1:00 PM", "6:00 PM", "7:00 PM", "8:00 PM"]  # Available time slots

# Load bookings from file
def load_bookings():
    if os.path.exists(BOOKINGS_FILE):
        with open(BOOKINGS_FILE, 'r') as f:
            return json.load(f)
    return {}

# Save bookings to file
def save_bookings(bookings):
    with open(BOOKINGS_FILE, 'w') as f:
        json.dump(bookings, f, indent=4)

# Check table availability
def check_availability(date, time):
    bookings = load_bookings()
    date_bookings = bookings.get(date, {})
    time_bookings = date_bookings.get(time, 0)
    return TABLES - time_bookings

# Make a reservation
def make_reservation(name, date, time, party_size):
    bookings = load_bookings()
    if date not in bookings:
        bookings[date] = {}
    if time not in bookings[date]:
        bookings[date][time] = 0
    
    available = check_availability(date, time)
    if available >= party_size:
        bookings[date][time] += party_size
        bookings[date][f"{time}_names"] = bookings[date].get(f"{time}_names", []) + [name]
        save_bookings(bookings)
        return f"Reservation confirmed for {name} on {date} at {time} for {party_size} people."
    return f"Sorry, only {available} seats available for {date} at {time}."

# Cancel a reservation
def cancel_reservation(name, date, time):
    bookings = load_bookings()
    if date in bookings and f"{time}_names" in bookings[date] and name in bookings[date][f"{time}_names"]:
        bookings[date][f"{time}_names"].remove(name)
        bookings[date][time] -= 1
        if bookings[date][time] == 0:
            del bookings[date][time]
            del bookings[date][f"{time}_names"]
            if not bookings[date]:
                del bookings[date]
        save_bookings(bookings)
        return f"Reservation for {name} on {date} at {time} canceled."
    return "No reservation found for that name, date, and time."

# Respond to user input
def respond(message):
    message = message.lower()

    # Greeting
    if re.search(r'\b(hi|hello|hey|greetings)\b', message):
        return "Welcome to Taste Haven Restaurant! How can I help you? (Book, check availability, cancel, etc.)"

    # Check availability
    elif re.search(r'\b(available|availability|tables|open)\b', message):
        date_match = re.search(r'\b(\d{1,2}/\d{1,2}/\d{4})\b', message)
        time_match = re.search(r'\b(\d{1,2}:\d{2}\s*(am|pm))\b', message)
        date = date_match.group(1) if date_match else "today"
        time = time_match.group(1) if time_match else None
        if time in SLOTS:
            available = check_availability(date, time)
            return f"{available} tables available on {date} at {time}."
        return f"Please specify a valid time slot: {', '.join(SLOTS)}."

    # Make reservation
    elif re.search(r'\b(book|reserve|reservation)\b', message):
        name_match = re.search(r'\bname\s+(\w+)\b', message)
        date_match = re.search(r'\b(\d{1,2}/\d{1,2}/\d{4})\b', message)
        time_match = re.search(r'\b(\d{1,2}:\d{2}\s*(am|pm))\b', message)
        size_match = re.search(r'\b(\d+)\s*(people|person)\b', message)
        
        name = name_match.group(1) if name_match else "Guest"
        date = date_match.group(1) if date_match else datetime.now().strftime("%m/%d/%Y")
        time = time_match.group(1) if time_match else None
        party_size = int(size_match.group(1)) if size_match else 1

        if time in SLOTS:
            return make_reservation(name, date, time, party_size)
        return f"Please specify a valid time slot: {', '.join(SLOTS)}."

    # Cancel reservation
    elif re.search(r'\b(cancel|delete)\b', message):
        name_match = re.search(r'\bname\s+(\w+)\b', message)
        date_match = re.search(r'\b(\d{1,2}/\d{1,2}/\d{4})\b', message)
        time_match = re.search(r'\b(\d{1,2}:\d{2}\s*(am|pm))\b', message)
        
        name = name_match.group(1) if name_match else None
        date = date_match.group(1) if date_match else None
        time = time_match.group(1) if time_match else None

        if name and date and time in SLOTS:
            return cancel_reservation(name, date, time)
        return "Please provide name, date (MM/DD/YYYY), and time slot."

    # Farewell
    elif re.search(r'\b(bye|goodbye|exit|quit)\b', message):
        return "Thank you for choosing Taste Haven! Goodbye. Type 'exit' to end."

    # Default
    else:
        return "Sorry, I didn't understand. Try 'book a table', 'check availability', or 'cancel reservation'."

# Main execution
def main():
    print("Chatbot: Welcome to Taste Haven Restaurant Booking Bot! Type 'exit' or 'bye' to quit.")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'bye', 'goodbye', 'quit']:
            print("Chatbot: Goodbye!")
            break
        response = respond(user_input)
        print(f"Chatbot: {response}")

if __name__ == "__main__":
    main()