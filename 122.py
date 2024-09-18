import pandas as pd
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

# Load data from Excel spreadsheet
file_path = 'autoexcel.xlsx'  # Update with your file path
df = pd.read_excel(file_path)

# Loop through each meeting entry
for index, row in df.iterrows():
    date_str = row["Date"]
    start_time_str = row["Start Time"]
    meeting_name = row["Meeting Name"]
    duration = int(row["Duration"])

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
            join_url = meeting_details.get("join_url", "")
            
            # Update the DataFrame with the Zoom link
            df.at[index, "Zoom Link"] = join_url
            
            print(f"Meeting created successfully: {meeting_details}")
        else:
            print(f"Failed to create meeting. Status code: {meeting_response.status_code}")
            print(f"Response content: {meeting_response.content}")
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON response: {e}")
        print(f"Response content: {meeting_response.content}")

# Save the updated DataFrame back to the Excel file
df.to_excel(file_path, index=False)
