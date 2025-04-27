import grpc
import cliente_grpc.servico_pb2
import cliente_grpc.servico_pb2_grpc

def run():
    # Conectando ao servidor gRPC
    channel = grpc.insecure_channel('localhost:50051')  # Ajuste a porta para a do servidor
    stub = cliente_grpc.service_pb2_grpc.UserServiceStub(channel)

    # Criando um usuário
    create_user_request = cliente_grpc.service_pb2.CreateUserRequest(nome="Teste", email="teste@example.com")
    create_user_response = stub.CreateUser(create_user_request)
    print(f"User created with ID: {create_user_response.id}")

    # Obtendo um usuário
    get_user_request = cliente_grpc.service_pb2.GetUserRequest(id=create_user_response.id)
    get_user_response = stub.GetUser(get_user_request)
    print(f"User details - ID: {get_user_response.id}, Nome: {get_user_response.nome}, Email: {get_user_response.email}")

if __name__ == '__main__':
    run()
