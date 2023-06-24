import os
import json
import sqlite3
import config
from datetime import datetime


# Функция для парсинга строки лога и извлечения IP-адреса и времени
def create_database_db():
    if os.path.exists(config.apache_db):
        os.remove(config.apache_db)
    conn = sqlite3.connect(config.apache_db)
    c = conn.cursor()
    c.execute('''CREATE TABLE logs_apache
                 (ip text, date text, request text, status_code integer, size integer)''')
    with open(config.apache_logs) as f:
        for line in f:
            parts = line.split()
            ip = parts[0]
            date_str = parts[3][1:] + " " + parts[4][:-1]
            date = datetime.strptime(date_str, '%d/%b/%Y:%H:%M:%S %z')
            date_formatted = date.strftime('%d/%b/%Y:%H:%M:%S %z')
            request = parts[5] + " " + parts[6] + " " + parts[7]
            status_code = int(parts[8])
            size = int(parts[9])
            c.execute(f"INSERT INTO logs_apache VALUES ('{ip}', '{date_formatted}', '{request}', {status_code}, {size})")
    conn.commit()
    conn.close()

def apache_ip(ip):
    conn = sqlite3.connect(config.apache_db)
    c = conn.cursor()
    c.execute(f"SELECT * FROM logs_apache WHERE ip='{ip}'")
    rows = c.fetchall()
    conn.close()
    return rows

def apache_date(date):
    conn = sqlite3.connect(config.apache_db)
    c = conn.cursor()
    date_formatted = date.strftime('%d/%b/%Y:%H:%M:%S %z')
    c.execute(f"SELECT * FROM logs_apache WHERE date='{date_formatted}'")
    rows = c.fetchall()
    conn.close()
    return rows

def apache_date_range(start_date, end_date):
    conn = sqlite3.connect(config.apache_db)
    c = conn.cursor()
    start_date_formatted = start_date.strftime('%d/%b/%Y:%H:%M:%S %z')
    end_date_formatted = end_date.strftime('%d/%b/%Y:%H:%M:%S %z')
    c.execute(f"SELECT * FROM logs_apache WHERE date BETWEEN '{start_date_formatted}' AND '{end_date_formatted}'")
    rows = c.fetchall()
    conn.close()
    return rows

def create_database_json():
  if os.path.exists(config.json_db):
      os.remove(config.json_db)
  conn = sqlite3.connect(config.json_db)
  c = conn.cursor()
  c.execute('''CREATE TABLE logs_json
               (ip text, date text, request text, status_code integer, size integer)''')
  with open(config.json_logs) as f:
      data = json.load(f)
      for log in data:
          ip = log['IP']
          date_str = log['Date'] + ' ' + log['Time']
          date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
          date_formatted = date.strftime('%d/%b/%Y:%H:%M:%S %z')
          request = log['First_Line']
          status_code = log['Status']
          size = log['Size']
          c.execute(f"INSERT INTO logs_json VALUES ('{ip}', '{date_formatted}', '{request}', {status_code}, {size})")
  conn.commit()
  conn.close()

def json_ip(ip_address):
    with open(config.json_logs) as cicl:
        logs = json.load(cicl)
    return [log for log in logs if log['IP'] == ip_address]

def json_date(date):
    with open(config.json_logs) as cicl:
        logs = json.load(cicl)
    return [log for log in logs if log['Date'] == date]

def json_date_range(start_date, end_date):
    with open(config.json_logs) as cicl:
        logs = json.load(cicl)
    return [log for log in logs if start_date <= log['Date'] <= end_date]


create_database_db()
create_database_json()