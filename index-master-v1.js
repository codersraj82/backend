const express = require("express");
const cors = require("cors");
const multer = require("multer");
const path = require("path");
const fs = require("fs");

const app = express();
const PORT = 5000;

// Middleware
const corsOptions = {
  origin: "*",
  //   [
  //   "http://localhost:3000", // Local frontend URL for dev
  //   "https://xrd-4bgx.onrender.com", // Frontend URL on Render
  // ],
  methods: ["GET", "POST", "PUT", "DELETE"],
  credentials: true,
  allowedHeaders: [
    "Origin",
    "X-Requested-With",
    "Content-Type",
    "Accept",
    "Authorization",
  ],
};
app.use(cors(corsOptions));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// File upload directory
const uploadDir = path.join(
  __dirname,
  process.env.FILE_STORAGE_PATH || "./uploads"
);
if (!fs.existsSync(uploadDir)) {
  fs.mkdirSync(uploadDir, { recursive: true });
}

// Multer setup
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, uploadDir); // Use the consistent directory path
  },
  filename: (req, file, cb) => {
    const uniqueSuffix = Date.now() + "-" + Math.round(Math.random() * 1e9);
    cb(
      null,
      `${file.fieldname}-${uniqueSuffix}${path.extname(file.originalname)}`
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
  fs.readdir(uploadDir, (err, files) => {
    if (err) {
      console.error("Error reading directory:", err);
      return res.status(500).json({ message: "Unable to list files." });
    }
    console.log("Files found:", files);
    res.json(files);
  });
});

app.get("/upload/:fileName", (req, res) => {
  const { fileName } = req.params;
  const filePath = path.join(uploadDir, fileName);

  console.log("Requested file:", fileName);
  console.log("File path:", filePath);

  fs.access(filePath, fs.constants.F_OK, (err) => {
    if (err) {
      console.error("File not found:", err);
      return res.status(404).json({ error: "File not found" });
    }

    fs.readFile(filePath, "utf8", (err, data) => {
      if (err) {
        console.error("Error reading file:", err);
        return res.status(500).json({ error: "Unable to read the file" });
      }

      res.type("text/plain").send(data);
    });
  });
});

app.delete("/upload/:fileName", (req, res) => {
  const { fileName } = req.params;
  const filePath = path.join(uploadDir, fileName);

  fs.unlink(filePath, (err) => {
    if (err) {
      console.error("Error deleting file:", err);
      return res.status(500).json({ error: "Failed to delete the file." });
    }

    res.status(200).json({ message: "File deleted successfully!" });
  });
});

// Serve uploaded files statically
app.use("/uploads", express.static(uploadDir));

// Root route
app.get("/", (req, res) => {
  res.send("Hello, World!");
});

// Start server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
