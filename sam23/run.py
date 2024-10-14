from datetime import datetime, timedelta
import pytz
import json
from zoomus import ZoomClient

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

def get_next_weekday_occurrences(start_date, weekday_name, num_occurrences):
    # Map weekday names to numbers (Monday = 0, Sunday = 6)
    weekday_map = {
        "Monday": 0, "Tuesday": 1, "Wednesday": 2,
        "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6
    }
    
    # Convert start date string to datetime object
    current_date = datetime.strptime(start_date, "%Y-%m-%d")
    
    # Find the weekday number
    target_weekday = weekday_map[weekday_name]
    
    # Calculate occurrences
    occurrences = []
    while len(occurrences) < num_occurrences:
        # If the current date matches the target weekday, add it to the list
        if current_date.weekday() == target_weekday:
            occurrences.append(current_date)
        
        # Move to the next day
        current_date += timedelta(days=1)
    
    return occurrences

# Example data
table_data = [
    {"Date": "2024-09-17", "Meeting Name": "Classes Grade -AI #1", "User List": "anujd0009@gmail.com, rohan@igebra.ai", "Start Time": "10:30", "Duration": "30", "Day": "Monday", "Occurrences": 3},
    {"Date": "2024-09-18", "Meeting Name": "AI Creative", "User List": "anujd0009@gmail.com, rohan@igebra.ai", "Start Time": "11:00", "Duration": "31", "Day": "Wednesday", "Occurrences": 2},
]

# Loop through each meeting entry and create recurring meetings
for entry in table_data:
    start_date = entry["Date"]
    start_time_str = entry["Start Time"]
    meeting_name = entry["Meeting Name"]
    duration = int(entry["Duration"])
    weekday_name = entry["Day"]
    num_occurrences = int(entry["Occurrences"])
    
    # Get the next occurrences for the specified day
    occurrences = get_next_weekday_occurrences(start_date, weekday_name, num_occurrences)

    # Loop through the occurrences and create meetings
    for occurrence in occurrences:
        occurrence_str = occurrence.strftime("%Y-%m-%d")
        adjusted_start_time_iso = get_adjusted_start_time(occurrence_str, start_time_str)
        meeting_start_time = datetime.fromisoformat(adjusted_start_time_iso)
        
        # Create a Zoom meeting for each occurrence
        meeting_response = client.meeting.create(
            user_id='me',
            topic=meeting_name,
            type=2,  # Scheduled meeting
            start_time=meeting_start_time,
            duration=duration,  # Duration in minutes
            timezone='UTC'
        )

        # Handle the response
        try:
            if meeting_response.status_code == 201:
                meeting_details = json.loads(meeting_response.content)
                print(f"Meeting created successfully for {occurrence_str}: {meeting_details}")
            else:
                print(f"Failed to create meeting for {occurrence_str}. Status code: {meeting_response.status_code}")
                print(f"Response content: {meeting_response.content}")
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON response: {e}")
            print(f"Response content: {meeting_response.content}")
