import sqlite3

def main():
    with sqlite3.connect("date/list.db") as db:
        cur = db.cursor()

        query = """CREATE TABLE list (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        text TEXT NOT NULL
        );"""

        cur.execute(query)

        db.commit()


def select_list():
    with sqlite3.connect("date/list.db") as db:
        cur = db.cursor()

        query = """SELECT * FROM list"""
        cur.execute(query)

        select = cur.fetchall()

        db.commit()

    return select

def inser_list(title, text):
    with sqlite3.connect("date/list.db") as db:
        cur = db.cursor()

        query = f"""
        INSERT INTO list (title, text)
        VALUES ("{title}", "{text}")
        """

        cur.execute(query)

        db.commit()

def list_json(db):
    req_json = []
    
    for row in db:
        facts = {
            "id": row[0],
            "title": row[1],
            "text": row[2]
        } 

        req_json.append(facts)

    return req_json

def delete_list(id):
    with sqlite3.connect("date/list.db") as db:
        cur = db.cursor()

        query = """
        DELETE FROM list
        WHERE id = ? 
        """

        cur.execute(query, (id,))

        db.commit()
        
    
if __name__ == "__main__":
    # inser_list("Второй лист", "Второй текст")
    for i in list_json(db=select_list()):
        print(i)
