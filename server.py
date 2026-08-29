#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bhajan Maalika (भजन मालिका) - Backend REST API & Web Server
Provides robust SQLite persistence, REST endpoints, and static web serving.
"""

import http.server
import json
import os
import re
import sqlite3
import sys
import time
import urllib.parse
from http import HTTPStatus

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

PORT = 8000
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
DB_PATH = os.path.join(DATA_DIR, 'bhajan_maalika.db')

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# --------------------------------------------------------------------------
# DATABASE MANAGEMENT
# --------------------------------------------------------------------------
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS collections (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            subtitle TEXT DEFAULT '',
            icon TEXT DEFAULT '🌸',
            image TEXT DEFAULT 'assets/images/ganesha.svg',
            color TEXT DEFAULT '#FF7A00',
            created_at INTEGER NOT NULL,
            updated_at INTEGER NOT NULL
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bhajans (
            id TEXT PRIMARY KEY,
            collection_id TEXT NOT NULL,
            title TEXT NOT NULL,
            content TEXT DEFAULT '',
            created_at INTEGER NOT NULL,
            updated_at INTEGER NOT NULL,
            FOREIGN KEY (collection_id) REFERENCES collections(id) ON DELETE CASCADE
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );
    """)
    conn.commit()

    # Check if empty, seed initial Marathi devotional data
    cursor.execute("SELECT COUNT(*) as count FROM collections")
    row = cursor.fetchone()
    if row and row['count'] == 0:
        seed_initial_data(conn)
    conn.close()

