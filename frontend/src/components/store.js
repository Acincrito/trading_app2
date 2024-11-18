// frontend/src/store/store.js
import { configureStore } from "@reduxjs/toolkit";
import robotsReducer from "./robotsSlice";

const store = configureStore({
    reducer: {
        robots: robotsReducer,
    },
});

export default store;
