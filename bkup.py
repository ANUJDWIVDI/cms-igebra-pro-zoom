
#working
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




'''from datetime import datetime, timedelta
import pytz

def get_adjusted_start_time(table_data, index):
    # Define the timezone
    tz = pytz.UTC

    # Get the entry based on the index
    entry = table_data[index]

    # Extract date and start time
    date_str = entry["Date"]
    start_time_str = entry["Start Time"]

    # Combine date and start time into a single datetime object
    datetime_str = f"{date_str} {start_time_str}"
    meeting_start_time = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")

    # Localize to UTC
    meeting_start_time = tz.localize(meeting_start_time)

    # Adjust the time (round to the nearest hour)
    adjusted_start_time = meeting_start_time.replace(minute=0, second=0, microsecond=0)

    # Return the adjusted start time in ISO format
    return adjusted_start_time.isoformat()

# Example usage
table_data = [
    {"Date": "2024-09-17", "Meeting Name": "Classes Grade -AI #1", "User List": "anujd0009@gmail.com, rohan@igebra.ai, chiranjeevi@igebra.ai, anuj@igebra.ai", "Start Time": "10:30", "Duration": "30", "Additional Notes": "test-app and teach"},
    {"Date": "2024-09-18", "Meeting Name": "AI Creative", "User List": "anujd0009@gmail.com, rohan@igebra.ai, chiranjeevi@igebra.ai, anuj@igebra.ai", "Start Time": "11:00", "Duration": "31", "Additional Notes": "should be recurring run"},
    {"Date": "2024-09-19", "Meeting Name": "Classes Grade -AI #!", "User List": "anujd0009@gmail.com, rohan@igebra.ai, chiranjeevi@igebra.ai, anuj@igebra.ai", "Start Time": "13:00", "Duration": "32", "Additional Notes": "must enable zoom apps"},
]

# Get adjusted time for the second meeting (index 1)
adjusted_time = get_adjusted_start_time(table_data, 1)
print(adjusted_time)
'''


import json
from zoomus import ZoomClient

# Initialize the Zoom client
CLIENT_ID = "2VWdkjoQVOCccFFec7jaw"
CLIENT_SECRET = "3wWizHoDNks1WfQNYu1NBCsCCjaJguzG"
ACCOUNT_ID = "iBSoo0_TQ423RP5ZcpEvoQ"
BASE_URI = "https://api.zoom.us/v2"  # Change to EU endpoint if needed

print("Initializing Zoom client...")
client = ZoomClient(CLIENT_ID, CLIENT_SECRET, ACCOUNT_ID, base_uri=BASE_URI)
print("Zoom client initialized successfully.")

# Define a list of user emails
user_emails = ["anujd0009@gmail.com", "chiranjeevi@igebra.ai", "anuj@igebra.ai"]  # Add more emails if needed
print("User emails defined successfully.")

# Fetch user list
print("Fetching user list...")
user_list_response = client.user.list()
user_list = json.loads(user_list_response.content)
print(f"User list fetched successfully: {user_list}")

# Fetch user details for each email and create user if not existing
for email in user_emails:
    print(f"Fetching details for user: {email}")
    user_found = False
    for user in user_list.get('users', []):
        if user['email'] == email:
            user_found = True
            user_id = user['id']
            print(f"User details for {email}: {user}")
            break
    if not user_found:
        print(f"User with email {email} not found. Creating user...")
        create_user_response = client.user.create(email=email, type=1, first_name=email.split('@')[0], last_name="")
        new_user = json.loads(create_user_response.content)
        print(f"User created successfully: {new_user}")

# Run a simple test to create a meeting
print("Creating a test meeting...")
meeting_response = client.meeting.create(user_id='me', topic='Test Meeting Zoom Integration', type=2)
meeting_details = json.loads(meeting_response.content)
print(f"Test meeting created successfully: {meeting_details}")


