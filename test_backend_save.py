import urllib.request
import json
import sqlite3
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# 1. Test Auto-Save via PUT request
col_id = "col_aarti"
bhajan_id = "test_bhajan_auto_save_123"
url = f"http://localhost:8000/api/collections/{col_id}/bhajans/{bhajan_id}"

payload = {
    "title": "आनंदाचे डोही आनंद तरंग (कसोटी)",
    "content": "आनंदाचे डोही आनंद तरंग ।\nआनंदचि अंग आनंदाचे ॥ १ ॥\n\nकाय सांगो सुखाची माये ।\nविठ्ठल पाय वंदिले ॥ २ ॥"
}

req = urllib.request.Request(
    url,
    data=json.dumps(payload, ensure_ascii=False).encode('utf-8'),
    headers={'Content-Type': 'application/json; charset=utf-8'},
    method='PUT'
)

with urllib.request.urlopen(req) as resp:
    result = json.loads(resp.read().decode('utf-8'))
    print("PUT API Response:", result)

# 2. Check SQLite directly
conn = sqlite3.connect('data/bhajan_maalika.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()
c.execute("SELECT id, title, content, updated_at FROM bhajans WHERE id = ?", (bhajan_id,))
row = c.fetchone()
if row:
    print("SUCCESS! Bhajan saved in SQLite database:")
    print(" - ID:", row['id'])
    print(" - Title:", row['title'])
    print(" - Content:", repr(row['content']))
else:
    print("ERROR: Not found in database!")
