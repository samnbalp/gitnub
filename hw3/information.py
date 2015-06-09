#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter11/bank.py
# A small library of database routines to power a payments application.

import os, pprint, sqlite3
from collections import namedtuple

def open_database(path='myinformation.db'):
    new = not os.path.exists(path)
    db = sqlite3.connect(path)
    if new:
        c = db.cursor()
        c.execute('CREATE TABLE information (id INTEGER PRIMARY KEY,'
                  ' user TEXT, color TEXT, aspiration TEXT, interest TEXT)')
        add_information(db, 'brandon', 'Unfilled', 'Unfilled', 'Unfilled')
        add_information(db, 'sam', 'Unfilled', 'Unfilled', 'Unfilled')
        db.commit()
    return db

def add_information(db, in_user, in_color, in_aspiration, in_interest):
    db.cursor().execute('INSERT INTO information (user, color, aspiration, interest)'
                        ' VALUES (?, ?, ?, ?)', (in_user, in_color, in_aspiration, in_interest))	
	
def update_inform(db, in_user, in_color, in_aspiration, in_interest):
    num=0
    if in_color!='':
        num=num+1
    if in_aspiration!='':
        num=num+3
    if in_interest!='':
        num=num+5
    
    if num==1:
        db.cursor().execute('UPDATE information SET color=? WHERE user= ?',(in_color,in_user))
    elif num==3:
        db.cursor().execute('UPDATE information SET aspiration=? WHERE user= ?',(in_aspiration,in_user))
    elif num==4:
        db.cursor().execute('UPDATE information SET color=? ,aspiration=? WHERE user= ?',(in_color, in_aspiration,in_user))
    elif num==5:
        db.cursor().execute('UPDATE information SET interest=? WHERE user= ?',(in_interest,in_user))
    elif num==6:
        db.cursor().execute('UPDATE information SET color=? ,interest=? WHERE user= ?',(in_color,in_interest,in_user))
    elif num==8:
        db.cursor().execute('UPDATE information SET aspiration=? ,interest=? WHERE user= ?',(in_aspiration, in_interest,in_user))
    elif num==9:
        db.cursor().execute('UPDATE information SET color=? ,aspiration=? ,interest=? WHERE user= ?',(in_color, in_aspiration, in_interest,in_user))
    else:
        num=0

def get_information(db, account):
    c = db.cursor()
    c.execute('SELECT * FROM information WHERE user = ?',(account,))
    Row = namedtuple('Row', [tup[0] for tup in c.description])
    return [Row(*row) for row in c.fetchall()]

if __name__ == '__main__':
    db = open_database()
    pprint.pprint(get_payments_of(db, 'brandon'))