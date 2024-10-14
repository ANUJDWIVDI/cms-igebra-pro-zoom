// /components/MeetingList.js
import { useEffect, useState } from 'react';

const MeetingList = ({ meetings }) => {
    if (meetings.length === 0) {
        return <p>No meetings created yet.</p>;
    }

    return (
        <ul>
            {meetings.map((meeting, index) => (
                <li key={index}>
                    <strong>{meeting.topic}</strong> - {new Date(meeting.start_time).toLocaleString()}
                </li>
            ))}
        </ul>
    );
};

export default MeetingList;