'''from datetime import datetime, time
import json
import pandas as pd
from zoomus import ZoomClient

# Initialize the Zoom client
CLIENT_ID = "2VWdkjoQVOCccFFec7jaw"
CLIENT_SECRET = "3wWizHoDNks1WfQNYu1NBCsCCjaJguzG"
ACCOUNT_ID = "iBSoo0_TQ423RP5ZcpEvoQ"
BASE_URI = "https://api.zoom.us/v2"

print("===================================")
print("Initializing Zoom client...")
client = ZoomClient(CLIENT_ID, CLIENT_SECRET, ACCOUNT_ID, base_uri=BASE_URI)
print("Zoom client initialized successfully.")
print("===================================")

# Fetch user list
print("Fetching user list...")
user_list_response = client.user.list()
user_list = json.loads(user_list_response.content)
print("User list fetched successfully.")
print("===================================")
print(f"User list: {json.dumps(user_list, indent=2)}")
print("===================================")

# Read the Excel file
file_path = "autoexcel.xlsx"
print(f"Reading Excel file: {file_path}")
df = pd.read_excel(file_path)
print("Excel file read successfully.")
print("===================================")

# Function to create Zoom meeting
def create_zoom_meeting(meeting_name, start_time, end_time, user_emails, notes):
    print(f"Creating Zoom meeting: {meeting_name}")

    # Ensure that start_time and end_time are datetime objects
    if isinstance(start_time, str):
        start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    if isinstance(end_time, str):
        end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')

    # Convert to ISO 8601 format strings
    start_time_str = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    end_time_str = end_time.strftime('%Y-%m-%dT%H:%M:%SZ')

    meeting_payload = {
        "topic": meeting_name,
        "type": 2,
        "start_time": start_time_str,
        "duration": int((end_time - start_time).total_seconds() / 60),  # Duration in minutes
        "agenda": notes,
        "settings": {
            "host_video": True,
            "participant_video": True,
            "join_before_host": True,
            "mute_upon_entry": True,
            "watermark": True,
            "use_pmi": False,
            "approval_type": 0,
            "audio": "both",
            "auto_recording": "cloud"
        }
    }

    try:
        meeting_response = client.meeting.create(user_id='me', **meeting_payload)
        if meeting_response.status_code == 201:
            meeting_details = json.loads(meeting_response.content)
            meeting_link = meeting_details['join_url']
            return meeting_link, None
        else:
            return None, f"Error creating meeting: {meeting_response.content}"
    except Exception as e:
        return None, str(e)

# Function to check for meeting clashes
def check_for_clashes(existing_meetings, new_start_time, new_end_time):
    clashes = []
    for meeting in existing_meetings:
        if new_start_time < meeting['end_time'] and new_end_time > meeting['start_time']:
            clashes.append(meeting['name'])
    return clashes

# Initialize or add the columns for Zoom link and logs
if 'Zoom Meetings Link' not in df.columns:
    df['Zoom Meetings Link'] = None
if 'Logs' not in df.columns:
    df['Logs'] = None

# Collect existing meetings to check for clashes
existing_meetings = []

# Process each row in the Excel file
for index, row in df.iterrows():
    date = row['Date']
    meeting_name = row['Meeting Name']
    user_list = row['User List'].split(',')
    
    try:
        # Convert string times to datetime.time
        start_time_str = row['Start Time']
        end_time_str = row['End Time']
        
        # Parse times from strings if they are not already datetime.time objects
        if isinstance(start_time_str, str):
            start_time = datetime.strptime(start_time_str, '%H:%M:%S').time()
        else:
            start_time = start_time_str
        
        if isinstance(end_time_str, str):
            end_time = datetime.strptime(end_time_str, '%H:%M:%S').time()
        else:
            end_time = end_time_str
        
        # Combine date with time for start and end
        start_datetime = datetime.combine(date, start_time)
        end_datetime = datetime.combine(date, end_time)
    except Exception as e:
        error_message = f"Error parsing times for row {index + 1}: {e}"
        print(error_message)
        df.at[index, 'Logs'] = json.dumps([error_message])
        continue
    
    notes = row['Additional Notes']
    
    # Check for clashes
    clashes = check_for_clashes(existing_meetings, start_datetime, end_datetime)
    
    if clashes:
        error_message = f"Meeting clashes with: {', '.join(clashes)}"
        print(f"Error: {error_message}")
        df.at[index, 'Logs'] = json.dumps([error_message])
        continue
    
    print(f"Processing row {index + 1}: {meeting_name}")
    print(f"Start Time: {start_datetime}, End Time: {end_datetime}")
    
    # Create Zoom meeting and print meeting link
    meeting_link, error_message = create_zoom_meeting(meeting_name, start_datetime, end_datetime, user_list, notes)
    if meeting_link:
        print(f"Meeting Name: {meeting_name}")
        print(f"Zoom Meeting Link: {meeting_link}")
        print("===================================")
        
        # Update Excel file
        df.at[index, 'Zoom Meetings Link'] = meeting_link
        df.at[index, 'Logs'] = json.dumps([f"Meeting created successfully: {meeting_link}"])
    else:
        df.at[index, 'Logs'] = json.dumps([f"Error creating meeting: {error_message}"])

    # Add current meeting to the existing meetings list
    existing_meetings.append({
        'name': meeting_name,
        'start_time': start_datetime,
        'end_time': end_datetime
    })

# Save the updated Excel file
df.to_excel(file_path, index=False)
print(f"Excel file updated successfully with meeting links and logs only: {file_path}")
print("===================================")
'''