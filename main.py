from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
import random
from string import ascii_uppercase

# Create the Flask application instance
app = Flask(__name__)
# Set the secret key for session management
app.config["SECRET_KEY"] = "0000"
# Initialize SocketIO with the Flask app
socketio = SocketIO(app)

# Dictionary to store room information
rooms = {}

# Function to generate a unique room code
def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        
        if code not in rooms:
            break
    
    return code

# Route for the home page
@app.route("/", methods=["POST", "GET"])
def home():
    # Clear the session data
    session.clear()
    if request.method == "POST":
        # Get form data
        name = request.form.get("name")
        code = request.form.get("code").upper()
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        # Validation for joining a room
        if join != False and not name:
            return render_template("home.html", error="Please enter a name.", code=code, name=name)

        if join != False and not code:
            return render_template("home.html", error="Please enter a room code.", code=code, name=name)
        
        # If creating a room, set name to "Host"
        if create != False:
            name = "Host"
        
        room = code
        if create != False:
            # Generate a unique room code and create the room
            room = generate_unique_code(4)
            rooms[room] = {"members": 0, "messages": []}
        elif code not in rooms:
            return render_template("home.html", error="Room does not exist.", code=code, name=name)
        
        # Store room and name in session
        session["room"] = room
        session["name"] = name

        # Redirect to host or room page based on the action
        if create != False:
            return redirect(url_for("host"))

        return redirect(url_for("room"))

    return render_template("home.html")

# Route for the host page
@app.route("/host")
def host():
    room = session.get("room")
    name = session.get("name")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("home"))

    return render_template("host.html", code=room, name=name, messages=rooms[room]["messages"])

# Route for the room page
@app.route("/room")
def room():
    room = session.get("room")
    name = session.get("name")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("home"))

    return render_template("room.html", code=room, name=name)

# Event handler for receiving messages
@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return 
    
    content = {
        "name": session.get("name"),
        "message": data,
        "memberCount": rooms[room]['members']
    }
    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')} {data}")

# Event handler for new connections
@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return
    
    join_room(room)
    send({"message": "", "memberCount": rooms[room]["members"]}, to=room)
    rooms[room]["members"] += 1
    print(f"{name} joined room {room}")

# Event handler for disconnections
@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]
    
    send({"message": "", "memberCount": rooms[room]["members"] - 1}, to=room)
    print(f"{name} has left the room {room}")

# Run the application
if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0")
