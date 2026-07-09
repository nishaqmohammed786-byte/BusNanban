from flask import Blueprint, render_template, request

search_bp = Blueprint('search', __name__)

@search_bp.route('/bus', methods=['GET'])
def bus():
    # 1. Grab filter selections directly from the user's search form submission
    source = request.args.get('source', 'Kilambakkam').strip()
    destination = request.args.get('destination', 'Guindy').strip()
    bus_type = request.args.get('bus_type', 'Any')

    # 2. Mock Bus Data Repository representing our live MTC inventory matching Kilambakkam -> Guindy line
    all_buses = [
        {
            "number": "51A",
            "type": "AC Deluxe",
            "type_category": "AC",
            "departure": "08:15 AM",
            "arrival": "08:40 AM",
            "duration": "25 mins",
            "fare": 35
        },
        {
            "number": "A1",
            "type": "Deluxe Express",
            "type_category": "Deluxe",
            "departure": "08:30 AM",
            "arrival": "09:00 AM",
            "duration": "30 mins",
            "fare": 18
        },
        {
            "number": "E18",
            "type": "Regular City Bus",
            "type_category": "Normal",
            "departure": "08:45 AM",
            "arrival": "09:20 AM",
            "duration": "35 mins",
            "fare": 12
        }
    ]

    # 3. Filter our dataset based on user's Preferred Bus Comfort type select field
    if bus_type != 'Any':
        filtered_buses = [bus for bus in all_buses if bus['type_category'] == bus_type]
    else:
        filtered_buses = all_buses

    # 4. Hand off variables cleanly down into templates/routes.html for the interactive map/split-view layout
    return render_template(
        'routes.html', 
        buses=filtered_buses, 
        source=source, 
        destination=destination, 
        bus_type=bus_type
    )