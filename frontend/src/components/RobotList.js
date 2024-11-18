// frontend/src/components/RobotList.js
import React, { useState } from "react";
import EditRobotForm from "./EditRobotForm";
import { useDispatch, useSelector } from "react-redux";
import { updateRobot } from "../store/robotsSlice";

const RobotList = () => {
    const robots = useSelector((state) => state.robots);
    const dispatch = useDispatch();

    const [selectedRobot, setSelectedRobot] = useState(null);
    const [isEditModalOpen, setIsEditModalOpen] = useState(false);

    const handleEditClick = (robot) => {
        setSelectedRobot(robot);
        setIsEditModalOpen(true);
    };

    const handleSave = (updatedRobot) => {
        dispatch(updateRobot(updatedRobot));
        setIsEditModalOpen(false);
    };

    return (
        <div>
            <h2>Lista de Robôs</h2>
            <ul>
                {robots.map((robot) => (
                    <li key={robot.id}>
                        <span>{robot.name} - {robot.strategy}</span>
                        <button onClick={() => handleEditClick(robot)}>Editar</button>
                    </li>
                ))}
            </ul>

            {isEditModalOpen && selectedRobot && (
                <div className="modal">
                    <EditRobotForm
                        robot={selectedRobot}
                        onSave={handleSave}
                        onClose={() => setIsEditModalOpen(false)}
                    />
                </div>
            )}
        </div>
    );
};

export default RobotList;
