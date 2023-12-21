import os
import psycopg2
from flask import Flask, render_template

app=Flask(__name__)
@app.route("/")
def hello():
    return "<p>hello</p>"
@app.route("/psqlconnection")
def connect():
    conn=psycopg2.connect(
        database="roshini",  
        user="postgres", 
        password="1234",  
        host="localhost", port="5432") 
    cur=conn.cursor()

    cur.execute('''select * from task''')
    values=cur.fetchall()
    conn.commit()
    return render_template('index.html',data=values)
    cur.close()
    conn.close()
if __name__ == "__main__":
    app.run(debug=True)