from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import uuid

app = Flask(__name__)

# Simulação de banco de dados em memória
pedidos = []
consultas = []

# Página do paciente - formulário de marcação
@app.route('/', methods=['GET', 'POST'])
def marcar_consulta():
    if request.method == 'POST':
        novo_pedido = {
            'id': str(uuid.uuid4()),
            'nome': request.form['nome'],
            'idade': request.form['idade'],
            'processo': request.form['processo'],
            'data_pedido': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'Pendente'
        }
        pedidos.append(novo_pedido)
        return render_template('recibo_pendente.html', pedido=novo_pedido)
    return render_template('marcar.html')

# Página do funcionário - lista de pedidos
@app.route('/gestor', methods=['GET', 'POST'])
def painel_gestor():
    if request.method == 'POST':
        id_pedido = request.form['id']
        data_consulta = request.form['data_consulta']
        hora_consulta = request.form['hora_consulta']
        ficha = request.form['ficha']

        for pedido in pedidos:
            if pedido['id'] == id_pedido:
                consulta = pedido.copy()
                consulta['data_consulta'] = data_consulta
                consulta['hora_consulta'] = hora_consulta
                consulta['ficha'] = ficha
                consulta['status'] = 'Confirmada'
                consultas.append(consulta)
                pedidos.remove(pedido)
                break

        return redirect(url_for('painel_gestor'))

    return render_template('painel_gestor.html', pedidos=pedidos, consultas=consultas)

# Página de recibo oficial
@app.route('/recibo/<id>')
def recibo(id):
    consulta = next((c for c in consultas if c['id'] == id), None)
    return render_template('recibo_final.html', consulta=consulta)

if __name__ == '__main__':
    app.run(debug=True)
