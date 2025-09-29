# 📁 downloadManager

A Python script that uses the Watchdog library to monitor your **Downloads** folder. It automatically moves files into categorized folders based on their extensions (images, videos, documents, etc.).

---

## 📦 Features

- Automatically organizes files in the Downloads folder
- Categorizes files by extension (e.g., `.jpg` to `Images`, `.mp4` to `Videos`, etc.)
- Skips temporary/incomplete downloads (`.crdownload`, `.part`, `.tmp`)
- Keeps logs of all file movements
- Handles name conflicts with suffixes like `filename (1).ext`

---

## 🛠️ Requirements

- Python 3.10+
- [`watchdog`](https://pypi.org/project/watchdog/)

Install dependencies:

```bash
pip install watchdog
```

---

## 🚀 Usage

Run the script using:

```bash
python scriptD.py
```

The script will:
- Start watching your `Downloads` folder
- Move files into categorized subfolders (e.g., `Documents`, `Videos`, etc.)
- Log activities in `watcher.log`

---

## 📂 Folder Structure

```
downloadManager/
├── kill.bat           # Optional: Used to terminate script if needed
├── run.bat            # Optional: Starts scriptD.py
├── run.vbs            # Optional: Run Python script silently
├── scriptD.py         # Main Watchdog script
├── watcher.log        # File activity logs
└── README.md          # (You're reading it!)
```

---

## ⚙️ Configuration

**Default watched folder**:

```python
WATCH_FOLDER = r"C:\Users\susil\Downloads"
```

Change this path to match your system if needed.

Example for portability:
```python
WATCH_FOLDER = os.path.join(os.environ["USERPROFILE"], "Downloads")
```

---

## 🧠 Future Improvements

- Add support for recursive watching of subdirectories
- Add GUI or CLI flags to customize folders/categories
- Add support for scheduling (e.g., only run during certain hours)

---

## 📜 License

MIT License

---

## 🧾 Log Example (watcher.log)

```
2025-08-03 22:10:21 - Watching folder: C:\Users\susil\Downloads
2025-08-03 22:10:30 - [Created] C:\Users\susil\Downloads\newfile.pdf
2025-08-03 22:10:35 - File Moved : newfile.pdf
```