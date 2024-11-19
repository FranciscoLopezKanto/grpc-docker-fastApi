from concurrent import futures
import logging

import grpc
import users_pb2
import users_pb2_grpc
from pymongo import MongoClient
from bson.objectid import ObjectId
#L3wOx7kWB3t0GXbs
# Configuración MongoDB
MONGO_URI = "mongodb+srv://Admin:L3wOx7kWB3t0GXbs@cluster0.azhio.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client["users_db"]
users_collection = db["users"]

class Users(users_pb2_grpc.UsersServicer):
    def GetUsers(self, request, context):
        logging.debug("Fetching all users from MongoDB")
        users_cursor = users_collection.find()
        users = [
            users_pb2.User(
                id=str(user["_id"]),
                name=user["name"],
                email=user["email"],
                password=user["password"]
            )
            for user in users_cursor
        ]
        return users_pb2.GetUsersResponse(users=users)

    def GetUserById(self, request, context):
        logging.debug(f"Fetching user by ID: {request.id}")
        user = users_collection.find_one({"_id": ObjectId(request.id)})
        if not user:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("User not found")
            return users_pb2.GetUserByIdResponse()
        return users_pb2.GetUserByIdResponse(
            user=users_pb2.User(
                id=str(user["_id"]),
                name=user["name"],
                email=user["email"],
                password=user["password"]
            )
        )

    def CreateUser(self, request, context):
        logging.debug(f"Creating user: {request.user.name}")
        new_user = {
            "name": request.user.name,
            "email": request.user.email,
            "password": request.user.password
        }
        result = users_collection.insert_one(new_user)
        new_user["_id"] = result.inserted_id
        return users_pb2.CreateUserResponse(
            user=users_pb2.User(
                id=str(new_user["_id"]),
                name=new_user["name"],
                email=new_user["email"],
                password=new_user["password"]
            )
        )

    def UpdateUser(self, request, context):
        logging.debug(f"Updating user: {request.user.id}")
        user_id = request.user.id
        updated_data = {
            "name": request.user.name,
            "email": request.user.email,
            "password": request.user.password
        }
        result = users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": updated_data})
        if result.matched_count == 0:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("User not found")
            return users_pb2.UpdateUserResponse()
        return users_pb2.UpdateUserResponse(
            user=request.user
        )

    def DeleteUser(self, request, context):
        logging.debug(f"Deleting user by ID: {request.id}")
        result = users_collection.delete_one({"_id": ObjectId(request.id)})
        if result.deleted_count == 0:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("User not found")
            return users_pb2.DeleteUserResponse()
        return users_pb2.DeleteUserResponse(id=request.id)

def serve():
    logging.basicConfig(level=logging.DEBUG)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    users_pb2_grpc.add_UsersServicer_to_server(Users(), server)
    server.add_insecure_port('[::]:50051')

    server.start()
    logging.debug("Server started at localhost:50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
