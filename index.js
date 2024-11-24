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

// Configure CORS settings
const corsOptions = {
  origin: "*",
  //[
  //   "http://localhost:3000", // Local frontend URL for dev
  //   "https://xrd-4bgx.onrender.com", // Frontend URL on Render
  // ],
  methods: ["GET", "POST", "PUT", "DELETE"],
  credentials: true, // Allow credentials like cookies to be sent with requests
  allowedHeaders: [
    "Origin",
    "X-Requested-With",
    "Content-Type",
    "Accept",
    "Authorization",
  ], // Specific allowed headers
};

app.use(cors(corsOptions));

// Handle preflight (OPTIONS) requests
app.options("*", (req, res) => {
  res.status(200).end();
});

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

app.options("*", (req, res) => {
  res.sendStatus(200); // Respond with status 200 for OPTIONS requests
});

app.use((req, res, next) => {
  res.header("Access-Control-Allow-Origin", "*"); // Allow all origins or specify the exact origin
  res.header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS"); // Allowed methods
  res.header(
    "Access-Control-Allow-Headers",
    "Origin, Content-Type, X-Requested-With, Accept, Authorization"
  ); // Allowed headers
  res.header("Access-Control-Allow-Credentials", "true"); // Allow credentials if needed
  next();
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
