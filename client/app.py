import users_pb2
import users_pb2_grpc
import grpc


def criar_token(stub, email, password):
    """Cria um token para autenticar usuários"""
    




def create_user(stub, name, email, password):
    """Cria um usuário no servidor gRPC."""
    request = users_pb2.CreateUserRequest(
        user=users_pb2.User(
            name=name,
            email=email,
            password=password
        )
    )
    response = stub.CreateUser(request)
    return response.user



def get_user_by_id(stub, user_id):
    """Busca um usuário pelo ID no servidor gRPC."""
    request = users_pb2.GetUsersByIdRequest(id=user_id)
    try:
        response = stub.GetUserById(request)
        return response.user
    except grpc.RpcError as e:
        print(f"Erro ao buscar usuário: {e.details()} (Código: {e.code()})")
        return None

def update_user(stub, id, name, email, password):
    """Atualizar um usuário no servidor gRPC."""
    get_user_by_id(stub,id)
    
    request = users_pb2.UpdateUserRequest(
        user=users_pb2.User(
            id=str(id),
            name=name,
            email=email,
            password=password
        )
    )
    response = stub.UpdateUser(request)
    return response.user

def delete_user(stub,id):
   
    
    request = users_pb2.DeleteUserRequest(
            id=id)
    try:
        response = stub.DeleteUser(request)
        return print(f"Usuário deletado {response.user}")
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.NOT_FOUND:
            print(f"Erro: {e.details()}")
        else:
            print(f"Erro inesperado: {e.details()}")
    

def run():
    """Função principal do cliente."""
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = users_pb2_grpc.UsersStub(channel)

        # Criar usuário
        #user = create_user(stub, "Jean Miguel", "teste@gmail.com", "123")
        #print("Created User:", user)

        # Buscar usuário pelo ID informado pelo terminal
        #user_id = input("Informe o id do usuário que deseja atualizar: ")
        #get_user = get_user_by_id(stub,'3')
        
        #print("User", get_user)
       # update_user(stub, id='7', name="Ruan", email="hacker@gmail.com", password="fuihackeado")
            
        #fetched_user = update_user(stub, id='7', name="Ruan", email="hacker@gmail.com", password="fuihackeado")
        #if fetched_user:
            #print("User updated ID:", fetched_user)
            
        #deletar usuario
        
        deleted_user = delete_user(stub, "2")
        print("usuário deletado ", deleted_user)

if __name__ == '__main__':
    run()