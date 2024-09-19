// /pages/api/create-meeting.js
import axios from 'axios';

const ZOOM_BASE_URL = 'https://api.zoom.us/v2';
const ZOOM_JWT_TOKEN = 'YOUR_ZOOM_JWT_TOKEN';  

export default async function handler(req, res) {
    if (req.method === 'POST') {
        const { date, meetingName, userList, startTime, duration } = req.body;

        try {
            // Prepare the meeting data
            const meetingDateTime = `${date}T${startTime}:00Z`; // Format the date and time to ISO

            const response = await axios.post(
                `${ZOOM_BASE_URL}/users/me/meetings`,
                {
                    topic: meetingName,
                    type: 2,  // Scheduled meeting
                    start_time: meetingDateTime,
                    duration: parseInt(duration),
                    timezone: 'UTC'
                },
                {
                    headers: {
                        'Authorization': `Bearer ${ZOOM_JWT_TOKEN}`,
                        'Content-Type': 'application/json'
                    }
                }
            );

            res.status(201).json(response.data);
        } catch (error) {
            console.error('Zoom API error:', error.response?.data || error.message);
            res.status(500).json({ error: 'Failed to create Zoom meeting' });
        }
    } else {
        res.status(405).json({ message: 'Method Not Allowed' });
    }
}
