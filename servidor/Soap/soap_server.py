from zeep import Server
from zeep.xsd import xsd_element, xsd_string, xsd_int

#   ---   Dados de exemplo (substitua pela sua lógica de persistência)   ---
dados = {}  #   Dicionário para armazenar os dados em memória

def criar_usuario(nome: str, email: str):
    """
    Operação SOAP para criar um novo usuário.
    """
    novo_id = str(len(dados) + 1)
    dados[novo_id] = {"id": novo_id, "nome": nome, "email": email}
    print(f"INFO: Criado usuário: {nome} ({email}) com ID: {novo_id}")
    return novo_id

def obter_usuario(id: str):
    """
    Operação SOAP para obter informações de um usuário por ID.
    """
    print(f"INFO: Obtendo usuário com ID: {id}")
    usuario = dados.get(id)
    if usuario:
        return usuario
    else:
        return None

def atualizar_usuario(id: str, nome: str = None, email: str = None):
    """
    Operação SOAP para atualizar informações de um usuário.
    """
    print(f"INFO: Atualizando usuário com ID: {id}")
    usuario = dados.get(id)
    if usuario:
        if nome:
            usuario["nome"] = nome
        if email:
            usuario["email"] = email
        return f"Usuário com ID '{id}' atualizado."
    else:
        return f"Usuário com ID '{id}' não encontrado."

def apagar_usuario(id: str):
    """
    Operação SOAP para apagar um usuário.
    """
    print(f"INFO: Apagando usuário com ID: {id}")
    usuario = dados.get(id)
    if usuario:
        del dados[id]
        return f"Usuário com ID '{id}' apagado."
    else:
        return f"Usuário com ID '{id}' não encontrado."

def exportar_usuarios():
    """
    Operação SOAP para exportar a lista de usuários para XML.
    """
    print("INFO: Exportando usuários para XML")
    #   Simples exemplo de formatação XML (adapte conforme necessário)
    xml_data = "<usuarios>"
    for usuario in dados.values():
        xml_data += f"<usuario><id>{usuario['id']}</id><nome>{usuario['nome']}</nome><email>{usuario['email']}</email></usuario>"
    xml_data += "</usuarios>"
    return xml_data

def importar_usuarios(xml_data: str):
    """
    Operação SOAP para importar usuários a partir de XML.
    """
    print("INFO: Importando usuários de XML")
    print(f"INFO: Dados XML:\n{xml_data}")
    #   Implemente a lógica para analisar o XML e criar/atualizar usuários
    #   Este é apenas um exemplo de como você pode começar a analisar o XML
    #   Você provavelmente precisará de uma biblioteca XML para fazer isso corretamente
    #   E.g., xml.etree.ElementTree in Python
    #   Para este exemplo, apenas retornamos uma mensagem
    return "Importação de usuários de XML não implementada."

#   ---   Mapeamento das operações para o serviço   ---
service_map = {
    '{http://tempuri.org/servicos/usuario}': {  #   Namespace do seu WSDL
        'UsuarioPortType': {  #   Nome do seu portType no WSDL
            'CriarUsuario': criar_usuario,
            'ObterUsuario': obter_usuario,
            'AtualizarUsuario': atualizar_usuario,
            'ApagarUsuario': apagar_usuario,
            'ExportarUsuarios': exportar_usuarios,
            'ImportarUsuarios': importar_usuarios,
        }
    }
}

wsdl_file = 'servidor/wsdl/servico.wsdl'

if __name__ == '__main__':
    try:
        #   Inicializa o servidor SOAP
        server = Server(wsdl_file, service_map)
        print(
            "INFO: Servidor SOAP iniciado. Acessível em: http://localhost:8080/servicos/usuario?wsdl")
        server.serve(host='0.0.0.0', port=8080)
    except Exception as e:
        print(f"ERRO: Ocorreu um erro ao iniciar o servidor SOAP: {e}")