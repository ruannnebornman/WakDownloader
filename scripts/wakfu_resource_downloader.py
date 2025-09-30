import requests
import json
import sqlite3
from bs4 import BeautifulSoup
import time

DB_NAME = 'db/wakfu_resources.db'
BASE_URL = 'https://www.wakfu.com'
RESOURCE_LIST_URL = f'{BASE_URL}/en/mmorpg/encyclopedia/resources'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS resources')
    c.execute('''
        CREATE TABLE resources (
            id INTEGER PRIMARY KEY,
            name TEXT,
            url TEXT,
            type TEXT,
            level INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def get_all_resources():
    resources = []
    url = RESOURCE_LIST_URL
    print(f"Fetching {url}")
    resp = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(resp.text, 'html.parser')
    table = soup.find('table')
    if not table:
        print("No table found on page.")
        return resources
    tbody = table.find('tbody')
    if not tbody:
        print("No tbody found in table.")
        return resources
    rows = tbody.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        if len(cols) < 4:
            continue
        # Name and link (column 1)
        name_tag = cols[1].find('a')
        name = name_tag.text.strip() if name_tag else ''
        link = BASE_URL + name_tag['href'] if name_tag and name_tag.has_attr('href') else ''
        # ID from URL
        resource_id = None
        if name_tag and name_tag.has_attr('href'):
            parts = name_tag['href'].split('/')
            if len(parts) > 0:
                id_part = parts[-1].split('-')[0]
                try:
                    resource_id = int(id_part)
                except Exception:
                    resource_id = None
        # Type from image alt text in the item-type column (column 2)
        type_img_tag = cols[2].find('img') if len(cols) > 2 else None
        type_ = type_img_tag['alt'].strip() if type_img_tag and type_img_tag.has_attr('alt') else ''
        # Level (column 3)
        level_text = cols[3].text.strip()
        try:
            level = int(level_text.replace('Lvl', '').strip())
        except Exception:
            level = None
        if resource_id is not None:
            resources.append({
                'id': resource_id,
                'name': name,
                'url': link,
                'type': type_,
                'level': level
            })
    return resources

def save_resource(resource):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO resources (id, name, url, type, level)
        VALUES (?, ?, ?, ?, ?)
    ''', (resource['id'], resource['name'], resource['url'], resource['type'], resource['level']))
    conn.commit()
    conn.close()

def main():
    init_db()
    resources = get_all_resources()
    print(f'Found {len(resources)} resources.')
    for i, resource in enumerate(resources):
        print(f'[{i+1}/{len(resources)}] Saving {resource["name"]}')
        save_resource(resource)
        time.sleep(0.05)
    print('Done.')

if __name__ == '__main__':
    main()
