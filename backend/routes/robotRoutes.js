// backend/routes/robotRoutes.js
const express = require("express");
const router = express.Router();
const { getOperationHistory } = require("../controllers/robotController");

router.get("/:robotId/history", getOperationHistory);

module.exports = router;
