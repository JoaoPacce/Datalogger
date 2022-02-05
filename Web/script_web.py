from flask import Flask, render_template, request
app = Flask(__name__)
import sqlite3


# Retrieve data from database
def getData():
    conn = sqlite3.connect('../datalogger.db')
    cursor = conn.cursor()
    for row in cursor.execute("SELECT * FROM teste ORDER BY id DESC LIMIT 1"):
        dia = row[1]
        mes = row[2]
        ano = row[3]
        hora = row[4]
        minuto = row[5]
        segundo = row[6]
        dado = row[7]
    conn.close()
    return dia, mes, ano, hora, minuto, segundo, dado

# main route 
@app.route("/")
def index():
    dia, mes, ano, hora, minuto, segundo, dado = getData()
    templateData = {
        'dia': dia,
        'mes': mes,
        'ano': ano,
        'hora': hora,
        'minuto': minuto,
        'segundo': segundo,
        'dado' : dado
    }
    return render_template('index.html', **templateData)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=5000, debug=False)
