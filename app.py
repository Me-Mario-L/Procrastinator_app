from flask import Flask, render_template, request, url_for, redirect, flash
from flask_mysqldb import MySQL

# MYSQL CONNECTION
app = Flask(__name__)
app.config ['MYSQL_HOST'] = 'localhost'
app.config ['MYSQL_USER'] = 'root'
app.config ['MYSQL_PASSWORD'] = ''
app.config ['MYSQL_DB'] = 'nuevas_tasks'
mysql = MySQL(app)

# SETTINGS
app.secret_key = 'udutech'

@app.route('/temporal')
def temporal():
    return render_template ('testG.html')


@app.route('/')
def main():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM procras_app_tasks')
    data = cur.fetchall()
    return render_template('main.html', tasks = data)

@app.route('/add', methods=['POST'])
def add_task():
    if request.method == 'POST':
        title = request.form['task_title']
        description = request.form['description']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO procras_app_tasks (title, description) VALUES (%s, %s)', (title, description))
        mysql.connection.commit()
        flash('added succesfully')
    return redirect(url_for('main'))


@app.route('/delete/<string:id>')
def delete_task(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM procras_app_tasks WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('deleted succesfully')
    return redirect(url_for('main'))

@app.route('/edit/<string:id>')
def edit_task(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM procras_app_tasks WHERE id = {0}'.format(id))# HE UTILIZADO EL FORMAT POR QUE AL PARECER EL %s PRESENTA ERRORES, EN ESTA LINEA DE CODIGO, ADEMAS EN LOS FOROS RECOMIENDAN USAR EL FORMAT PRECISAMENTE POR EL MISMO MOTIVO POR EL QUE LO ESTOY UTILIZANDO
    data = cur.fetchall()
    print(data[0])
    return render_template('edit.html', task = data[0])

##LA POSIBILIDAD DE ACTUALIZACION, PARA EDITAR UNTEXTO DE LA BASE DE DATOS ESTARA ENDIENTE POR QUE ME HE ENCONTRADO DEMASIADOS INCONVENIENTES PARA MI YO ACTUAL.
# @app.route('/update/<string:id>', methods =['POST'])  
# def update(id):
#     if request.method == 'POST':
#         title = request.form['task_title']
#         description = request.form['description']
#         cur = mysql.connection.cursor()
#         cur.execute("UPDATE procras_app_tasks SET title = %s, description = %s, WHERE id = {0}". format(id) , (title, description,)) 
#         flash('updated')
    

if __name__ == '__main__':
    app.run(port=3000, debug=True)

