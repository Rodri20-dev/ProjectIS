from flask import Flask
from flask_graphql import GraphQLView
from graphene import ObjectType, String, Schema, List, Field

app = Flask(__name__)

#   ---   Dados de exemplo (substitua pela sua lógica de persistência)   ---
dados = {}  #   Dicionário para armazenar os dados em memória
ultimo_id = 0

#   ---   Definição dos tipos GraphQL   ---
class Usuario(ObjectType):
    id = String()
    nome = String()
    email = String()

#   ---   Definição das Queries   ---
class Query(ObjectType):
    usuarios = List(Usuario, id=String())

    def resolve_usuarios(root, info, id=None):
        if id:
            print(f"INFO: Obtendo usuário com ID: {id}")
            return [dados.get(id)]
        else:
            print("INFO: Obtendo todos os usuários")
            return list(dados.values())

#   ---   Definição das Mutations   ---
class CriarUsuario(ObjectType):
    id = String()
    nome = String()
    email = String()

    def mutate(root, info, nome, email):
        global ultimo_id
        ultimo_id += 1
        novo_id = str(ultimo_id)
        dados[novo_id] = {"id": novo_id, "nome": nome, "email": email}
        print(f"INFO: Criado usuário: {nome} ({email}) com ID: {novo_id}")
        return CriarUsuario(id=novo_id, nome=nome, email=email)

class AtualizarUsuario(ObjectType):
    id = String()
    nome = String()
    email = String()

    def mutate(root, info, id, nome=None, email=None):
        print(f"INFO: Atualizando usuário com ID: {id}")
        usuario = dados.get(id)
        if usuario:
            if nome:
                usuario["nome"] = nome
            if email:
                usuario["email"] = email
            return AtualizarUsuario(id=id, nome=usuario["nome"], email=usuario["email"])
        else:
            return None

class ApagarUsuario(ObjectType):
    id = String()

    def mutate(root, info, id):
        print(f"INFO: Apagando usuário com ID: {id}")
        usuario = dados.get(id)
        if usuario:
            del dados[id]
            return ApagarUsuario(id=id)
        else:
            return None

class Mutation(ObjectType):
    criar_usuario = Field(CriarUsuario)
    atualizar_usuario = Field(AtualizarUsuario)
    apagar_usuario = Field(ApagarUsuario)

    def resolve_criar_usuario(root, info, nome, email):
        return CriarUsuario.mutate(root, info, nome, email)

    def resolve_atualizar_usuario(root, info, id, nome=None, email=None):
        return AtualizarUsuario.mutate(root, info, id, nome, email)

    def resolve_apagar_usuario(root, info, id):
        return ApagarUsuario.mutate(root, info, id)

#   ---   Definição do Schema   ---
schema = Schema(query=Query, mutation=Mutation)

#   ---   Adiciona o endpoint GraphQL   ---
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True  #   Habilita o GraphiQL para testes no navegador
    )
)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000)