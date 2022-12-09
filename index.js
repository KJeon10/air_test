import express from "express";
import { spawn } from "child_process";
import path from "path";

const app = express();
const __dirname = path.resolve();
app.get("/show", (req, res) => {
  // Spawn a new child process to run the python code
  const pyProc = spawn("python3", ["generate_png.py"]);

  // Listen for any errors from the python code
  pyProc.stderr.on("data", (data) => {
    console.error(`Error: ${data}`);
  });

  // Once the python code has finished running, send the generated png file to the response
  pyProc.on("close", (code) => {
    res.sendFile(`${__dirname}/foo.png`, (err) => {
      if (err) {
        console.error(`Error sending file: ${err}`);
      }
    });
  });
});

app.listen(80, () => {
  console.log("Express server listening on port 3000");
});
