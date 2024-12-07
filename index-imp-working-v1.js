const express = require("express");
const cors = require("cors");
const multer = require("multer");
const path = require("path");
const { spawn } = require("child_process");
const fs = require("fs");

const app = express();
const port = 5000;

// Enable CORS
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Set up multer for file uploads
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, "uploads/");
  },
  filename: (req, file, cb) => {
    cb(null, Date.now() + path.extname(file.originalname)); // Save with a unique name
  },
});

const upload = multer({ storage: storage });

// Handle file upload and Python processing
app.post("/process-xrd", upload.single("inputFile"), (req, res) => {
  // Log the incoming request data
  console.log("Received request body:", req.body);

  // Ensure the input file is uploaded
  if (!req.file) {
    return res.status(400).json({ error: "No file uploaded" });
  }

  // Prepare arguments for the Python script
  const inputFilePath = path.join(__dirname, "uploads", req.file.filename);
  const outputDir = path.join(__dirname, "outputs");
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir); // Create output directory if it doesn't exist
  }

  const outputFilePathPDF = path.join(outputDir, "output_plot.pdf");
  const outputFilePathImage = path.join(outputDir, "output_plot.png");

  // Log input file and output paths
  console.log(`Processing input file: ${inputFilePath}`);
  console.log(
    `Output will be saved to: ${outputFilePathPDF} and ${outputFilePathImage}`
  );

  // Spawn Python process to process the file
  const pythonProcess = spawn("python", [
    "peakfinding.py", // Ensure the correct path to your Python script
    inputFilePath, // CSV input file
    outputFilePathPDF, // PDF output path
    outputFilePathImage, // PNG output path
  ]);

  pythonProcess.stdout.on("data", (data) => {
    console.log(`stdout: ${data}`);
  });

  pythonProcess.stderr.on("data", (data) => {
    console.error(`stderr: ${data}`);
  });

  pythonProcess.on("close", (code) => {
    if (code !== 0) {
      console.error("Python script execution failed");
      return res.status(500).json({ error: "Python script execution failed" });
    }

    // Send the processed output files back
    res.json({
      message: "XRD processing completed",
      pdfPath: `/outputs/output_plot.pdf`,
      imagePath: `/outputs/output_plot.png`,
    });
  });
});

// Serve output files statically
app.use("/outputs", express.static(path.join(__dirname, "outputs")));

// Start the Express server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
