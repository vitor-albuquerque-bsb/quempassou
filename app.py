from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Carregar dados do CSV com delimitador ';'
df = pd.read_csv(r'C:\Users\euvit\Desktop\PROJETO QUEM PASSOU\my_flask_app\union.csv', delimiter=';')

@app.route('/')
def index():
    orgaos = df['nome_orgao'].unique().tolist()
    orgaos.sort()  # Ordena os órgãos alfabeticamente
    anos = df['ano_edital'].unique().tolist()
    anos.sort()  # Ordena os anos alfabeticamente
    cargos = df['cargo_especialidade'].unique().tolist()
    cargos.sort()  # Ordena os cargos alfabeticamente
    return render_template('index.html', orgaos=orgaos, anos=anos, cargos=cargos)

@app.route('/data')
def data():
    filter_orgao = request.args.get('filter_orgao', '')
    filter_ano_edital = request.args.get('filter_ano_edital', '')
    filter_cargo_especialidade = request.args.get('filter_cargo_especialidade', '')
    filter_nome_candidato = request.args.get('filter_nome_candidato', '')
    page = int(request.args.get('page', 1))
    page_size = request.args.get('page_size', '10')

    if page_size == 'all':
        PAGE_SIZE = len(df)
    else:
        PAGE_SIZE = int(page_size)

    filtered_df = df

    if filter_orgao:
        filtered_df = filtered_df[filtered_df['nome_orgao'] == filter_orgao]
    if filter_ano_edital:
        filtered_df = filtered_df[filtered_df['ano_edital'] == int(filter_ano_edital)]
    if filter_cargo_especialidade:
        filtered_df = filtered_df[filtered_df['cargo_especialidade'] == filter_cargo_especialidade]
    if filter_nome_candidato:
        filtered_df = filtered_df[filtered_df['nome_candidato'].str.contains(filter_nome_candidato, case=False, na=False)]

    # Substituir NaN por ''
    filtered_df = filtered_df.fillna('')

    # Calcular o índice de início e fim para a página atual
    start_idx = (page - 1) * PAGE_SIZE
    end_idx = start_idx + PAGE_SIZE

    # Dados da página atual
    page_data = filtered_df.iloc[start_idx:end_idx].to_dict(orient='records')

    total_pages = (len(filtered_df) // PAGE_SIZE) + (1 if len(filtered_df) % PAGE_SIZE != 0 else 0)

    return jsonify({'data': page_data, 'page': page, 'total_pages': total_pages})


if __name__ == '__main__':
    app.run(debug=True)
