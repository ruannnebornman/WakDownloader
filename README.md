# WakDownloader

This project downloads all armor data from the Wakfu encyclopedia and stores it in a local SQLite database for easy querying and analysis.

## Structure
- `scripts/wakfu_armor_downloader.py`: Scrapes the Wakfu encyclopedia and generates the database in `db/wakfu_armors.db`.
- `db/`: Folder where the SQLite database is stored.
- `main.py`: Python script to run everything needed to generate the database.

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
	- Print the first 10 rows for inspection

4. To browse the database, use a SQLite extension in VS Code or any SQLite viewer.

## Data format
- Each armor entry includes:
  - `id`: The armor's unique ID from the Wakfu encyclopedia URL
  - `name`: The name of the armor
  - `url`: Direct link to the encyclopedia entry
  - `type`: The type of armor (e.g., Helmet, Boots)
  - `level`: The level requirement
  - `bonuses`: A JSON array of bonus strings for easy programmatic use
