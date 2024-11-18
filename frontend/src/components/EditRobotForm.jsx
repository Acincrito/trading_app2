// frontend/src/components/EditRobotForm.js
import React, { useState } from "react";
import "./EditRobotForm.css";


const EditRobotForm = ({ robot, onSave, onClose }) => {
    const [name, setName] = useState(robot.name || "");
    const [strategy, setStrategy] = useState(robot.strategy || "");

    const handleSubmit = (e) => {
        e.preventDefault();
        onSave({ ...robot, name, strategy });
        onClose();  // Fecha a modal após salvar
    };

    return (
        <div className="edit-robot-form">
            <form onSubmit={handleSubmit}>
                <label>Nome do Robô</label>
                <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="Nome do Robô"
                />
                <label>Estratégia</label>
                <input
                    type="text"
                    value={strategy}
                    onChange={(e) => setStrategy(e.target.value)}
                    placeholder="Estratégia"
                />
                <button type="submit">Salvar</button>
                <button type="button" onClick={onClose}>Cancelar</button>
            </form>
        </div>
    );
};

export default EditRobotForm;
