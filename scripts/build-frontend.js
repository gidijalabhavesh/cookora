const fs = require("node:fs");
const path = require("node:path");

const root = path.resolve(__dirname, "..");
const source = path.join(root, "frontend");
const destination = path.join(root, "dist");
const apiUrl = process.env.RECIPE_API_URL || "";

fs.rmSync(destination, { recursive: true, force: true });
fs.cpSync(source, destination, { recursive: true });
fs.writeFileSync(
  path.join(destination, "config.js"),
  `window.RECIPE_API_URL = ${JSON.stringify(apiUrl)};\n`,
  "utf8",
);