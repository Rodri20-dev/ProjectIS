import requests
from zeep import Client
import json
import grpc
import servico_pb2
import servico_pb2_grpcSe

# --- Configurações do Servidor ---
SOAP_URL = "http://localhost:8080/servicos/usuario?wsdl"
REST_URL_BASE = "http://localhost:5000/usuarios"
GRAPHQL_URL = "http://localhost:4000/graphql"
GRPC_TARGET = 'localhost:50051'

# --- Funções para interagir com SOAP ---
def testar_soap():
    try:
        client = Client(SOAP_URL)

        # Criar usuário
        nome = "Teste SOAP"
        email = "teste.soap@example.com"
        criar_response = client.service.CriarUsuario(nome=nome, email=email)
        print(f"\nSOAP - Criar Usuário: {criar_response}")
        user_id = criar_response  # Assuming the ID is returned

        if user_id:
            # Obter usuário
            obter_response = client.service.ObterUsuario(id=user_id)
            print(f"SOAP - Obter Usuário ({user_id}): {obter_response}")

            # Atualizar usuário
            atualizar_response = client.service.AtualizarUsuario(id=user_id, nome="Teste SOAP Atualizado")
            print(f"SOAP - Atualizar Usuário ({user_id}): {atualizar_response}")

            # Apagar usuário
            apagar_response = client.service.ApagarUsuario(id=user_id)
            print(f"SOAP - Apagar Usuário ({user_id}): {apagar_response}")

        # Exportar usuários
        exportar_response = client.service.ExportarUsuarios()
        print(f"\nSOAP - Exportar Usuários:\n{exportar_response}")

    except Exception as e:
        print(f"Erro SOAP: {e}")

# --- Funções para interagir com REST ---
def testar_rest():
    try:
        # Criar usuário
        novo_usuario = {"nome": "Teste REST", "email": "teste.rest@example.com"}
        response_criar = requests.post(REST_URL_BASE, json=novo_usuario)
        print(f"\nREST - Criar Usuário (Código {response_criar.status_code}): {response_criar.json()}")
        if response_criar.status_code == 201:
            user_id = response_criar.json().get("id")
            if user_id:
                # Obter usuário
                response_obter = requests.get(f"{REST_URL_BASE}?id={user_id}")
                print(f"REST - Obter Usuário ({user_id}) (Código {response_obter.status_code}): {response_obter.json()}")

                # Atualizar usuário
                usuario_atualizado = {"nome": "Teste REST Atualizado"}
                response_atualizar = requests.put(f"{REST_URL_BASE}/{user_id}", json=usuario_atualizado)
                print(f"REST - Atualizar Usuário ({user_id}) (Código {response_atualizar.status_code}): {response_atualizar.json()}")

                # Apagar usuário
                response_apagar = requests.delete(f"{REST_URL_BASE}/{user_id}")
                print(f"REST - Apagar Usuário ({user_id}) (Código {response_apagar.status_code}): {response_apagar.json()}")

        # Exportar usuários (assumindo um endpoint /exportar)
        response_exportar = requests.get(f"{REST_URL_BASE}/exportar")
        print(f"\nREST - Exportar Usuários (Código {response_exportar.status_code}): {response_exportar.text}")

    except requests.exceptions.RequestException as e:
        print(f"Erro REST: {e}")
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON da resposta REST: {e}")

