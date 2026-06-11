const fs = require('fs');
const path = require('path');

const source = "C:\\Users\\RUPAM BHARDWAJ\\.gemini\\antigravity\\brain\\da637fac-185c-4e04-98d2-56e684dabf35\\media__1780822061134.png";
const dest = path.join(__dirname, 'header.png');

try {
    fs.copyFileSync(source, dest);
    console.log("=========================================");
    console.log("SUCCESS: Header image copied successfully!");
    console.log("Destination: " + dest);
    console.log("=========================================");
} catch (err) {
    console.error("ERROR: Failed to copy header image.");
    console.error(err);
}
