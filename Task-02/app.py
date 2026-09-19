from flask import Flask, request, redirect, session, render_template_string
import sqlite3, hashlib

app = Flask(__name__)
app.secret_key = "prodigy2024"

def db():
    conn = sqlite3.connect('emp.db')
    conn.execute("CREATE TABLE IF NOT EXISTS users (u TEXT, p TEXT)")
    conn.execute("CREATE TABLE IF NOT EXISTS emps (id INTEGER PRIMARY KEY, name TEXT, email TEXT, dept TEXT, sal TEXT)")
    try:
        h = hashlib.sha256("admin123".encode()).hexdigest()
        conn.execute("INSERT INTO users VALUES (?,?)", ("admin", h))
        conn.commit()
    except: pass
    return conn

HTML = """
<h2>Task-02: Employee Management - Prodigy</h2>
{% if not session.get('user') %}
<form method=post action=/login>
<input name=user placeholder=admin required> <input name=pass type=password placeholder=admin123 required> <button>Login</button>
</form>
{% else %}
<a href=/logout>Logout</a><br><br>
<form method=post action=/add>
<input name=name placeholder=Name required> <input name=email placeholder=Email required>
<input name=dept placeholder=Dept required> <input name=sal placeholder=Salary required> <button>Add</button>
</form><br>
<table border=1><tr><th>ID</th><th>Name</th><th>Email</th><th>Dept</th><th>Sal</th><th>Del</th></tr>
{% for e in emps %}<tr><td>{{e[0]}}</td><td>{{e[1]}}</td><td>{{e[2]}}</td><td>{{e[3]}}</td><td>{{e[4]}}</td><td><a href=/del/{{e[0]}}>X</a></td></tr>{% endfor %}</table>
{% endif %}
"""

@app.route('/')
def home():
    con=db(); emps=con.execute("SELECT * FROM emps").fetchall(); con.close()
    return render_template_string(HTML, emps=emps)

@app.route('/login', methods=['POST'])
def login():
    h=hashlib.sha256(request.form['pass'].encode()).hexdigest()
    con=db(); u=con.execute("SELECT * FROM users WHERE u=? AND p=?",(request.form['user'],h)).fetchone(); con.close()
    if u: session['user']=u[0]; return redirect('/')
    return "Invalid Login! Use admin/admin123"

@app.route('/add', methods=['POST'])
def add():
    if "@" not in request.form['email']: return "Invalid Email"
    con=db(); con.execute("INSERT INTO emps (name,email,dept,sal) VALUES (?,?,?,?)",(request.form['name'],request.form['email'],request.form['dept'],request.form['sal'])); con.commit(); con.close()
    return redirect('/')

@app.route('/del/<int:id>')
def delete(id):
    con=db(); con.execute("DELETE FROM emps WHERE id=?",(id,)); con.commit(); con.close(); return redirect('/')

@app.route('/logout')
def logout(): session.clear(); return redirect('/')

if __name__=='__main__': app.run(debug=True)
