// /components/MeetingForm.js
import { useState } from 'react';
import axios from 'axios';

const MeetingForm = ({ onMeetingCreated }) => {
    const [formData, setFormData] = useState({
        date: '',
        meetingName: '',
        userList: '',
        startTime: '',
        duration: ''
    });

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await axios.post('/api/create-meeting', formData);
            onMeetingCreated(response.data); // Pass the meeting data to the parent component
            alert('Meeting created successfully!');
        } catch (error) {
            console.error('Error creating meeting:', error);
            alert('Failed to create meeting');
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <label>Date:</label>
            <input type="date" name="date" value={formData.date} onChange={handleChange} required />

            <label>Meeting Name:</label>
            <input type="text" name="meetingName" value={formData.meetingName} onChange={handleChange} required />

            <label>User List (comma separated):</label>
            <input type="text" name="userList" value={formData.userList} onChange={handleChange} required />

            <label>Start Time (HH:MM):</label>
            <input type="time" name="startTime" value={formData.startTime} onChange={handleChange} required />

            <label>Duration (in minutes):</label>
            <input type="number" name="duration" value={formData.duration} onChange={handleChange} required />

            <button type="submit">Create Meeting</button>
        </form>
    );
};

export default MeetingForm;
