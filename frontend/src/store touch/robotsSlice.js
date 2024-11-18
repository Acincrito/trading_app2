// frontend/src/store/robotsSlice.js
import { createSlice } from "@reduxjs/toolkit";

const robotsSlice = createSlice({
    name: "robots",
    initialState: [
        { id: 1, name: "Robo 1", strategy: "Estratégia A" },
        { id: 2, name: "Robo 2", strategy: "Estratégia B" },
    ],
    reducers: {
        updateRobot: (state, action) => {
            const { id, name, strategy } = action.payload;
            const existingRobot = state.find((robot) => robot.id === id);
            if (existingRobot) {
                existingRobot.name = name;
                existingRobot.strategy = strategy;
            }
        },
    },
});

export const { updateRobot } = robotsSlice.actions;

export default robotsSlice.reducer;
