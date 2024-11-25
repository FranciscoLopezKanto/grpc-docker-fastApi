import logging
import grpc
import users_pb2
import users_pb2_grpc
from db.mongo import (
    find_user_by_email,
    find_user_by_id,
    find_all_users,
    insert_user,
    update_user,
    delete_user,
)
from utils.auth import generate_token, verify_token


class UserService(users_pb2_grpc.UsersServicer):
    def Register(self, request, context):
        logging.debug(f"Registering new user: {request.name}")
        
        # Verificar si el correo ya está registrado
        existing_user = find_user_by_email(request.email)
        if existing_user:
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details("Email already registered")
            return users_pb2.RegisterResponse()

        # Crear el nuevo usuario
        new_user = {
            "name": request.name,
            "email": request.email,
            "password": request.password,  # Nota: se recomienda hashear contraseñas
            "role": request.role or "user",  # Rol por defecto: usuario normal
        }
        result = insert_user(new_user)
        new_user["_id"] = result.inserted_id

        return users_pb2.RegisterResponse(
            user=users_pb2.User(
                id=str(new_user["_id"]),
                name=new_user["name"],
                email=new_user["email"],
                role=new_user["role"],
            ),
            message="User registered successfully"
        )

    def GetUsers(self, request, context):
        # Obtener el token desde el objeto de solicitud
        token = request.token

        if not token:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Token de autenticación no proporcionado.")

        # Validar el token
        if not verify_token(token):
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Token inválido.")

        # Si el token es válido, continuar con la lógica del servicio
        users = find_all_users()  # Lógica para obtener los usuarios
        user_list = [
            users_pb2.User(
                id=str(user["_id"]),
                name=user["name"],
                email=user["email"],
                role=user.get("role", "user"),
            )
            for user in users
        ]
        return users_pb2.GetUsersResponse(users=user_list)

    def GetUserById(self, request, context):
        # Buscar usuario por ID
        user = find_user_by_id(request.id)
        if not user:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("User not found")
            return users_pb2.GetUserByIdResponse()
        
        return users_pb2.GetUserByIdResponse(
            user=users_pb2.User(
                id=str(user["_id"]),
                name=user["name"],
                email=user["email"],
                role=user.get("role", "user"),
            )
        )

    def UpdateUser(self, request, context):
        # Actualizar datos del usuario
        result = update_user(request.user.id, {
            "name": request.user.name,
            "email": request.user.email,
            "role": request.user.role,
        })
        if result.matched_count == 0:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("User not found")
            return users_pb2.UpdateUserResponse()
        
        return users_pb2.UpdateUserResponse(user=request.user)

    def DeleteUser(self, request, context):
        # Eliminar usuario
        result = delete_user(request.id)
        if result.deleted_count == 0:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("User not found")
            return users_pb2.DeleteUserResponse()
        
        return users_pb2.DeleteUserResponse(id=request.id)