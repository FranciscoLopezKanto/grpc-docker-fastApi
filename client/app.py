import grpc
import users_pb2
import users_pb2_grpc

def get_users(token):
    # Conectar con el servidor gRPC
    with grpc.insecure_channel('host.docker.internal:50051') as channel:
        stub = users_pb2_grpc.UsersStub(channel)

        # Crear los metadatos con el token de autorización
        metadata = [('authorization', token)]  # Asegúrate de pasar el token correctamente

        try:
            # Realizar la solicitud de obtener usuarios con los metadatos
            response = stub.GetUsers(users_pb2.GetUsersRequest(), metadata=metadata)

            # Mostrar los usuarios obtenidos
            for user in response.users:
                print(f"ID: {user.id}, Name: {user.name}, Email: {user.email}, Role: {user.role}")
        except grpc.RpcError as e:
            print(f"Error al obtener los usuarios: {e.details()} (Código: {e.code()})")

if __name__ == "__main__":
    # El token recibido tras el login
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjc1NzIwZDI4ZmJhZTRlYmY0Mjk5YTJjIiwicm9sZSI6InVzZXIifQ.4FtFaYVAgmFSvloyLLOIsNe7X6BtDK6mNxDAWJFPFjQ"

    get_users(token)
