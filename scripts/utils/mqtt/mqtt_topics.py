

def alert_topic(machine_id):
    return f"factory/{machine_id}/alerts"

def sensor_topic(line, machine_id):
    return f"factory/{line}/{machine_id}"
