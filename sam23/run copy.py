from datetime import datetime, timezone
from zoomus import ZoomClient
from zoomus.util import date_to_str
import json
import pytz

# Initialize the Zoom client
CLIENT_ID = "2VWdkjoQVOCccFFec7jaw"
CLIENT_SECRET = "3wWizHoDNks1WfQNYu1NBCsCCjaJguzG"
ACCOUNT_ID = "iBSoo0_TQ423RP5ZcpEvoQ"
BASE_URI = "https://api.zoom.us/v2"  # Change to EU endpoint if needed

client = ZoomClient(CLIENT_ID, CLIENT_SECRET, ACCOUNT_ID, base_uri=BASE_URI)

def get_adjusted_start_time(date_str, start_time_str):
    # Define the timezone
    tz = pytz.UTC

    # Combine date and start time into a single datetime object
    datetime_str = f"{date_str} {start_time_str}"
    meeting_start_time = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")

    # Localize to UTC
    meeting_start_time = tz.localize(meeting_start_time)

    # Adjust the time (round to the nearest hour)
    adjusted_start_time = meeting_start_time.replace(minute=0, second=0, microsecond=0)

    # Return the adjusted start time in ISO format
    return adjusted_start_time.isoformat()

# Example data
table_data = [
    {"Date": "2024-09-17", "Meeting Name": "Classes Grade -AI #1", "User List": "anujd0009@gmail.com, rohan@igebra.ai, chiranjeevi@igebra.ai, anuj@igebra.ai", "Start Time": "10:30", "Duration": "30", "Additional Notes": "test-app and teach"},
    {"Date": "2024-09-18", "Meeting Name": "AI Creative", "User List": "anujd0009@gmail.com, rohan@igebra.ai, chiranjeevi@igebra.ai, anuj@igebra.ai", "Start Time": "11:00", "Duration": "31", "Additional Notes": "should be recurring run"},
    {"Date": "2024-09-19", "Meeting Name": "Classes Grade -AI #!", "User List": "anujd0009@gmail.com, rohan@igebra.ai, chiranjeevi@igebra.ai, anuj@igebra.ai", "Start Time": "13:00", "Duration": "32", "Additional Notes": "must enable zoom apps"},
]

# Loop through each meeting entry
for entry in table_data:
    date_str = entry["Date"]
    start_time_str = entry["Start Time"]
    meeting_name = entry["Meeting Name"]
    duration = int(entry["Duration"])

    # Get the adjusted start time
    adjusted_start_time_iso = get_adjusted_start_time(date_str, start_time_str)
    
    # Convert ISO format to datetime for Zoom API
    meeting_start_time = datetime.fromisoformat(adjusted_start_time_iso)

    # Create a meeting
    meeting_response = client.meeting.create(
        user_id='me',
        topic=meeting_name,
        type=2,  # Scheduled meeting
        start_time=meeting_start_time,  # Pass the datetime object directly
        duration=duration,  # Duration in minutes
        timezone='UTC'
    )

    # Handle the response
    try:
        if meeting_response.status_code == 201:
            meeting_details = json.loads(meeting_response.content)
            print(f"Meeting created successfully: {meeting_details}")
        else:
            print(f"Failed to create meeting. Status code: {meeting_response.status_code}")
            print(f"Response content: {meeting_response.content}")
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON response: {e}")
        print(f"Response content: {meeting_response.content}")
