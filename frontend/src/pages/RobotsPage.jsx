import React, { useEffect, useState } from 'react';
import axios from 'axios';
import RobotCard from '../components/RobotCard';

function RobotsPage() {
    const [robots, setRobots] = useState([]);

    useEffect(() => {
        const fetchRobots = async () => {
            const response = await axios.get('/api/robots');
            setRobots(response.data);
        };

        fetchRobots();
    }, []);

    return (
        <div>
            <h1>Robôs de Trading</h1>
            {robots.map(robot => (
                <RobotCard key={robot.id} robot={robot} />
            ))}
        </div>
    );
}

export default RobotsPage;
