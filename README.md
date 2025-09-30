# WakDownloader


This project downloads armor, weapon, monster, and resource data from the Wakfu encyclopedia and stores them in local SQLite databases for easy querying and analysis.


## Structure
- `scripts/wakfu_armor_downloader.py`: Scrapes the Wakfu encyclopedia and generates the armor database in `db/wakfu_armors.db`.
- `scripts/wakfu_weapon_downloader.py`: Scrapes the Wakfu encyclopedia and generates the weapon database in `db/wakfu_weapons.db`.
- `scripts/wakfu_monster_downloader.py`: Scrapes the Wakfu encyclopedia and generates the monster database in `db/wakfu_monsters.db`.
- `scripts/wakfu_resource_downloader.py`: Scrapes the Wakfu encyclopedia and generates the resource database in `db/wakfu_resources.db`.
- `db/`: Folder where all SQLite databases are stored.
- `main.py`: Python script to run all downloaders and generate all databases.

## Usage
1. Ensure you have Python 3 and pip installed.
2. Install dependencies:
	```bash
	pip install -r requirements.txt
	```

3. Run the main script:
	```bash
	python3 main.py
	```
	This will:
	- Create the `db/` folder if it doesn't exist
	- Scrape the armor data and generate `db/wakfu_armors.db`
	- Scrape the weapon data and generate `db/wakfu_weapons.db`
	- Scrape the monster data and generate `db/wakfu_monsters.db`
	- Scrape the resource data and generate `db/wakfu_resources.db`

4. To browse the databases, use a SQLite extension in VS Code or any SQLite viewer.


## Data format

- **Armor and Weapons** (`db/wakfu_armors.db`, `db/wakfu_weapons.db`):
	- `id`: The item's unique ID from the Wakfu encyclopedia URL
	- `name`: The name of the item
	- `url`: Direct link to the encyclopedia entry
	- `type`: The type (e.g., Helmet, Sword, Dagger)
	- `level`: The level requirement
	- `bonuses`: A JSON array of bonus strings for easy programmatic use

- **Monsters** (`db/wakfu_monsters.db`):
	- `id`: The monster's unique ID from the encyclopedia URL
	- `name`: The monster's name
	- `url`: Direct link to the encyclopedia entry
	- `family`: Monster family
	- `level`: Level string (may include ranges or text)
	- `drops`: JSON array of drop names
	- `harvesting`: JSON array of harvesting options

- **Resources** (`db/wakfu_resources.db`):
	- `id`: The resource's unique ID from the encyclopedia URL
	- `name`: The resource's name
	- `url`: Direct link to the encyclopedia entry
	- `type`: Resource type (e.g., Monster Resource, Plant, etc.)
	- `level`: The level requirement
