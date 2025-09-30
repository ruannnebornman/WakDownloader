import os
import subprocess

# Ensure db directory exists
os.makedirs('db', exist_ok=True)



# Run all downloader scripts
subprocess.run(['python3', 'scripts/wakfu_armor_downloader.py'], check=True)
subprocess.run(['python3', 'scripts/wakfu_weapon_downloader.py'], check=True)
subprocess.run(['python3', 'scripts/wakfu_monster_downloader.py'], check=True)
subprocess.run(['python3', 'scripts/wakfu_resource_downloader.py'], check=True)

print("Databases generated in db/. Use a SQLite viewer or the inspect_db.py script to browse the data.")
