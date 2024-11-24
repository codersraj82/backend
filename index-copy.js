const express = require("express");
const cors = require("cors");
const multer = require("multer");
const path = require("path");
const fs = require("fs");

const app = express();
const PORT = 5000;

// Middleware
// app.use(cors());
// Enable CORS for your frontend

app.use(
  cors({
    origin: ["http://localhost:3000", "https://xrd-4bgx.onrender.com/"], // URL of your deployed React app
    methods: ["GET", "POST", "PUT", "DELETE"], // Allowed HTTP methods
    credentials: true, // Optional: Include cookies in requests if needed
  })
);

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// File upload setup
// const uploadDir = path.join(__dirname, "uploads");
// if (!fs.existsSync(uploadDir)) {
//   fs.mkdirSync(uploadDir);
// }
const uploadDir = path.join(__dirname, "tmp/uploads");
if (!fs.existsSync(uploadDir)) {
  fs.mkdirSync(uploadDir, { recursive: true });
}

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, "uploads/"); // Save files to 'uploads' folder
  },
  filename: (req, file, cb) => {
    const uniqueSuffix = Date.now() + "-" + Math.round(Math.random() * 1e9);
    cb(
      null,
      file.fieldname + "-" + uniqueSuffix + path.extname(file.originalname)
    );
  },
});

const upload = multer({
  storage,
  limits: { fileSize: 50 * 1024 * 1024 }, // 50 MB limit
});

// Routes
app.post("/upload", upload.single("file"), (req, res) => {
  if (!req.file) {
    return res.status(400).json({ message: "No file uploaded" });
  }

  console.log("File metadata:", req.file);
  res.status(200).json({ message: "File uploaded successfully!" });
});

app.get("/upload", (req, res) => {
  res.send("This route only supports POST requests for file uploads.");
});

app.get("/", (req, res) => {
  res.send("Hello, World!");
});
// Serve uploaded files statically (optional)
app.use("/uploads", express.static(uploadDir));

// Start server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
