from flask import Flask
from flask_graphql import GraphQLView
from graphene import Schema, ObjectType, String

# Exemplo básico de esquema GraphQL
class Query(ObjectType):
    hello = String(name=String(default_value="stranger"))

    def resolve_hello(self, info, name):
        return f"Hello, {name}"

schema = Schema(query=Query)

app = Flask(__name__)

# Configurando a rota GraphQL
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000)
