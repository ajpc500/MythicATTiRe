import json, sys
from datetime import datetime
from uuid import uuid4 as uuid

# Util function to convert timestamps to ISO8601 format
def convert_to_iso8601(timestamp):
    return datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S Z").strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + 'Z'

# Function to convert single callback input JSON to ATTIRE format
def convert_to_attire(input_data):
    attire_json = {
        "attire-version": "1.1",
        "execution-data": {
            "execution-command": "Converted from provided JSON",
            "execution-id": str(uuid()),
            "execution-source": "mythic_admin",
            "execution-category": {
                "name": "Mythic",
                "abbreviation": "MYTHIC"
            },
            "target": {
                "host": input_data["host"],
                "ip": input_data["ips"][0],
                "path": "",
                "user": input_data["user"]
            },
            "time-generated": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + 'Z'
        },
        "procedures": []
    }
    
    for task in input_data["tasks"]:
        if task["start_time"] == "N/A" and task["end_time"] == "N/A":
            # naively assuming this is a top-level task that triggers subtasks that do the real work
            # or it's a server-side task that doesn't have a start/end time (e.g. help command)
            continue

        procedure = {
            "procedure-name": task["command_name"],
            "procedure-description": f"Task executed by {input_data['user']} on host {input_data['host']}",
            "procedure-id": {
                "type": "guid",
                "id": str(uuid())
            },
            "mitre-technique-id": task["mitre"][0] if task["mitre"] else "",
            "order": task["display_id"],
            "steps": []
        }
        
        step = {
            "command": f"{task['command_name']} {task['display_params']}",
            "executor": "unknown",
            "order": task["display_id"],
            "output": [{"content": out, "level": "STDOUT", "type": "console"} for out in task["output"]],
            "time-start": convert_to_iso8601(task["start_time"]),
            "time-stop": convert_to_iso8601(task["end_time"])
        }
        procedure["steps"].append(step)
        attire_json["procedures"].append(procedure)
    
    return attire_json

# Read input JSON from the first command-line argument
if len(sys.argv) < 2:
    print("Usage: mythicATTiRe.py <input_json_file>")
    sys.exit(1)

input_json_file = sys.argv[1]

# Input JSON data
try:
  input_json = json.loads(open(input_json_file, "r").read())
except FileNotFoundError:
  print("Failed to open JSON input file")
  sys.exit(1)
except json.JSONDecodeError:
  print("Failed to parse input JSON")
  sys.exit(1)

if not input_json:
  print("No input JSON to process")
  sys.exit(1)

for callback in input_json["activity"][0]["callbacks"]:
    # Convert the input JSON to ATTIRE format
    attire_json = convert_to_attire(callback)
    out_file_name = f"ATTiRe_{callback["report_callback_id"]}_{sys.argv[1].replace(' ','_')}"

    with open(out_file_name, "w") as attire_output:
        attire_output.write(json.dumps(attire_json))
    print("[+] Created ATTiRe JSON file: " + out_file_name)