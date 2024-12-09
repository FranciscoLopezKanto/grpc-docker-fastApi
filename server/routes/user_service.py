import logging
from multiprocessing import context
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
from bson import ObjectId  # Aseguramos que estamos importando ObjectId

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
        new_user["_id"] = result.inserted_id  # Asegúrate de que el _id se guarde como ObjectId

        # Convertir el ObjectId a string antes de retornar el usuario
        return users_pb2.RegisterResponse(
            user=users_pb2.User(
                id=str(new_user["_id"]),  # Convertir ObjectId a string
                name=new_user["name"],
                email=new_user["email"],
                role=new_user["role"],
            ),
            message="User registered successfully"
        )

    def Login(self, request, context):
        user = find_user_by_email(request.email)
        if not user or user["password"] != request.password:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Credenciales inválidas")
        
        # Convertir el ObjectId a string antes de generar el token
        token = generate_token(str(user["_id"]))  # Aquí convertimos el ObjectId a string
        return users_pb2.LoginResponse(token=token)

    def GetUsers(self, request, context):
        # Obtener los metadatos de la solicitud
        metadata = dict(context.invocation_metadata())
        token = metadata.get('authorization')

        # Verificar si el token está presente
        if not token:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Token de autenticación no proporcionado.")
        
        # Verificar si el token es válido
        try:
            decoded_token = verify_token(token)
        except ValueError:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Token inválido.")
        
        # Si el token es válido, proceder con la lógica de negocio
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

        # Retornar los usuarios
        return users_pb2.GetUsersResponse(users=user_list)

    def GetUserById(self, request, context):
        # Buscar usuario por ID
        user = find_user_by_id(request.id)
        if not user:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("User not found")
            return users_pb2.GetUserByIdResponse()

        # Convertir el ObjectId a string antes de enviar la respuesta
        return users_pb2.GetUserByIdResponse(
            user=users_pb2.User(
                id=str(user["_id"]),  # Convertir ObjectId a string
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

    