def seed_initial_data(conn):
    cursor = conn.cursor()
    now = int(time.time() * 1000)

    initial_data = [
        {
            "id": "col_ganpati",
            "name": "श्री गणेश भजने व आरत्या",
            "subtitle": "Ganpati Bhajans & Aartis",
            "icon": "🌺",
            "color": "#FF5722",
            "created_at": now - 86400000 * 5,
            "bhajans": [
                {
                    "id": "bhajan_sukhkarta",
                    "title": "सुखकर्ता दुःखहर्ता (श्री गणपती आरती)",
                    "content": """सुखकर्ता दुःखहर्ता वार्ता विघ्नाची ।
नुरवी पुरवी प्रेम कृपा जयाची ।
सर्वांगी सुंदर उटी शेंदुराची ।
कंठी झळके माळ मुक्ताफळांची ॥ १ ॥

जय देव जय देव जय मंगलमूर्ती ।
दर्शनमात्रे मनकामना पुरती ॥ ध्रु. ॥

रत्नखचित फरा तुज गौरीकुमरा ।
चंदनाची उटी कुंकुमकेशरा ।
हीरेजडित मुकुट शोभतो बरा ।
रुणझुणती नुपूरे चरणी घागरिया ॥ २ ॥
जय देव जय देव...

लंबोदर पीतांबर फणिवरबंधना ।
सरळ सोंड वक्रतुंड त्रिनयना ।
दास रामाचा वाट पाहे सदना ।
संकटी पावावे निर्वाणी रक्षावे सुरवरवंदना ॥ ३ ॥
जय देव जय देव जय मंगलमूर्ती ।
दर्शनमात्रे मनकामना पुरती ॥"""
                },
                {
                    "id": "bhajan_shendur",
                    "title": "शेंदुर लाल चढायो (आरती)",
                    "content": """शेंदुर लाल चढायो चांगो हर कुंवरो ।
कमल नयन निरखत भय मोचन तेरो ॥
अष्ट सिद्धि नव निधि के दाता दुखहर्ता ।
जय जय गणेश गिरिजा सुत विघ्नहर्ता ॥ १ ॥

जय जय श्री गणराज विद्या सुखदाता ।
धन्य तुम्हारो दर्शन सुर मुनि मन भाता ॥ ध्रु. ॥

गौरी के नंदन त्रिभुवन वंदन ।
मोदक भोग लगावत सेवक आनंदन ॥
ऋद्धि सिद्धि चवर ढुलत शोभित छवि भारी ।
संत जनन हितकारी भक्तन रखवारी ॥ २ ॥
जय जय श्री गणराज..."""
                },
                {
                    "id": "bhajan_prathamanaman",
                    "title": "प्रथम नमन गणेशा - भजन",
                    "content": """प्रथम नमन करू गणेशा ।
भवभय हरणा विघ्नेशा ॥ ध्रु. ॥

एकदंत दयावंत चार भुजाधारी ।
माथ्यावरती मुकुट शोभे मोदक आहारी ॥ १ ॥

रिद्धि-सिद्धि दासी तुझी मंगल वरदाता ।
कृपा करी बाप्पा आम्हा भक्तांच्या माथा ॥ २ ॥

शरण आलो तुजला आम्ही गणनायका ।
वारंवार वंदितो श्री सिद्धिविनायका ॥ ३ ॥"""
                }
            ]
        },
        {
            "id": "col_vitthal",
            "name": "विठ्ठल अभंग व भजने",
            "subtitle": "Vitthal Abhang & Bhajans",
            "icon": "🪕",
            "color": "#F59E0B",
            "created_at": now - 86400000 * 4,
            "bhajans": [
                {
                    "id": "bhajan_maher_pandhari",
                    "title": "माझे माहेर पंढरी (संत एकनाथ)",
                    "content": """माझे माहेर पंढरी । आहे भिवरेच्या तीरी ॥ १ ॥

बाप आणि आई । माझी विठ्ठल रखुमाई ॥ २ ॥

पुंडलीक बंधु । त्याची ख्याती काय सांगू ॥ ३ ॥

बहिणी चंद्रभागा । करीतसे पापभंगा ॥ ४ ॥

एका जनार्दनी । शरण शरण चक्रपाणी ॥ ५ ॥"""
                },
                {
                    "id": "bhajan_kanada_raja",
                    "title": "कानडा राजा पंढरीचा",
                    "content": """कानडा राजा पंढरीचा ।
वेदांनाही नाही कळला अंत पार याचा ॥ ध्रु. ॥

निराकार तो निर्गुण ईश्वर ।
भक्तांसाठी झाला सगुण साकार ॥
विटेवरी उभा कटेवरी हात ।
युगे अठ्ठावीस उभा पाहा पंढरीनाथ ॥ १ ॥

पुंडलिकाच्या भावासाठी ।
परब्रह्म आले वैकुंठी ॥
आनंदाचे डोही आनंद तरंग ।
भक्तीत रमले भक्तजन दंग ॥ २ ॥"""
                },
                {
                    "id": "bhajan_vithu_mauli",
                    "title": "विठू माऊली तू माऊली जगाची",
                    "content": """विठू माऊली तू माऊली जगाची ।
माऊलीच मूर्ती विठ्ठलाची ॥ ध्रु. ॥

काया ही पंढरी, आत्मा हा विठ्ठल ।
नांदतो हा देव अंतरात ॥
भाव-भक्तीचे हे बांधिले देऊळ ।
घेई गळा लावूनिया सर्व भक्तांस ॥ १ ॥

अमृताची गोडी तुझ्या नामामध्ये ।
दुःख दैन्य सारे दूर पळे ॥
माऊली कृपा कर आम्हा बालकांवर ।
चरणकमली ठाव दे निरंतर ॥ २ ॥"""
                }
            ]
        },
        {
            "id": "col_aarti",
            "name": "नित्य आरती संग्रह",
            "subtitle": "Daily Aarti Collection",
            "icon": "🪔",
            "color": "#EA580C",
            "created_at": now - 86400000 * 3,
            "bhajans": [
                {
                    "id": "bhajan_ghalin_lotangan",
                    "title": "घालीन लोटांगण वंदीन चरण",
                    "content": """घालीन लोटांगण वंदीन चरण ।
डोळ्यांनी पाहीन रूप तुझें ।
प्रेमें आलिंगिन आनंदे पूजिन ।
भावें ओवाळिन म्हणे नामा ॥ १ ॥

त्वमेव माता च पिता त्वमेव ।
त्वमेव बंधुश्च सखा त्वमेव ।
त्वमेव विद्या द्रविणं त्वमेव ।
त्वमेव सर्वं मम देवदेव ॥ २ ॥

कायेन वाचा मनसेंद्रियैर्वा ।
बुद्ध्यात्मना वा प्रकृतिस्वभावात् ।
करोमि यद्यत् सकलं परस्मै ।
नारायणायेति समर्पयामि ॥ ३ ॥

अच्युतं केशवं रामनारायणं ।
कृष्णदामोदरं वासुदेवं हरिम् ।
श्रीधरं माधवं गोपिकावल्लभं ।
जानकीनायकं रामचंद्रं भजे ॥ ४ ॥"""
                },
                {
                    "id": "bhajan_durge_durghat",
                    "title": "दुर्गे दुर्घट भारी (देवीची आरती)",
                    "content": """दुर्गे दुर्घट भारी तुजविण संसारी ।
अनाथनाथे अंबे करुणा विस्तारी ।
वारी वारी जन्ममरणाते वारी ।
हारी पडलो आता संकट निवारी ॥ १ ॥

जय देवी जय देवी जय महिषासुरमथनी ।
सुरवरईश्वरवरदे तारक संजीवनी ॥ ध्रु. ॥

त्रिभुवनभुवनी पाहता तुज ऐसी नाही ।
चारी श्रमले परंतु न बोलवे काही ।
साही विवाद करिता पडले प्रवाही ।
ते तू भक्तांलागी पावसी लवलाही ॥ २ ॥
जय देवी जय देवी...

प्रसन्न वदने प्रसन्न होसी निजदासां ।
क्लेशांपासोनि सोडी तोडी भवपाशा ।
अंबे तुजवांचून कोण पुरवील आशा ।
नरहरि तल्लीन झाला पदपंकजलेशा ॥ ३ ॥
जय देवी जय देवी जय महिषासुरमथनी..."""
                }
            ]
        },
        {
            "id": "col_datta_sai",
            "name": "श्री दत्त व साई भजने",
            "subtitle": "Datta & Sai Baba Bhajans",
            "icon": "🚩",
            "color": "#D97706",
            "created_at": now - 86400000 * 2,
            "bhajans": [
                {
                    "id": "bhajan_digambara",
                    "title": "दिगंबरा दिगंबरा श्रीपाद वल्लभ दिगंबरा",
                    "content": """दिगंबरा दिगंबरा श्रीपाद वल्लभ दिगंबरा ॥ ध्रु. ॥

गाणगापूरचे गुरु महाराज ।
तारक तू भवसिंधूचा आज ॥ १ ॥

औदुंबर छायेखाली ध्यान ।
दत्त नामाचे घेई रे गुणगान ॥ २ ॥

त्रिमुखी त्रिनेत्र आनंदमूर्ती ।
दर्शन होता मन पावे शांती ॥ ३ ॥

दिगंबरा दिगंबरा श्रीपाद वल्लभ दिगंबरा ॥"""
                },
                {
                    "id": "bhajan_shirdi_maze",
                    "title": "शिर्डी माझे पंढरपूर",
                    "content": """शिर्डी माझे पंढरपूर । साईबाबा रमावर ॥ १ ॥

शुद्ध भक्ती चंद्रभागा । भाव प्रेमाचा हा ओघा ॥ २ ॥

दया क्षमा शांती तुळसी । वाहा बाबांच्या चरणांसी ॥ ३ ॥

दास म्हणे साईनाथ । तूचि माझा दीनानाथ ॥ ४ ॥"""
                }
            ]
        }
    ]

    for col in initial_data:
        cursor.execute(
            "INSERT INTO collections (id, name, subtitle, icon, color, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (col["id"], col["name"], col["subtitle"], col["icon"], col["color"], col["created_at"], col["created_at"])
        )
        for b in col["bhajans"]:
            cursor.execute(
                "INSERT INTO bhajans (id, collection_id, title, content, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                (b["id"], col["id"], b["title"], b["content"], col["created_at"], col["created_at"])
            )

    cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('theme', 'light')")
    conn.commit()

