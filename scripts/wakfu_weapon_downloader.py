import requests
import json
import sqlite3
import time
from bs4 import BeautifulSoup

DB_NAME = 'db/wakfu_weapons.db'
BASE_URL = 'https://www.wakfu.com'
WEAPON_LIST_URL = f'{BASE_URL}/en/mmorpg/encyclopedia/weapons'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS weapons')
    c.execute('''
        CREATE TABLE weapons (
            id INTEGER PRIMARY KEY,
            name TEXT,
            url TEXT,
            type TEXT,
            level INTEGER,
            bonuses TEXT -- JSON array
        )
    ''')
    conn.commit()
    conn.close()

def get_all_weapons():
    weapons = []
    page = 1
    while True:
        url = f"{WEAPON_LIST_URL}?page={page}"
        print(f"Fetching {url}")
        resp = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(resp.text, 'html.parser')
        table = soup.find('table')
        if not table:
            print("No table found on page.")
            return weapons
        tbody = table.find('tbody')
        if not tbody:
            print("No tbody found in table.")
            return weapons
        rows = tbody.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) < 5:
                continue
            name_tag = cols[1].find('a')
            name = name_tag.text.strip() if name_tag else ''
            link = BASE_URL + name_tag['href'] if name_tag and name_tag.has_attr('href') else ''
            weapon_id = None
            if name_tag and name_tag.has_attr('href'):
                parts = name_tag['href'].split('/')
                if len(parts) > 0:
                    id_part = parts[-1].split('-')[0]
                    try:
                        weapon_id = int(id_part)
                    except Exception:
                        weapon_id = None
            type_img_tag = cols[2].find('img') if len(cols) > 2 else None
            type_ = type_img_tag['alt'].strip() if type_img_tag and type_img_tag.has_attr('alt') else ''
            bonuses_lines = [line.strip() for line in cols[3].stripped_strings if line.strip()]
            bonuses = json.dumps(bonuses_lines, ensure_ascii=False)
            level_text = cols[4].text.strip()
            try:
                level = int(level_text.replace('Lvl', '').strip())
            except Exception:
                level = None
            if weapon_id is not None:
                weapons.append({
                    'id': weapon_id,
                    'name': name,
                    'url': link,
                    'type': type_,
                    'level': level,
                    'bonuses': bonuses
                })
        # Only fetch the first page for now (remove this return to enable pagination)
        return weapons

def save_weapon(weapon):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO weapons (id, name, url, type, level, bonuses)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (weapon['id'], weapon['name'], weapon['url'], weapon['type'], weapon['level'], weapon['bonuses']))
    conn.commit()
    conn.close()

def main():
    init_db()
    weapons = get_all_weapons()
    print(f'Found {len(weapons)} weapons.')
    for i, weapon in enumerate(weapons):
        print(f'[{i+1}/{len(weapons)}] Saving {weapon["name"]}')
        save_weapon(weapon)
        time.sleep(0.1)
    print('Done.')

if __name__ == '__main__':
    main()
