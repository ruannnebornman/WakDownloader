import requests
import json
import sqlite3
import time
from bs4 import BeautifulSoup

DB_NAME = 'db/wakfu_monsters.db'
BASE_URL = 'https://www.wakfu.com'
MONSTER_LIST_URL = f'{BASE_URL}/en/mmorpg/encyclopedia/monsters'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS monsters')
    c.execute('''
        CREATE TABLE monsters (
            id INTEGER PRIMARY KEY,
            name TEXT,
            url TEXT,
            family TEXT,
            level TEXT,
            drops TEXT,           -- JSON
            harvesting TEXT       -- JSON
        )
    ''')
    conn.commit()
    conn.close()

def get_monster_links():
    links = []
    page = 1
    while True:
        url = f"{MONSTER_LIST_URL}?page={page}"
        print(f"Fetching {url}")
        resp = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(resp.text, 'html.parser')
        for a in soup.select('td > span.ak-linker > a[href*="/en/mmorpg/encyclopedia/monsters/"]'):
            href = a.get('href')
            if href and '/en/mmorpg/encyclopedia/monsters/' in href:
                links.append(BASE_URL + href)
        break
    return list(set(links))

def parse_monster_page(url):
    resp = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(resp.text, 'html.parser')
    # ID from URL
    id_part = url.rstrip('/').split('/')[-1].split('-')[0]
    try:
        monster_id = int(id_part)
    except Exception:
        monster_id = None
    # Name from h1 header
    h1 = soup.find('h1')
    name = h1.text.strip() if h1 else ''
    # Family
    family = ''
    fam_tag = soup.find('div', class_='ak-encyclo-detail-family')
    if fam_tag:
        family = fam_tag.text.replace('Family:', '').strip()
    # Level from the right of family (col-xs-4 text-right ak-encyclo-detail-level)
    level = None
    # Find the div with all required classes for level
    lvl_tag = soup.find('div', attrs={
        'class': lambda x: x and all(cls in x.split() for cls in ['col-xs-4', 'text-right', 'ak-encyclo-detail-level'])
    })
    if lvl_tag:
        lvl_text = lvl_tag.text.strip()
        # Extract the part after 'Level :' or 'Lvl'
        lvl_text = lvl_text.replace('Lvl', '').replace('Level', '').replace(':', '').strip()
        level = lvl_text if lvl_text else None
    # Drops
    drops = []
    for drop in soup.select('.ak-drop-list .ak-list-element'):
        drops.append(drop.text.strip())
    # Allows harvesting
    harvesting = []
    for harv in soup.select('.ak-harvest-list .ak-list-element'):
        harvesting.append(harv.text.strip())
    return {
        'id': monster_id,
        'name': name,
        'url': url,
        'family': family,
        'level': level,
        'drops': json.dumps(drops, ensure_ascii=False),
        'harvesting': json.dumps(harvesting, ensure_ascii=False)
    }

def save_monster(monster):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO monsters (id, name, url, family, level, drops, harvesting)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        monster['id'], monster['name'], monster['url'], monster['family'], monster['level'],
        monster['drops'], monster['harvesting']
    ))
    conn.commit()
    conn.close()

def main():
    init_db()
    links = get_monster_links()
    print(f'Found {len(links)} monsters.')
    for i, url in enumerate(links[:3]):
        print(f'[{i+1}/3] Downloading {url}')
        monster = parse_monster_page(url)
        save_monster(monster)
        time.sleep(0.1)
    print('Done.')

if __name__ == '__main__':
    main()
