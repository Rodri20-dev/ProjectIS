# grpc_server.py

from concurrent import futures
import grpc
import servico_pb2
import servico_pb2_grpc

class UserService(servico_pb2_grpc.UserServiceServicer):
    def __init__(self):
        # Base de dados fake só para testes
        self.users = {}

    def CreateUser(self, request, context):
        user_id = str(len(self.users) + 1)
        self.users[user_id] = {
            "nome": request.nome,
            "email": request.email
        }
        return servico_pb2.CreateUserResponse(id=user_id)

    def GetUser(self, request, context):
        user = self.users.get(request.id)
        if user:
            return servico_pb2.GetUserResponse(
                id=request.id,
                nome=user["nome"],
                email=user["email"]
            )
        else:
            context.set_details('User not found')
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return servico_pb2.GetUserResponse()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servico_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor gRPC no ar na porta 50051 🚀")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
