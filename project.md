# Roteiro Detalhado para o Desenvolvimento do Trabalho Prático Individual

Este documento detalha os passos necessários para a conclusão do trabalho prático individual de "Desenvolvimento de Serviços Web Multitecnologia", incluindo comandos relevantes.

## Fase 1: Planeamento e Configuração (Até [Data Limite Sugerida])

1.  **Compreensão dos Requisitos:**
    * Ler atentamente o documento "Enunciado trabalho Individual.pdf".
    * Identificar as tecnologias a implementar: SOAP, REST, GraphQL, gRPC.
    * Identificar as funcionalidades: operações CRUD, exportação/importação de dados.
    * Identificar os formatos de dados: XML e JSON.
    * Entender a necessidade de validação (XSD para SOAP, JSON Schema para REST).
    * Compreender a estrutura do repositório sugerida (`/servidor`, `/cliente`, `/documentacao`, `docker-compose.yml` (se aplicável)).

2.  **Escolha da Linguagem:**
    * Decidir entre Python ou Node.js para o desenvolvimento do servidor.
    * Decidir entre Python ou JavaScript para o desenvolvimento do cliente.
    * **Exemplo (Python):** Se escolher Python, precisará de ter o Python instalado. Verifique a versão com `python --version` ou `python3 --version`.
    * **Exemplo (Node.js):** Se escolher Node.js, precisará de ter o Node.js e npm instalados. Verifique as versões com `node -v` e `npm -v`.

3.  **Definição do Recurso:**
    * Escolher um recurso para implementar as operações CRUD (ex: utilizadores, produtos, etc.). Esta escolha deve ser feita com base na simplicidade e na capacidade de demonstrar as funcionalidades.

4.  **Escolha do Formato Principal:**
    * Decidir se o formato principal de persistência de dados será JSON ou XML.
    * **Nota:** A capacidade de converter entre os dois formatos é crucial para as funcionalidades de exportação e importação.

