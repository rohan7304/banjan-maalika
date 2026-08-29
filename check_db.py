import sqlite3
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect('data/bhajan_maalika.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()
c.execute('SELECT id, collection_id, title, content, updated_at FROM bhajans')
rows = c.fetchall()
print(f'Total bhajans in SQLite: {len(rows)}')
for r in rows:
    preview = r['content'][:40].replace('\n', ' ') if r['content'] else '(empty)'
    print(f"[{r['collection_id']}] ID: {r['id']} | Title: {r['title']} | Content: {preview}")
