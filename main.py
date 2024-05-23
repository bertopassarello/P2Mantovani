import pyodbc
from flask import Flask, request, render_template

dados_conexao = (
    "Driver={SQL Server};"
    "Server=DESKTOP-CDHJQUJ;"
    "Database=ProjectPython;"
)
conexao = pyodbc.connect(dados_conexao)
cursor = conexao.cursor()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'UMBERTO'

@app.route('/')
def home():
    return render_template('home.html')

#INSERINDO RECEITAS
@app.route('/add_receitas', methods=['POST'])
def add_receita():

    descricao = request.form.get('descricao')
    data_receita = request.form.get('date')
    valor_receita = request.form.get('valor_receita')

    add_receitas = f"""INSERT INTO RECEITAS(descricao, data_receita, valor_receita) VALUES
    ('{descricao}', '{data_receita}', {valor_receita})"""

    cursor.execute(add_receitas)
    cursor.commit()

    cursor.execute('select * from RECEITAS;')
    receitas = cursor.fetchall()
    cursor.execute('select * from GASTOS;')
    gastos = cursor.fetchall()

    return render_template("home.html", gastos=gastos,  receitas=receitas)

#INSERINDO GASTOS
@app.route('/add_gastos', methods=['POST'])
def add_gasto():

    descricao_gasto = request.form.get('descricao_gasto')
    data_gasto = request.form.get('data_gasto')
    valor_gasto = request.form.get('valor_gasto')
    
    add_gastos = f"""INSERT INTO GASTOS(descricao_gasto, data_gasto,valor_gasto) VALUES
    ('{descricao_gasto}', '{data_gasto}', {valor_gasto})"""

    cursor.execute(add_gastos)
    cursor.commit()

    cursor.execute('select * from RECEITAS;')
    receitas = cursor.fetchall()
    cursor.execute('select * from GASTOS;')
    gastos = cursor.fetchall()

    return render_template("home.html", gastos=gastos,  receitas=receitas)

#LISTANDO RECEITAS
@app.route('/listar_receitas')
def listar_receita():

    cursor.execute('select * from RECEITAS;')
    receitas = cursor.fetchall()

    return render_template("home.html", receitas=receitas)

#LISTANDO GASTOS
@app.route('/listar_gastos')
def listar_gasto():

    cursor.execute('select * from GASTOS;')
    gastos = cursor.fetchall()

    return render_template("home.html", gastos=gastos)

#EXCLUINDO RECEITAS
@app.route('/excluir_receitas', methods=['POST'])
def excluir_receitas():

    receitaID = request.form.get('excluirReceita')
    cursor.execute(f"delete from receitas where id_receita= '{receitaID}';")
    cursor.commit()

    cursor.execute('select * from RECEITAS;')
    receitas = cursor.fetchall()
    cursor.execute('select * from GASTOS;')
    gastos = cursor.fetchall()

    return render_template("home.html", gastos=gastos, receitas=receitas)

#EXCLUINDO GASTOS
@app.route('/excluir_gastos', methods=['POST'])
def excluir_gastos():

    gastoID = request.form.get('excluirGasto')
    cursor.execute(f"delete from gastos where id_gasto='{gastoID}';")
    cursor.commit()

    cursor.execute('select * from RECEITAS;')
    receitas = cursor.fetchall()
    cursor.execute('select * from GASTOS;')
    gastos = cursor.fetchall()

    return render_template("home.html", gastos=gastos, receitas=receitas)

#LISTAR RESUMOS 
@app.route('/listar_resumo')
def listar_resumo():

    cursor.execute('SELECT SUM (valor_receita) FROM RECEITAS;')
    resumo_receitas = cursor.fetchall()
    cursor.execute('SELECT SUM (valor_gasto) FROM GASTOS;')
    resumo_gastos = cursor.fetchall()

    return render_template("home.html", resumo_gastos=resumo_gastos,  resumo_receitas=resumo_receitas)



app.run(port=5000,host='localhost', debug=True)