import sqlite3

def main():
    with sqlite3.connect("date/list_final.db") as db:
        cur = db.cursor()

        query = """CREATE TABLE list (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        text TEXT NOT NULL,
        _date DATE NOT NULL,
        time DATE NOT NULL
        );"""

        cur.execute(query)

        db.commit()


def select_list():
    try:
        with sqlite3.connect("./list_final.db") as db:
            cur = db.cursor()

            query = """SELECT * FROM list"""
            cur.execute(query)

            select = cur.fetchall()

            db.commit()
    except Exception:
        return [(1,"Ошибка", Exception.__text_signature__, 0)]
        print(Exception.__text_signature__)
        
    return select

def inser_list(title, text, date, time):
    with sqlite3.connect("./list_final.db") as db:
        cur = db.cursor()

        query = f"""
        INSERT INTO list (title, text, _date, time)
        VALUES ("{title}", "{text}", "{date}", "{time}")
        """

        cur.execute(query)

        db.commit()

def list_json(db):
    req_json = []
    
    for row in db:
        facts = {
            "id": row[0],
            "title": row[1],
            "text": row[2],
            "date": row[3],
            "time": row[4]
        } 

        req_json.append(facts)

    return req_json

def delete_list(id):
    with sqlite3.connect("./list_final.db") as db:
        cur = db.cursor()

        query = """
        DELETE FROM list
        WHERE id = ? 
        """

        cur.execute(query, (id,))

        db.commit()
        
    
if __name__ == "__main__":
    # main()
    inser_list("Второй лист", "Второй текст", "24-10-2014", " ")
    # for i in list_json(db=select_list()):
    #     print(i)
