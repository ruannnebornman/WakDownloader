import os
import subprocess

# Ensure db directory exists
os.makedirs('db', exist_ok=True)

# Run the downloader script
subprocess.run(['python3', 'scripts/wakfu_armor_downloader.py'], check=True)


print("Database generated in db/wakfu_armors.db. Use a SQLite viewer or the inspect_db.py script to browse the data.")
