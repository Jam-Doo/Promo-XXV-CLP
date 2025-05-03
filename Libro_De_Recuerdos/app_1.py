from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)

# Carpeta para subir archivos
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Lista de recuerdos
recuerdos = []

RECUERDOS_POR_PAGINA = 3

@app.route('/')
@app.route('/pagina/<int:pagina>')
def index(pagina=1):
    inicio = (pagina - 1) * RECUERDOS_POR_PAGINA
    fin = inicio + RECUERDOS_POR_PAGINA
    total_paginas = (len(recuerdos) + RECUERDOS_POR_PAGINA - 1) // RECUERDOS_POR_PAGINA

    return render_template('index.html',
                           recuerdos=recuerdos[inicio:fin],
                           pagina_actual=pagina,
                           total_paginas=total_paginas)

@app.route('/subir', methods=['POST'])
def subir():
    nombre = request.form['nombre']
    fecha = request.form['fecha']
    descripcion = request.form['descripcion']
    archivo = request.files['archivo']

    if archivo.filename != '':
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], archivo.filename)
        archivo.save(filepath)
        recuerdos.append({
            'nombre': nombre,
            'fecha': fecha,
            'descripcion': descripcion,
            'archivo': archivo.filename,
            'tipo': 'video' if archivo.filename.lower().endswith(('.mp4', '.mov', '.avi')) else 'imagen',
            'timestamp': datetime.now()
        })

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
    import os
port = int(os.environ.get("PORT", 5000))
app.run(debug=True, host="0.0.0.0", port=port)