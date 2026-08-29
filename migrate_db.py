import sqlite3

conn = sqlite3.connect('data/bhajan_maalika.db')
c = conn.cursor()

c.execute('PRAGMA table_info(collections)')
cols = [row[1] for row in c.fetchall()]
if 'image' not in cols:
    c.execute("ALTER TABLE collections ADD COLUMN image TEXT DEFAULT ''")
    print('Added image column to collections')

c.execute("UPDATE collections SET image = 'assets/images/ganesha.svg' WHERE id = 'col_ganpati'")
c.execute("UPDATE collections SET image = 'assets/images/vitthal.svg' WHERE id = 'col_vitthal'")
c.execute("UPDATE collections SET image = 'assets/images/diya_aarti.svg' WHERE id = 'col_aarti'")
c.execute("UPDATE collections SET image = 'assets/images/sai.svg' WHERE id = 'col_datta_sai'")
c.execute("UPDATE collections SET image = 'assets/images/ganesha.svg' WHERE image IS NULL OR image = ''")

conn.commit()
print('Migration completed successfully!')
