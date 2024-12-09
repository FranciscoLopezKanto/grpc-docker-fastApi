import logging
from routes.user_service import UserService
import grpc
from concurrent import futures
import users_pb2_grpc

# Configurar el logging para que solo se vean los logs de tu aplicación
logging.basicConfig(level=logging.INFO)  # Solo logs INFO y superiores

# Establecer el nivel de logging para MongoDB (o cualquier otro módulo)
logging.getLogger('mongodb').setLevel(logging.WARNING)  # Solo mostrar WARNINGS y errores de MongoDB
logging.getLogger('pymongo').setLevel(logging.WARNING)  # Si usas pymongo, puedes ajustar este logger también

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    users_pb2_grpc.add_UsersServicer_to_server(UserService(), server)
    server.add_insecure_port("[::]:50051")
    logging.info("Server running on port 50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
