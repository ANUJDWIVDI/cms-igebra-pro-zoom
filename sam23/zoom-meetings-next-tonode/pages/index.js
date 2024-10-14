// /pages/index.js
import { useState } from 'react';
import MeetingForm from './components/MeetingForm';
import MeetingList from './components/MeetingList';

const Home = () => {
    const [meetings, setMeetings] = useState([]);

    const handleMeetingCreated = (newMeeting) => {
        setMeetings([...meetings, newMeeting]);
    };

    return (
        <div>
            <h1>Create a Zoom Meeting</h1>
            <MeetingForm onMeetingCreated={handleMeetingCreated} />
            <h2>Created Meetings</h2>
            <MeetingList meetings={meetings} />
        </div>
    );
};

export default Home;