# --- Funções para interagir com GraphQL ---
def testar_graphql():
    try:
        query_criar = """
            mutation {
              criarUsuario(nome: "Teste GraphQL", email: "teste.graphql@example.com") {
                id
                nome
                email
              }
            }
        """
        response_criar = requests.post(GRAPHQL_URL, json={'query': query_criar})
        print(f"\nGraphQL - Criar Usuário (Código {response_criar.status_code}): {response_criar.json()}")
        if response_criar.status_code == 200:
            data = response_criar.json().get('data')
            if data and data.get('criarUsuario'):
                user_id = data['criarUsuario']['id']
                print(f"GraphQL - ID do usuário criado: {user_id}")

                query_obter = f"""
                    query {{
                      usuarios(id: "{user_id}") {{
                        id
                        nome
                        email
                      }}
                    }}
                """
                response_obter = requests.post(GRAPHQL_URL, json={'query': query_obter})
                print(f"GraphQL - Obter Usuário ({user_id}) (Código {response_obter.status_code}): {response_obter.json()}")

                mutation_atualizar = f"""
                    mutation {{
                      atualizarUsuario(id: "{user_id}", nome: "Teste GraphQL Atualizado") {{
                        id
                        nome
                        email
                      }}
                    }}
                """
                response_atualizar = requests.post(GRAPHQL_URL, json={'query': mutation_atualizar})
                print(f"GraphQL - Atualizar Usuário ({user_id}) (Código {response_atualizar.status_code}): {response_atualizar.json()}")

                mutation_apagar = f"""
                    mutation {{
                      apagarUsuario(id: "{user_id}") {{
                        id
                      }}
                    }}
                """
                response_apagar = requests.post(GRAPHQL_URL, json={'query': mutation_apagar})
                print(f"GraphQL - Apagar Usuário ({user_id}) (Código {response_apagar.status_code}): {response_apagar.json()}")

    except requests.exceptions.RequestException as e:
        print(f"Erro GraphQL: {e}")
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON da resposta GraphQL: {e}")

# --- Funções para interagir com gRPC ---
def testar_grpc():
    try:
        channel = grpc.insecure_channel(GRPC_TARGET)
        stub = servico_pb2_grpc.ServicoUsuarioStub(channel)

        # Criar usuário
        criar_request = servico_pb2.CriarUsuarioRequest(nome="Teste gRPC", email="teste.grpc@example.com")
        response_criar = stub.CriarUsuario(criar_request)
        print(f"\ngRPC - Criar Usuário: {response_criar}")
        user_id = response_criar.id

        if user_id:
            # Obter usuário
            obter_request = servico_pb2.ObterUsuarioRequest(id=user_id)
            response_obter = stub.ObterUsuario(obter_request)
            print(f"gRPC - Obter Usuário ({user_id}): {response_obter}")

            # Atualizar usuário
            atualizar_request = servico_pb2.AtualizarUsuarioRequest(id=user_id, nome="Teste gRPC Atualizado")
            response_atualizar = stub.AtualizarUsuario(atualizar_request)
            print(f"gRPC - Atualizar Usuário ({user_id}): {response_atualizar}")

            # Apagar usuário
            apagar_request = servico_pb2.ApagarUsuarioRequest(id=user_id)
            response_apagar = stub.ApagarUsuario(apagar_request)
            print(f"gRPC - Apagar Usuário ({user_id}): {response_apagar}")

        # Exportar usuários (assumindo formato JSON)
        exportar_request_json = servico_pb2.ExportarUsuariosRequest(formato='json')
        response_exportar_json = stub.ExportarUsuarios(exportar_request_json)
        print(f"\ngRPC - Exportar Usuários (JSON):\n{response_exportar_json.dados}")

        # Exportar usuários (assumindo formato XML)
        exportar_request_xml = servico_pb2.ExportarUsuariosRequest(formato='xml')
        response_exportar_xml = stub.ExportarUsuarios(exportar_request_xml)
        print(f"gRPC - Exportar Usuários (XML):\n{response_exportar_xml.dados}")

        channel.close()

    except grpc.RpcError as e:
        print(f"Erro gRPC: {e}")

if __name__ == "__main__":
    import requests
    try:
        from zeep import Client
    except ImportError:
        print("A biblioteca zeep não está instalada. Por favor, instale-a (pip install zeep).")
    try:
        import graphene
    except ImportError:
        print("A biblioteca graphene não está instalada. Por favor, instale-a (pip install graphene).")
    try:
        import grpc
        import servico_pb2
        import servico_pb2_grpc
    except ImportError:
        print("As bibliotecas gRPC não estão instaladas. Por favor, instale-as (pip install grpcio grpcio-tools protobuf).")

    testar_soap()
    testar_rest()
    testar_graphql()
    testar_grpc()