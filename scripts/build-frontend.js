const fs = require("node:fs");
const path = require("node:path");

const apiUrl = process.env.RECIPE_API_URL?.trim();
if (!apiUrl) {
  throw new Error(
    "RECIPE_API_URL is required. Set it to the deployed Render API URL in the Vercel project settings."
  );
}

let parsedApiUrl;
try {
  parsedApiUrl = new URL(apiUrl);
} catch {
  throw new Error("RECIPE_API_URL must be a valid absolute URL.");
}

if (parsedApiUrl.protocol !== "https:" && parsedApiUrl.hostname !== "localhost") {
  throw new Error("RECIPE_API_URL must use HTTPS outside localhost.");
}

const projectRoot = path.resolve(__dirname, "..");
const frontendPath = path.join(projectRoot, "frontend");
const outputPath = path.join(projectRoot, "dist");

fs.rmSync(outputPath, { recursive: true, force: true });
fs.cpSync(frontendPath, outputPath, { recursive: true });
fs.writeFileSync(
  path.join(outputPath, "config.js"),
  `window.RECIPE_API_URL = ${JSON.stringify(parsedApiUrl.origin)};\n`
);