5.  **Configuração do Ambiente de Desenvolvimento:**
    * **Instalação de Ferramentas (Exemplo Python):**
        * Instalar `pip` se ainda não estiver instalado: `sudo apt update && sudo apt install python3-pip` (para Ubuntu/Debian).
        * Criar um ambiente virtual (opcional, mas recomendado): `python3 -m venv venv`
        * Ativar o ambiente virtual: `source venv/bin/activate` (Linux/macOS) ou `venv\Scripts\activate` (Windows).
    * **Instalação de Ferramentas (Exemplo Node.js):**
        * Inicializar um projeto Node.js (se ainda não tiver): `npm init -y`
    * **Instalação do Docker e Docker Compose (se aplicável):**
        * Instalar o Docker: Siga as instruções em [https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/).
        * Instalar o Docker Compose: Siga as instruções em [https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/).
    * **Instalação do Postman:**
        * Descarregar e instalar o Postman a partir do site oficial: [https://www.postman.com/downloads/](https://www.postman.com/downloads/).
    * **Criação da Estrutura Inicial do Repositório (Localmente):**
        ```bash
        mkdir trabalho-pratico-web
        cd trabalho-pratico-web
        mkdir servidor cliente documentacao
        touch docker-compose.yml # Criar arquivo vazio se for usar Docker
        ```
    * **Inicialização do Repositório Git (Localmente):**
        ```bash
        git init
        ```

6.  **Criação do Repositório GitHub e Adição do Colaborador:**
    * Criar um novo repositório no GitHub com o nome desejado (sugestão: `trabalho-pratico-web`).
    * Adicionar o professor como colaborador no repositório GitHub, concedendo permissões de leitura.
    * Obter o link do repositório GitHub.
    * Enviar o link do repositório por email ao professor o mais cedo possível.

## Fase 2: Desenvolvimento do Servidor (Até [Data Limite Sugerida])

1.  **Implementação do Servidor SOAP:**
    * **Configurar o ambiente para SOAP:**
        * **Python (Exemplo com `zeep`):** Instalar a biblioteca `zeep`: `pip install zeep`
        * **Node.js (Exemplo com `soap`):** Instalar a biblioteca `soap`: `npm install soap`
    * **Definir o contrato WSDL:**
        * Criar um arquivo WSDL (ex: `servidor/wsdl/servico.wsdl`) que defina as operações SOAP (criar, ler, atualizar, apagar) para o recurso escolhido.
        * Definir os tipos de dados e as mensagens no WSDL.
    * **Implementar os serviços SOAP:**
        * Escrever o código do servidor que implementa as operações definidas no WSDL.
        * **Exemplo Python com `zeep`:**
            ```python
            # servidor/soap_server.py
            from zeep import Server
            from zeep.xsd import xsd_element, xsd_string, xsd_int

            # Defina as operações SOAP aqui (ex: criar_usuario, obter_usuario, etc.)
            def criar_usuario(nome: str, email: str):
                # Lógica para criar usuário
                print(f"Criando usuário: {nome} ({email})")
                return f"Usuário {nome} criado com sucesso."

            # ... outras operações ...

            service_map = {
                '{[http://tempuri.org/](http://tempuri.org/)}' : {
                    'ServicoUsuario': {
                        'criarUsuario': criar_usuario,
                        # ... outras operações ...
                    }
                }
            }

            wsdl_file = 'servidor/wsdl/servico.wsdl'
            server = Server(wsdl_file, service_map)
            # ... código para iniciar o servidor SOAP ...
            ```
        * **Exemplo Node.js com `soap`:**
            ```javascript
            // servidor/soap_server.js
            const soap = require('soap');
            const http = require('http');
            const fs = require('fs');

            const service = {
              ServicoUsuario: {
                ServicoUsuarioSoap: {
                  criarUsuario: function(args, callback) {
                    console.log(`Criando usuário: ${args.nome} (${args.email})`);
                    callback(null, { resultado: `Usuário ${args.nome} criado com sucesso.` });
                  },
                  // ... outras operações ...
                }
              }
            };

            const xml = fs.readFileSync('servidor/wsdl/servico.wsdl', 'utf8');
            const server = http.createServer(function(request, response) {
              response.end('404: Not Found: ' + request.url);
            });

            server.listen(8080, function() {
              soap.listen(server, '/servico', service, xml, function() {
                console.log('SOAP service listening on port 8080');
              });
            });
            ```
    * **Validação XSD:**
        * Implementar a validação das requisições SOAP usando o arquivo WSDL (que contém as definições XSD). A biblioteca SOAP escolhida geralmente lida com isso automaticamente.

2.  **Implementação do Servidor REST:**
    * **Escolher um framework REST (Exemplo Python com Flask):**
        * Instalar Flask: `pip install Flask`
        * **Exemplo Node.js com Express:**
        * Instalar Express: `npm install express`
    * **Definir os endpoints REST:**
        * Definir as URLs para as operações CRUD (ex: `/usuarios`, `/usuarios/{id}`).
    * **Implementar a validação JSON Schema:**
        * Usar bibliotecas de validação JSON Schema (ex: `jsonschema` para Python).
        * Definir os esquemas JSON para as requisições (corpo das requisições POST/PUT) e respostas.
        * **Exemplo Python com Flask e `jsonschema`:**
            ```python
            # servidor/rest_server.py
            from flask import Flask, request, jsonify
            from jsonschema import validate, ValidationError

            app = Flask(__name__)

            usuario_schema = {
                "type": "object",
                "properties": {
                    "nome": {"type": "string"},
                    "email": {"type": "string", "format": "email"}
                },
                "required": ["nome", "email"]
            }

            usuarios = []
            next_id = 1

            @app.route('/usuarios', methods=['POST'])
            def criar_usuario_rest():
                try:
                    data = request.get_json()
                    validate(instance=data, schema=usuario_schema)
                    global next_id
                    data['id'] = next_id
                    usuarios.append(data)
                    next_id += 1
                    return jsonify(data), 201
                except ValidationError as e:
                    return jsonify({"error": str(e)}), 400
                except Exception as e:
                    return jsonify({"error": str(e)}), 500

            # ... outras rotas REST (GET, PUT, DELETE) ...

            if __name__ == '__main__':
                app.run(debug=True)
            ```
        * **Exemplo Node.js com Express e `express-joi`:**
            ```javascript
            // servidor/rest_server.js
            const express = require('express');
            const bodyParser = require('body-parser');
            const Joi = require('joi');

            const app = express();
            app.use(bodyParser.json());

            const usuarios = [];
            let nextId = 1;

            const usuarioSchema = Joi.object({
              nome: Joi.string().required(),
              email: Joi.string().email().required()
            });

            app.post('/usuarios', (req, res) => {
              const { error, value } = usuarioSchema.validate(req.body);
              if (error) {
                return res.status(400).json({ error: error.details[0].message });
              }
              value.id = nextId++;
              usuarios.push(value);
              res.status(201).json(value);
            });

            // ... outras rotas REST (GET, PUT, DELETE) ...

            const port = 3000;
            app.listen(port, () => {
              console.log(`REST server listening on port ${port}`);
            });
            ```
    * **Implementar a funcionalidade de consultas JSONPath:**
        * Usar uma biblioteca JSONPath (ex: `jsonpath` para Python, `jsonpath-plus` para Node.js) para permitir que os clientes consultem dados específicos usando expressões JSONPath. Implementar um endpoint (ex: `/usuarios/query?path=$.[?(@.nome=='John')]`).

3.  **Implementação do Servidor GraphQL:**
    * **Configurar o ambiente para GraphQL (Exemplo Python com `graphene`):**
        * Instalar `graphene`: `pip install graphene flask`
        * **Exemplo Node.js com `apollo-server-express`:**
        * Instalar `apollo-server-express`: `npm install apollo-server-express graphql`
    * **Definir o esquema GraphQL:**
        * Criar um arquivo com o esquema GraphQL (`servidor/graphql/schema.py` ou `servidor/graphql/schema.js`).
        * Definir os tipos, queries e mutations para o recurso escolhido.
        * **Exemplo Python com `graphene`:**
            ```python
            # servidor/graphql/schema.py
            import graphene

            class Usuario(graphene.ObjectType):
                id = graphene.ID()
                nome = graphene.String()
                email = graphene.String()

            class Query(graphene.ObjectType):
                usuarios = graphene.List(Usuario)
                usuario = graphene.Field(Usuario, id=graphene.ID(required=True))

                def resolve_usuarios(self, info):
                    # Lógica para obter todos os usuários
                    return [{'id': 1, 'nome': 'Alice', 'email': '[endereço de e-mail removido]'}]

                def resolve_usuario(self, info, id):
                    # Lógica para obter um usuário por ID
                    if id == '1':
                        return {'id': 1, 'nome': 'Alice', 'email': '[endereço de e-mail removido]'}
                    return None

            class CreateUsuario(graphene.Mutation):
                class Arguments:
                    nome = graphene.String(required=True)
                    email = graphene.String(required=True)

                usuario = graphene.Field(Usuario)

                def mutate(self, info, nome, email):
                    # Lógica para criar usuário
                    usuario = {'id': '2', 'nome': nome, 'email': email}
                    return CreateUsuario(usuario=usuario)

            class Mutation(graphene.ObjectType):
                create_usuario = CreateUsuario.Field()

            schema = graphene.Schema(query=Query, mutation=Mutation)
            ```
        * **Exemplo Node.js com `apollo-server-express`:**
            ```javascript
            // servidor/graphql/schema.js
            const { ApolloServer, gql } = require('apollo-server-express');

            const typeDefs = gql`
              type Usuario {
                id: ID!
                nome: String!
                email: String!
              }

              type Query {
                usuarios: [Usuario!]!
                usuario(id: ID!): Usuario
              }

              type Mutation {
                createUsuario(nome: String!, email: String!): Usuario!
              }
            `;

            const usuarios = [{ id: '1', nome: 'Bob', email: '[endereço de e-mail removido]' }];

            const resolvers = {
              Query: {
                usuarios: () => usuarios,
                usuario: (parent, { id }) => usuarios.find(u => u.id === id),
              },
              Mutation: {
                createUsuario: (parent, { nome, email }) => {
                  const novoUsuario = { id: String(usuarios.length + 1), nome, email };
                  usuarios.push(novoUsuario);
                  return novoUsuario;
                },
              },
            };

            const server = new ApolloServer({ typeDefs, resolvers });
            module.exports = server;
            ```
    * **Implementar os resolvers:**
        * Escrever as funções que resolvem as queries e mutations no esquema GraphQL.

4.  **Implementação do Servidor gRPC:**
    * **Definir os serviços gRPC (.proto):**
        * Criar um arquivo `.proto` (ex: `servidor/grpc/servico.proto`) que define os serviços gRPC (unários e streaming) e as mensagens.
        * **Exemplo:**
            ```protobuf
            // servidor/grpc/servico.proto
            syntax = "proto3";

            package servico;

            service UsuarioService {
              rpc CriarUsuario (UsuarioRequest) returns (UsuarioResponse);
              rpc ObterUsuario (ObterUsuarioRequest) returns (UsuarioResponse);
              rpc ListarUsuarios (google.protobuf.Empty) returns (stream UsuarioResponse);
            }

            message UsuarioRequest {
              string nome = 1;
              string email = 2;
            }

            message ObterUsuarioRequest {
              string id = 1;
            }

            message UsuarioResponse {
              string id = 1;
              string nome = 2;
              string email = 3;
            }
            ```
    * **Implementar os handlers:**
        * Gerar o código de stub e implementar os handlers para os serviços gRPC usando a linguagem escolhida (ex: `grpcio` para Python, `grpc` para Node.js).
        * **Exemplo Python com `grpcio`:**
            ```python
            # servidor/grpc_server.py
            import grpc
            from concurrent import futures
            import servico_pb2
            import servico_pb2_grpc

            class UsuarioServicer(servico_pb2_grpc.UsuarioServiceServicer):
                def __init__(self):
                    self.usuarios = {}
                    self.next_id = 1

                def CriarUsuario(self, request, context):
                    usuario_id = str(self.next_id)
                    self.usuarios[usuario_id] = {'id': usuario_id, 'nome': request.nome, 'email': request.email}
                    self.next_id += 1
                    return servico_pb2.UsuarioResponse(id=usuario_id, nome=request.nome, email=request.email)

                def ObterUsuario(self, request, context):
                    usuario_id = request.id
                    if usuario_id in self.usuarios:
                        usuario = self.usuarios[usuario_id]
                        return servico_pb2.UsuarioResponse(id=usuario['id'], nome=usuario['nome'], email=usuario['email'])
                    context.abort(grpc.StatusCode.NOT_FOUND, f'Usuário com ID {usuario_id} não encontrado')
                    return servico_pb2.UsuarioResponse() # Não