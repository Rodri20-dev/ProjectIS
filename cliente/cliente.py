import requests
from zeep import Client
import json


# --- Configurações do Servidor ---
REST_URL_BASE = "http://host.docker.internal:5000/usuarios"
GRAPHQL_URL = "http://172.18.0.2:4000/graphql"




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
                usuario_atualizado = {"nome": "Teste REST Atualizado", "email": "teste.rest@example.com"}
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
    
    testar_rest()
    testar_graphql()