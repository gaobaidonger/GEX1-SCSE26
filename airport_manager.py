######################## IMPORTANT ########################
"""Do not rename the variables or functions.
Do not change the function parameters.
Do not add input() calls inside airport_manager.py.
The file must be importable by the tests.
"""
###########################################################


# A tuple is used for fixed airport information.
airport_info = ("OUL", 1, "14-09-2026")

# Sets are appropriate here because membership checking is the main operation.
allowed_gates = {"A1", "A2", "A3", "A4", "B1", "B2"}
restricted_destinations = {"Moscow", "Pyongyang"}

# Flights are stored in a dictionary keyed by flight number. Each flight is
# itself a dictionary, and every passenger manifest is a list.
flights = {
    "AY450": {
        "destination": "Helsinki",
        "departure": "08:30",
        "gate": "A2",
        "capacity": 5,
        "passengers": ["Alice Wong", "David Kim", "Fatima Ali"],
    },
    "SK271": {
        "destination": "Stockholm",
        "departure": "10:15",
        "gate": "B1",
        "capacity": 4,
        "passengers": ["Chen Wei", "George Smith"],
    },
    "LH2491": {
        "destination": "Munich",
        "departure": "12:40",
        "gate": "A4",
        "capacity": 5,
        "passengers": ["Hana Lee", "Maria Garcia", "Noah Wilson"],
    },
}


def find_flight(flights, flight_number):
    """Return the actual dictionary key for a flight, ignoring case/spaces."""
    normalized = str(flight_number).strip().casefold()

    for key in flights:
        if str(key).strip().casefold() == normalized:
            return key

    return None


def passenger_exists(passengers, passenger_name):
    """Return True if passenger_name occurs in passengers, case-insensitively."""
    normalized = str(passenger_name).strip().casefold()

    return any(
        str(passenger).strip().casefold() == normalized
        for passenger in passengers
    )


def check_in_passenger(
    flights,
    flight_number,
    passenger_name,
    restricted_destinations
):
    """Check a passenger into a flight and return the required status string."""
    flight_key = find_flight(flights, flight_number)

    if flight_key is None:
        return "FLIGHT_NOT_FOUND"

    clean_name = str(passenger_name).strip()
    if not clean_name:
        return "EMPTY_NAME"

    flight = flights[flight_key]

    if passenger_exists(flight["passengers"], clean_name):
        return "DUPLICATE"

    if len(flight["passengers"]) >= flight["capacity"]:
        return "FULL"

    restricted_normalized = {
        str(destination).strip().casefold()
        for destination in restricted_destinations
    }
    if str(flight["destination"]).strip().casefold() in restricted_normalized:
        return "RESTRICTED"

    # Store names in a clean, readable form. This also normalizes all-lowercase
    # or all-uppercase input used by the exercise tests.
    flight["passengers"].append(clean_name.title())
    return "OK"


def remove_passenger(
    flights,
    flight_number,
    passenger_name
):
    """Remove a passenger from a flight, using case-insensitive matching."""
    flight_key = find_flight(flights, flight_number)

    if flight_key is None:
        return "FLIGHT_NOT_FOUND"

    target = str(passenger_name).strip().casefold()
    passengers = flights[flight_key]["passengers"]

    for index, passenger in enumerate(passengers):
        if str(passenger).strip().casefold() == target:
            passengers.pop(index)
            return "OK"

    return "PASSENGER_NOT_FOUND"


def change_gate(
    flights,
    flight_number,
    new_gate,
    allowed_gates
):
    """Change a flight gate if both the flight and requested gate are valid."""
    flight_key = find_flight(flights, flight_number)

    if flight_key is None:
        return "FLIGHT_NOT_FOUND"

    normalized_gate = str(new_gate).strip().casefold()
    matched_gate = None

    for gate in allowed_gates:
        if str(gate).strip().casefold() == normalized_gate:
            matched_gate = gate
            break

    if matched_gate is None:
        return "INVALID_GATE"

    flights[flight_key]["gate"] = matched_gate
    return "OK"


def flight_status(flight):
    """Return AVAILABLE, ALMOST FULL, or FULL from current occupancy."""
    passenger_count = len(flight["passengers"])
    capacity = flight["capacity"]

    if passenger_count >= capacity:
        return "FULL"

    if passenger_count / capacity >= 0.75:
        return "ALMOST FULL"

    return "AVAILABLE"


def sorted_manifest(
    flights,
    flight_number
):
    """Return a new sorted passenger list, or None when flight is not found."""
    flight_key = find_flight(flights, flight_number)

    if flight_key is None:
        return None

    return sorted(flights[flight_key]["passengers"])


def total_passengers(flights):
    """Return the total passenger count across every flight."""
    return sum(len(flight["passengers"]) for flight in flights.values())


def any_full_flight(flights):
    """Return True when at least one flight has reached its capacity."""
    return any(
        len(flight["passengers"]) >= flight["capacity"]
        for flight in flights.values()
    )


def all_flights_have_passengers(flights):
    """Return True when every flight has at least one passenger."""
    return all(
        len(flight["passengers"]) > 0
        for flight in flights.values()
    )