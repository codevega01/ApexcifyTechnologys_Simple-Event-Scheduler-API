from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# In-memory data store
events = []
event_id_counter = 1

@app.route('/events', methods=['GET'])
def get_events():
    """
    List all events sorted by date.
    """
    sorted_events = sorted(events, key=lambda x: x['date'])
    return jsonify(sorted_events)

@app.route('/events', methods=['POST'])
def add_event():
    """
    Add a new event.
    """
    global event_id_counter
    data = request.get_json()

    # Basic validation
    if not all(k in data for k in ['title', 'date', 'description']):
        return jsonify({'error': 'Missing required fields'}), 400

    title = data['title']
    date_str = data['date']
    description = data['description']

    # Date validation
    try:
        event_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        if event_date < datetime.now().date():
            return jsonify({'error': 'Event date cannot be in the past'}), 400
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

    # Create new event
    new_event = {
        'id': event_id_counter,
        'title': title,
        'date': date_str,
        'description': description
    }
    events.append(new_event)
    event_id_counter += 1

    return jsonify(new_event), 201

if __name__ == '__main__':
    app.run(debug=True)