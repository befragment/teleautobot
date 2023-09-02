import sqlite3

db = sqlite3.connect("message_restriction.db")
cur = db.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS ids(id integer)")


def get_restricted() -> None:
    file = open("textfiles/restricted_list", "r")
    for restricted_id in file:
        cur.execute(f"INSERT INTO id VALUES {restricted_id}")


def add_restricted(user_id: int) -> None:
    cur.execute(f"INSERT INTO ids VALUES ({user_id})")
    db.commit()


def all_restricted() -> list:
    cur.execute("SELECT id FROM ids")
    return cur.fetchall()


def restricted(user_id: int) -> bool:
    cur.execute("SELECT id FROM ids")
    return (user_id,) in cur.fetchall()
