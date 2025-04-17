from flask import Flask, jsonify, request
from jsonschema import validate
from jsonpath_ng import parse

app = Flask(__name__)

#   ---   Dados de exemplo (substitua pela sua lógica de persistência)   ---
dados = {}  #   Dicionário para armazenar os dados em memória
ultimo_id = 0

#   ---   JSON Schema para validação   ---
usuario_schema = {
    "type": "object",
    "properties": {
        "nome": {"type": "string"},
        "email": {"type": "string", "format": "email"}
    },
    "required": ["nome", "email"]
}

#   ---   Operações REST   ---
@app.route('/usuarios', methods=['POST'])
def criar_usuario():
    """
    Cria um novo usuário.
    """
    try:
        dados_usuario = request.get_json()
        validate(dados_usuario, usuario_schema)
        global ultimo_id
        ultimo_id += 1
        novo_id = str(ultimo_id)
        dados[novo_id] = {"id": novo_id, **dados_usuario}
        print(f"INFO: Criado usuário: {dados_usuario['nome']} ({dados_usuario['email']}) com ID: {novo_id}")
        return jsonify({"id": novo_id}), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

@app.route('/usuarios', methods=['GET'])
def obter_usuarios():
    """
    Obtém a lista de todos os usuários ou um usuário específico por ID.
    """
    id = request.args.get('id')
    if id:
        print(f"INFO: Obtendo usuário com ID: {id}")
        usuario = dados.get(id)
        if usuario:
            return jsonify(usuario)
        else:
            return jsonify({"mensagem": "Usuário não encontrado"}), 404
    else:
        print("INFO: Obtendo todos os usuários")
        return jsonify(list(dados.values()))

@app.route('/usuarios/<id>', methods=['PUT'])
def atualizar_usuario(id):
    """
    Atualiza um usuário existente.
    """
    print(f"INFO: Atualizando usuário com ID: {id}")
    usuario = dados.get(id)
    if usuario:
        try:
            dados_usuario = request.get_json()
            validate(dados_usuario, usuario_schema)
            usuario.update(dados_usuario)
            return jsonify({"mensagem": f"Usuário com ID '{id}' atualizado."})
        except Exception as e:
            return jsonify({"erro": str(e)}), 400
    else:
        return jsonify({"mensagem": "Usuário não encontrado"}), 404

@app.route('/usuarios/<id>', methods=['DELETE'])
def apagar_usuario(id):
    """
    Apaga um usuário existente.
    """
    print(f"INFO: Apagando usuário com ID: {id}")
    usuario = dados.get(id)
    if usuario:
        del dados[id]
        return jsonify({"mensagem": f"Usuário com ID '{id}' apagado."})
    else:
        return jsonify({"mensagem": "Usuário não encontrado"}), 404

@app.route('/usuarios/exportar', methods=['GET'])
def exportar_usuarios():
    """
    Exporta a lista de usuários para XML.
    """
    print("INFO: Exportando usuários para XML")
    #   Simples exemplo de formatação XML (adapte conforme necessário)
    xml_data = "<usuarios>"
    for usuario in dados.values():
        xml_data += f"<usuario><id>{usuario['id']}</id><nome>{usuario['nome']}</nome><email>{usuario['email']}</email></usuario>"
    xml_data += "</usuarios>"
    return xml_data

@app.route('/usuarios/importar', methods=['POST'])
def importar_usuarios():
    """
    Importa usuários a partir de XML.
    """
    print("INFO: Importando usuários de XML")
    xml_data = request.get_data(as_text=True)
    print(f"INFO: Dados XML:\n{xml_data}")
    #   Implemente a lógica para analisar o XML e criar/atualizar usuários
    #   Este é apenas um exemplo de como você pode começar
    #   Você provavelmente precisará de uma biblioteca XML para fazer isso corretamente
    #   E.g., xml.etree.ElementTree in Python
    #   Para este exemplo, apenas retornamos uma mensagem
    return jsonify({"mensagem": "Importação de usuários de XML não implementada."})

@app.route('/usuarios/consultar', methods=['GET'])
def consultar_usuarios():
    """
    Consulta usuários usando JSONPath.
    """
    jsonpath_expressao = request.args.get('jsonpath')
    if jsonpath_expressao:
        print(f"INFO: Consultando usuários com JSONPath: {jsonpath_expressao}")
        try:
            jsonpath_query = parse(jsonpath_expressao)
            resultados = [match.value for match in jsonpath_query.find(list(dados.values()))]
            return jsonify(resultados)
        except Exception as e:
            return jsonify({"erro": str(e)}), 400
    else:
        return jsonify({"mensagem": "Nenhuma expressão JSONPath fornecida."}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)