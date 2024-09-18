from datetime import datetime, timedelta, timezone
from zoomus import ZoomClient
from zoomus.util import date_to_str
import json

# Initialize the Zoom client
CLIENT_ID = "2VWdkjoQVOCccFFec7jaw"
CLIENT_SECRET = "3wWizHoDNks1WfQNYu1NBCsCCjaJguzG"
ACCOUNT_ID = "iBSoo0_TQ423RP5ZcpEvoQ"
BASE_URI = "https://api.zoom.us/v2"  # Change to EU endpoint if needed

client = ZoomClient(CLIENT_ID, CLIENT_SECRET, ACCOUNT_ID, base_uri=BASE_URI)

# Define the meeting start time for tomorrow at 10 AM UTC
meeting_start_time = datetime.now(timezone.utc) + timedelta(days=1)
print(f"Meeting start time: {meeting_start_time}")
meeting_start_time = meeting_start_time.replace(hour=10, minute=0, second=0, microsecond=0)
print(f"Meeting start time (adjusted): {meeting_start_time}")

# Convert the datetime object to a string in the required format
meeting_start_time_str = date_to_str(meeting_start_time)  # Output: "YYYY-MM-DDTHH:MM:SSZ"
print(f"Meeting start time (string): {meeting_start_time_str}")

# Create a meeting
meeting_response = client.meeting.create(
    user_id='me',
    topic='Test Meeting Zoom Integration',
    type=2,  # Scheduled meeting
    start_time=meeting_start_time,  # Pass the datetime object directly
    duration=30,  # Duration in minutes
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
