import grpc
import users_pb2
import users_pb2_grpc


def run():
    print("Client started")

    # El token obtenido del login o algún proceso previo
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjc0M2JiZjg5OWMyNWUxNzQyZTQwNzVjIiwicm9sZSI6InVzZXIifQ.Tbg3AdhU-Tf42KResxe8s45n_ezCE-NECWGwQxBw09g"

    # Usar 'host.docker.internal' si el servidor está en Docker
    with grpc.insecure_channel('host.docker.internal:50051') as channel:
        stub = users_pb2_grpc.UsersStub(channel)

        # Crear los metadatos con el token de autorización
        metadata = [('authorization', token)]

        # Obtener lista de usuarios
        print("\n--- GetUsers ---")
        print(metadata)
        try:
            response = stub.GetUsers(users_pb2.GetUsersRequest(), metadata=metadata)
            for user in response.users:
                print(f"ID: {user.id}, Name: {user.name}, Email: {user.email}, Role: {user.role}")
        except grpc.RpcError as e:
            print(f"Error al obtener los usuarios: {e.details()} (Código: {e.code()})")


if __name__ == "__main__":
    run()
