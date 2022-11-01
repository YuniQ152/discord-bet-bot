import sqlite3
from random import randint, shuffle
from utils import *

conn = sqlite3.connect("db.sqlite3")
cur = conn.cursor()

def update_user_data(target):
    cur.execute("INSERT OR IGNORE INTO userdata(id, username, diamond, gold, exp, registerAt) VALUES (?,?,?,?,?,?)", (target.id, target.name+"#"+target.discriminator, 10, 250, 0, get_unix_time()))
    cur.execute("UPDATE userdata SET username = ? WHERE id = ?", (target.name+"#"+target.discriminator, target.id))
    conn.commit()
    return()

def load_user_money(target):
    update_user_data(target)
    cur.execute("SELECT diamond, gold FROM userdata WHERE id = ?", (target.id,))
    data = cur.fetchone()
    diamond = data[0]
    gold = data[1]
    return(diamond, gold)

def change_user_diamond(target, val):
    update_user_data(target)
    diamond, gold = load_user_money(target)
    cur.execute("UPDATE userdata SET diamond = ? WHERE id = ?", (diamond+val, target.id))
    conn.commit()
    return(diamond+val)
def change_user_gold(target, val):
    update_user_data(target)
    diamond, gold = load_user_money(target)
    cur.execute("UPDATE userdata SET gold = ? WHERE id = ?", (gold+val, target.id))
    conn.commit()
    return(gold+val)