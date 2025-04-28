import os
import sqlite3
import uuid
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.config['SECRET_KEY'] = 'chave-secreta-super-simples'
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
DB_NAME = 'database.db'

EMAIL_ADDRESS = "notificacao.amfin.naoresponder@gmail.com"
EMAIL_PASSWORD = "zdct akit mgvp sjbq"

obra_emails = {
    "CPQ-LDN": ["engenharia@amfoodsbr.com", "carolina@amfoodsbr.com", "fernando@amfoodsbr.com", "gerencialdb1@gmail.com"],
    "CPQ-IGU": ["engenharia@amfoodsbr.com", "carolina@amfoodsbr.com", "fernando@amfoodsbr.com", "suportefinanceiropoa5@gmail.com"]
}

PROJECT_CODES = {
    "1234": "CPQ-LDN",
    "5678": "CPQ-IGU"
}

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT,
            description TEXT,
            total_amount REAL,
            payment_terms TEXT,
            delivery_date TEXT,
            pdf_path TEXT,
            payment_date TEXT,
            approved INTEGER DEFAULT 0,
            approver_name TEXT,
            observations TEXT,
            revised_pdf_path TEXT,
            payment_responsible TEXT,
            proof_path TEXT,
            last_edited TEXT,
            project_name TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def send_email(project_name, payment_id, company, description, total_amount, payment_terms, is_new=True):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['Subject'] = f"Novo Pagamento - {project_name} - {company}"
    body = f'''
    Projeto: {project_name}
    Empresa: {company}
    Descrição: {description}
    Valor Total: R$ {total_amount:,.2f}
    Condições de Pagamento: {payment_terms}
    {'Novo cadastro' if is_new else 'Atualização de cadastro'} no sistema AMFin.
    '''
    msg.attach(MIMEText(body, 'plain'))
    recipients = obra_emails.get(project_name, [])
    msg['To'] = ", ".join(recipients)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    server.send_message(msg)
    server.quit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/acesso', methods=['GET', 'POST'])
def acesso():
    error = None
    if request.method == 'POST':
        senha = request.form.get('senha')
        if senha == '1234':
            session['acesso_liberado'] = True
            return redirect(url_for('dashboard'))
        else:
            error = True
    return render_template('acesso.html', error=error)

@app.route('/dashboard')
def dashboard():
    if not session.get('acesso_liberado'):
        return redirect(url_for('acesso'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/select_project')
def select_project():
    return render_template('select_project.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)