# --------------------------------------------------------------------------
# API HELPERS & HANDLERS
# --------------------------------------------------------------------------
def fetch_all_collections():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM collections ORDER BY created_at DESC")
    collections = []
    for c_row in cursor.fetchall():
        col_id = c_row['id']
        cursor.execute("SELECT * FROM bhajans WHERE collection_id = ? ORDER BY created_at DESC", (col_id,))
        bhajans = [
            {
                "id": b['id'],
                "title": b['title'],
                "content": b['content'],
                "createdAt": b['created_at'],
                "updatedAt": b['updated_at']
            }
            for b in cursor.fetchall()
        ]
        collections.append({
            "id": c_row['id'],
            "name": c_row['name'],
            "subtitle": c_row['subtitle'],
            "icon": c_row['icon'],
            "image": c_row['image'] if 'image' in c_row.keys() and c_row['image'] else 'assets/images/ganesha.svg',
            "color": c_row['color'],
            "createdAt": c_row['created_at'],
            "updatedAt": c_row['updated_at'],
            "bhajans": bhajans
        })
    conn.close()
    return collections

class BhajanMaalikaHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        directory = os.path.dirname(os.path.abspath(__file__))
        super().__init__(*args, directory=directory, **kwargs)

    def translate_path(self, path):
        parsed = urllib.parse.urlparse(path)
        return super().translate_path(parsed.path)

    def _send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Origin, Accept')
        self.end_headers()
        self.wfile.write(body)

    def _read_body(self):
        length = int(self.headers.get('Content-Length', 0))
        if length > 0:
            raw = self.rfile.read(length).decode('utf-8')
            return json.loads(raw)
        return {}

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Origin, Accept')
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip('/')

        # 1. Health Check
        if path == '/api/health':
            self._send_json({"status": "ok", "app": "Bhajan Maalika", "version": "1.0", "backend": "Python SQLite"})
            return

        # 2. Get All Collections & Bhajans
        if path == '/api/collections':
            data = fetch_all_collections()
            self._send_json({"success": True, "collections": data})
            return

        # 3. Get Theme Setting
        if path == '/api/theme':
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM settings WHERE key = 'theme'")
            row = cursor.fetchone()
            theme = row['value'] if row else 'light'
            conn.close()
            self._send_json({"theme": theme})
            return

        # Static File Serving
        super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip('/')

        # 1. Create Collection: POST /api/collections
        if path == '/api/collections':
            payload = self._read_body()
            name = payload.get('name', '').strip()
            if not name:
                self._send_json({"error": "Collection name is required"}, status=400)
                return

            now = int(time.time() * 1000)
            col_id = payload.get('id') or ('col_' + str(now))
            subtitle = payload.get('subtitle', '').strip()
            icon = payload.get('icon', '🌸')
            image = payload.get('image', 'assets/images/ganesha.svg')
            color = payload.get('color', '#FF7A00')

            conn = get_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO collections (id, name, subtitle, icon, image, color, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (col_id, name, subtitle, icon, image, color, now, now)
            )
            conn.commit()
            conn.close()

            new_col = {
                "id": col_id,
                "name": name,
                "subtitle": subtitle,
                "icon": icon,
                "image": image,
                "color": color,
                "createdAt": now,
                "updatedAt": now,
                "bhajans": []
            }
            self._send_json({"success": True, "collection": new_col}, status=201)
            return

        # 2. Create Bhajan: POST /api/collections/<col_id>/bhajans
        m = re.match(r'^/api/collections/([^/]+)/bhajans$', path)
        if m:
            col_id = urllib.parse.unquote(m.group(1))
            payload = self._read_body()
            title = payload.get('title', '').strip() or 'नवीन भजन'
            content = payload.get('content', '')

            now = int(time.time() * 1000)
            bhajan_id = payload.get('id') or ('bhajan_' + str(now))

            conn = get_db()
            cursor = conn.cursor()
            # Ensure parent collection exists
            cursor.execute("SELECT id FROM collections WHERE id = ?", (col_id,))
            if not cursor.fetchone():
                cursor.execute(
                    "INSERT OR REPLACE INTO collections (id, name, subtitle, icon, color, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (col_id, "भजन संकलन", "", "🌸", "#FF7A00", now, now)
                )

            cursor.execute(
                "INSERT OR REPLACE INTO bhajans (id, collection_id, title, content, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                (bhajan_id, col_id, title, content, now, now)
            )
            cursor.execute("UPDATE collections SET updated_at = ? WHERE id = ?", (now, col_id))
            conn.commit()
            conn.close()

            new_bhajan = {
                "id": bhajan_id,
                "title": title,
                "content": content,
                "createdAt": now,
                "updatedAt": now
            }
            self._send_json({"success": True, "bhajan": new_bhajan}, status=201)
            return

        # 3. Save Theme: POST /api/theme
        if path == '/api/theme':
            payload = self._read_body()
            theme = payload.get('theme', 'light')
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('theme', ?)", (theme,))
            conn.commit()
            conn.close()
            self._send_json({"success": True, "theme": theme})
            return

        # 4. Bulk Sync: POST /api/sync
        if path == '/api/sync':
            payload = self._read_body()
            cols = payload.get('collections', [])
            if cols:
                conn = get_db()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM bhajans")
                cursor.execute("DELETE FROM collections")
                for c in cols:
                    c_time = c.get('createdAt', int(time.time() * 1000))
                    cursor.execute(
                        "INSERT INTO collections (id, name, subtitle, icon, color, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (c['id'], c['name'], c.get('subtitle', ''), c.get('icon', '🌸'), c.get('color', '#FF7A00'), c_time, c.get('updatedAt', c_time))
                    )
                    for b in c.get('bhajans', []):
                        b_time = b.get('createdAt', c_time)
                        cursor.execute(
                            "INSERT INTO bhajans (id, collection_id, title, content, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                            (b['id'], c['id'], b['title'], b.get('content', ''), b_time, b.get('updatedAt', b_time))
                        )
                conn.commit()
                conn.close()
            self._send_json({"success": True, "collections": fetch_all_collections()})
            return

        self._send_json({"error": "Endpoint not found"}, status=404)

    def do_PUT(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip('/')

        # 1. Update Collection: PUT /api/collections/<col_id>
        m = re.match(r'^/api/collections/([^/]+)$', path)
        if m:
            col_id = urllib.parse.unquote(m.group(1))
            payload = self._read_body()
            name = payload.get('name', '').strip()
            subtitle = payload.get('subtitle', '').strip()
            icon = payload.get('icon')
            image = payload.get('image')
            now = int(time.time() * 1000)

            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM collections WHERE id = ?", (col_id,))
            if cursor.fetchone():
                cursor.execute(
                    "UPDATE collections SET name = COALESCE(NULLIF(?, ''), name), subtitle = ?, icon = COALESCE(?, icon), image = COALESCE(?, image), updated_at = ? WHERE id = ?",
                    (name, subtitle, icon, image, now, col_id)
                )
            else:
                cursor.execute(
                    "INSERT INTO collections (id, name, subtitle, icon, image, color, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (col_id, name or "भजन संकलन", subtitle, icon or "🌸", image or "assets/images/ganesha.svg", "#FF7A00", now, now)
                )
            conn.commit()
            conn.close()
            self._send_json({"success": True, "updated": col_id})
            return

        # 2. Update Bhajan (Auto-Save): PUT /api/collections/<col_id>/bhajans/<bhajan_id>
        m = re.match(r'^/api/collections/([^/]+)/bhajans/([^/]+)$', path)
        if m:
            col_id = urllib.parse.unquote(m.group(1))
            bhajan_id = urllib.parse.unquote(m.group(2))
            payload = self._read_body()
            title = payload.get('title', '').strip()
            content = payload.get('content', '')
            now = int(time.time() * 1000)

            conn = get_db()
            cursor = conn.cursor()

            # Ensure parent collection exists
            cursor.execute("SELECT id FROM collections WHERE id = ?", (col_id,))
            if not cursor.fetchone():
                cursor.execute(
                    "INSERT OR REPLACE INTO collections (id, name, subtitle, icon, color, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (col_id, "भजन संकलन", "", "🌸", "#FF7A00", now, now)
                )

            # Check if bhajan exists; if so, update, otherwise insert
            cursor.execute("SELECT id FROM bhajans WHERE id = ? AND collection_id = ?", (bhajan_id, col_id))
            if cursor.fetchone():
                cursor.execute(
                    "UPDATE bhajans SET title = COALESCE(NULLIF(?, ''), title), content = ?, updated_at = ? WHERE id = ? AND collection_id = ?",
                    (title, content, now, bhajan_id, col_id)
                )
            else:
                cursor.execute(
                    "INSERT OR REPLACE INTO bhajans (id, collection_id, title, content, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                    (bhajan_id, col_id, title or 'नवीन भजन', content, now, now)
                )

            cursor.execute("UPDATE collections SET updated_at = ? WHERE id = ?", (now, col_id))
            conn.commit()
            conn.close()
            self._send_json({"success": True, "saved": bhajan_id, "updatedAt": now, "contentLength": len(content)})
            return

        self._send_json({"error": "Endpoint not found"}, status=404)

    def do_DELETE(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip('/')

        # 1. Delete Collection: DELETE /api/collections/<col_id>
        m = re.match(r'^/api/collections/([^/]+)$', path)
        if m:
            col_id = urllib.parse.unquote(m.group(1))
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM collections WHERE id = ?", (col_id,))
            conn.commit()
            conn.close()
            self._send_json({"success": True, "deleted": col_id})
            return

        # 2. Delete Bhajan: DELETE /api/collections/<col_id>/bhajans/<bhajan_id>
        m = re.match(r'^/api/collections/([^/]+)/bhajans/([^/]+)$', path)
        if m:
            col_id = urllib.parse.unquote(m.group(1))
            bhajan_id = urllib.parse.unquote(m.group(2))
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM bhajans WHERE id = ? AND collection_id = ?", (bhajan_id, col_id))
            conn.commit()
            conn.close()
            self._send_json({"success": True, "deleted": bhajan_id})
            return

        self._send_json({"error": "Endpoint not found"}, status=404)

def run_server():
    init_db()
    server_address = ('', PORT)
    httpd = http.server.ThreadingHTTPServer(server_address, BhajanMaalikaHandler)
    print(f"[Bhajan Maalika Backend] Server running at http://localhost:{PORT}")
    print(f"[SQLite Database] Initialized at {DB_PATH}")
    sys.stdout.flush()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
        httpd.server_close()

if __name__ == '__main__':
    run_server()
