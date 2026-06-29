from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

@app.route("/", methods=["GET"])
def welcome():
    return jsonify({"message": "Welcome to the Events API"}), 200

@app.route("/events", methods=["GET"])
def get_events():
    return jsonify([event.to_dict() for event in events]), 200

# TODO: Task 1 - Define the Problem
# Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()

    if not data or "title" not in data or not isinstance(data["title"], str):
        return jsonify({"error": "Request body must include a title."}), 400

    next_id = max((event.id for event in events), default=0) + 1
    new_event = Event(next_id, data["title"])
    events.append(new_event)

    return jsonify(new_event.to_dict()), 201

# TODO: Task 1 - Define the Problem
# Update the title of an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    data = request.get_json()

    if not data or "title" not in data or not isinstance(data["title"], str):
        return jsonify({"error": "Request body must include a title."}), 400

    for event in events:
        if event.id == event_id:
            event.title = data["title"]
            return jsonify(event.to_dict()), 200

    return jsonify({"error": "Event not found."}), 404

# TODO: Task 1 - Define the Problem
# Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    for index, event in enumerate(events):
        if event.id == event_id:
            events.pop(index)
            return "", 204

    return jsonify({"error": "Event not found."}), 404

if __name__ == "__main__":
    app.run(debug=True)
