const express = require("express");
const cors = require("cors");
const multer = require("multer");
const path = require("path");
const fs = require("fs");
const { PythonShell } = require("python-shell");
const { spawn } = require("child_process");

const app = express();
const PORT = 5000;

// Middleware
const corsOptions = {
  origin: "*",
  methods: ["GET", "POST", "PUT", "DELETE"],
  credentials: true,
  allowedHeaders: ["Origin", "X-Requested-With", "Content-Type", "Accept"],
};
app.use(cors(corsOptions));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// File upload directory
const uploadDir = path.join(__dirname, "uploads");
const outputDir = path.join(__dirname, "outputs");
if (!fs.existsSync(uploadDir)) fs.mkdirSync(uploadDir, { recursive: true });
if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });

// Multer setup
const storage = multer.diskStorage({
  destination: (req, file, cb) => cb(null, uploadDir),
  filename: (req, file, cb) => {
    const uniqueSuffix = Date.now() + "-" + Math.round(Math.random() * 1e9);
    cb(
      null,
      `${file.fieldname}-${uniqueSuffix}${path.extname(file.originalname)}`
    );
  },
});
const upload = multer({ storage, limits: { fileSize: 50 * 1024 * 1024 } });

// Routes
app.get("/upload", (req, res) => {
  fs.readdir(uploadDir, (err, files) => {
    if (err) {
      console.error("Error reading directory:", err);
      return res.status(500).json({ message: "Unable to list files." });
    }
    console.log("Files found:", files);
    res.json(files);
  });
});

// Upload a file
app.post("/upload", upload.single("file"), (req, res) => {
  if (!req.file) return res.status(400).json({ message: "No file uploaded" });
  res
    .status(200)
    .json({ message: "File uploaded successfully!", file: req.file.filename });
});
// fetch uploaded file
app.get("/upload/:fileName", (req, res) => {
  const { fileName } = req.params;

  // Validate the fileName to prevent directory traversal attacks
  if (fileName.includes("..") || fileName.includes("/")) {
    console.error("Invalid file name:", fileName);
    return res.status(400).json({ error: "Invalid file name" });
  }

  const filePath = path.join(uploadDir, fileName);

  console.log("Requested file:", fileName);
  console.log("File path:", filePath);

  // Read the file
  fs.readFile(filePath, "utf8", (err, data) => {
    if (err) {
      if (err.code === "ENOENT") {
        console.error("File not found:", fileName);
        return res.status(404).json({ error: "File not found" });
      }

      console.error("Error reading file:", err.message);
      return res.status(500).json({ error: "Unable to read the file" });
    }

    // Send the file content
    res.type("text/plain").send(data);
  });
});

// Process a file using Python
app.post("/process/:fileName", (req, res) => {
  const { fileName } = req.params;
  const filePath = path.join(__dirname, "uploads", fileName); // Ensure this points to the uploaded file location
  const outputDir = path.join(__dirname, "outputs"); // Define the output directory

  // Use PythonShell to run the script
  const pythonProcess = PythonShell.run(
    "./python_scripts/process_file.py",
    {
      pythonPath: "./venv/bin/python", // Point to virtual environment Python
      args: [filePath, outputDir],
    },
    (err, results) => {
      if (err) {
        console.error("Error running Python script:", err);
        return res.status(500).json({ error: "Failed to process the file." });
      }
      console.log("Python script results:", results);
      res
        .status(200)
        .json({ message: "File processed successfully!", results });
    }
  );

  // Ensure proper error handling for process exit
  pythonProcess.on("exit", (code) => {
    if (code !== 0) {
      console.error(`Python process exited with code ${code}`);
      res.status(500).json({ error: "Python script execution failed." });
    }
  });
});

// List all output files
app.get("/outputs", (req, res) => {
  fs.readdir(outputDir, (err, files) => {
    if (err)
      return res.status(500).json({ error: "Failed to list output files." });
    res.json(files);
  });
});

// Download an output file
app.get("/outputs/:fileName", (req, res) => {
  const { fileName } = req.params;
  const filePath = path.join(outputDir, fileName);

  if (!fs.existsSync(filePath))
    return res.status(404).json({ error: "File not found" });

  res.download(filePath, fileName);
});

// Delete an uploaded file
app.delete("/upload/:fileName", (req, res) => {
  const { fileName } = req.params;
  const filePath = path.join(uploadDir, fileName);

  if (!fs.existsSync(filePath))
    return res.status(404).json({ error: "File not found" });

  fs.unlink(filePath, (err) => {
    if (err)
      return res.status(500).json({ error: "Failed to delete the file." });
    res.status(200).json({ message: "File deleted successfully!" });
  });
});

// Delete an output file
app.delete("/outputs/:fileName", (req, res) => {
  const { fileName } = req.params;
  const filePath = path.join(outputDir, fileName);

  if (!fs.existsSync(filePath))
    return res.status(404).json({ error: "File not found" });

  fs.unlink(filePath, (err) => {
    if (err)
      return res.status(500).json({ error: "Failed to delete the file." });
    res.status(200).json({ message: "Output file deleted successfully!" });
  });
});

pythonProcess.on("exit", (code) => {
  if (code === 0) {
    console.log("Python script executed successfully");
    return res.status(200).json({ message: "File processed successfully!" });
  } else {
    console.error(`Python process exited with code ${code}`);
    return res.status(500).json({ error: "Failed to process the file." });
  }
});

// Serve uploaded and output files statically
app.use("/uploads", express.static(uploadDir));
app.use("/outputs", express.static(outputDir));

// Start server
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});