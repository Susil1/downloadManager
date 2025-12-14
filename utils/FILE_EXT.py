
# 🖼️ Image extensions
images:list[str] = ['.svg', '.png', '.bmp', '.jpg', '.webp', '.tiff', '.ico', '.gif', '.avif', '.jpeg']

# 📄 Document extensions
documents:list[str] = [".pdf", ".doc", ".docx", ".txt", ".odt", ".rtf", ".md", ".epub", ".xls", ".xlsx", ".ppt", ".pptx"]

# 🎥 Video extensions
videos:list[str] = [".mp4", ".mkv", ".avi", ".mov", ".flv", ".wmv", ".webm", ".3gp"]

# 🎵 Audio extensions
audios:list[str] = [".mp3", ".wav", ".aac", ".ogg", ".flac", ".wma", ".m4a"]

# 📦 Archive extensions
archives:list[str] = [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".iso"]

# ⚙️ Executable/script extensions
executables = [
    # Windows
    ".exe", ".msi", ".bat", ".cmd",
    # macOS
    ".app", ".dmg", ".pkg",
    # Linux / Unix
    ".sh", ".bin", ".run", ".AppImage", ".deb", ".rpm",
    # Cross-platform / others
    ".apk", ".jar", ".py"
]
#Web Files
# 🌐 Web-related file extensions
web_files: list[str] = [
    # HTML/CSS/JS
    ".html", ".htm", ".css", ".scss", ".sass", ".less", ".js", ".mjs", ".ts", ".tsx",

    # Template files
    ".ejs", ".hbs", ".mustache", ".pug", ".jinja", ".twig",

    # JSON, XML, YAML
    ".json", ".xml", ".yaml", ".yml",

    # Config/manifest files
    ".env", ".ini", ".conf", ".config", ".manifest", ".webmanifest",

    # Web fonts
    ".woff", ".woff2", ".ttf", ".otf", ".eot",

    # Misc
    ".php", ".asp", ".aspx", ".jsp", ".cfm"
]

# 🧪 Miscellaneous/Other extensions
others:list[str] = [".csv", ".db", ".sqlite3", ".log", ]

# ✅ Optional combined dict
all_extensions:dict[str,list[str]] = {
    "images": images,
    "documents": documents,
    "videos": videos,
    "audios": audios,
    "archives": archives,
    "executables": executables,
    "web_files":web_files,
    "others": others
}