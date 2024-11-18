// frontend/src/components/EditRobotForm.js

import React, { useState } from "react";

const EditRobotForm = ({ robot, onSave }) => {
    const [name, setName] = useState(robot.name);
    const [strategy, setStrategy] = useState(robot.strategy);

    const handleSubmit = (e) => {
        e.preventDefault();
        onSave({ name, strategy });  // Envia os dados atualizados para o backend
    };

    return (
        <form onSubmit={handleSubmit}>
            <div className="form-group">
                <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="Nome do Robô"
                    required
                    className="form-control"
                />
            </div>
            <div className="form-group">
                <input
                    type="text"
                    value={strategy}
                    onChange={(e) => setStrategy(e.target.value)}
                    placeholder="Estratégia"
                    required
                    className="form-control"
                />
            </div>
            <div>
                <button type="submit" className="btn btn-primary">Salvar</button>
            </div>
        </form>
    );
};

export default EditRobotForm;
