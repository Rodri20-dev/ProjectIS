import grpc
from concurrent import futures
import time

#   Importe os ficheiros gerados pelo Protocol Buffers
import servico_pb2
import servico_pb2_grpc

#   ---   Dados de exemplo (substitua pela sua lógica de persistência)   ---
dados = {}  #   Dicionário para armazenar os dados em memória
ultimo_id = 0

class ServicoUsuario(servico_pb2_grpc.ServicoUsuarioServicer):
    def CriarUsuario(self, request, context):
        """
        Implementa o serviço gRPC para criar um novo usuário.
        """
        global ultimo_id
        ultimo_id += 1
        novo_id = str(ultimo_id)
        dados[novo_id] = {"id": novo_id, "nome": request.nome, "email": request.email}
        print(f"INFO: Criado usuário: {request.nome} ({request.email}) com ID: {novo_id}")
        return servico_pb2.CriarUsuarioResponse(id=novo_id)

    def ObterUsuario(self, request, context):
        """
        Implementa o serviço gRPC para obter informações de um usuário por ID.
        """
        print(f"INFO: Obtendo usuário com ID: {request.id}")
        usuario = dados.get(request.id)
        if usuario:
            return servico_pb2.ObterUsuarioResponse(id=usuario["id"], nome=usuario["nome"], email=usuario["email"])
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Usuário não encontrado.")
            return servico_pb2.ObterUsuarioResponse()

    def AtualizarUsuario(self, request, context):
        """
        Implementa o serviço gRPC para atualizar informações de um usuário.
        """
        print(f"INFO: Atualizando usuário com ID: {request.id}")
        usuario = dados.get(request.id)
        if usuario:
            if request.nome:
                usuario["nome"] = request.nome
            if request.email:
                usuario["email"] = request.email
            return servico_pb2.AtualizarUsuarioResponse(mensagem=f"Usuário com ID '{request.id}' atualizado.")
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Usuário não encontrado.")
            return servico_pb2.AtualizarUsuarioResponse()

    def ApagarUsuario(self, request, context):
        """
        Implementa o serviço gRPC para apagar um usuário.
        """
        print(f"INFO: Apagando usuário com ID: {request.id}")
        usuario = dados.get(request.id)