import os
import subprocess

ISS_PATH = "DownTube.iss"   # <-- your .iss file name
INNO_COMPILER = r"E:\Softwares\Inno Setup 6\ISCC.exe"

# -----------------------
# 1️⃣ Read & Increment Version
# -----------------------
with open("version.txt", "r") as f:
    version = f.read().strip()

major, minor, patch = map(int, version.split("."))
patch += 1
new_version = f"{major}.{minor}.{patch}"

with open("version.txt", "w") as f:
    f.write(new_version)

print(f"New Version: {new_version}")

# -----------------------
# 2️⃣ Update yt-dlp
# -----------------------
subprocess.run(["pip", "install", "-U", "yt-dlp"])

# -----------------------
# 3️⃣ Clean Old Builds
# -----------------------
if os.path.isdir("build") and os.path.isdir("dist") :
    os.system("rmdir /s /q build")
    os.system("rmdir /s /q dist")

# -----------------------
# 4️⃣ Build EXE
# -----------------------
subprocess.run(["run_script.bat"], shell= True)

# -----------------------
# 5️⃣ Update Version in ISS file
# -----------------------
with open(ISS_PATH, "r") as f:
    iss_content = f.read()

import re
iss_content = re.sub(
    r"AppVersion=.*",
    f"AppVersion={new_version}",
    iss_content
)

with open(ISS_PATH, "w") as f:
    f.write(iss_content)

# -----------------------
# 6️⃣ Build Installer
# -----------------------
subprocess.run([INNO_COMPILER, ISS_PATH])

print("🔥 Full Release Build Complete!")