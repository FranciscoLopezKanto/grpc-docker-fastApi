from __future__ import print_function
import logging
import grpc
import users_pb2
import users_pb2_grpc

def run():
    print("Client started")
    # Usar 'host.docker.internal' para conectar desde el cliente (fuera del contenedor) al servidor gRPC
    with grpc.insecure_channel('host.docker.internal:50051') as channel:
        stub = users_pb2_grpc.UsersStub(channel)
        
        # 1. GetUsers
        print("\n--- GetUsers ---")
        response = stub.GetUsers(users_pb2.GetUsersRequest())
        print("Users:", response.users)
        
        # 2. GetUserById
        print("\n--- GetUserById ---")
        user_id = "673bd00de0c32d501bb60db0"  # ObjectId válido
        try:
            response = stub.GetUserById(users_pb2.GetUserByIdRequest(id=user_id))
            print(f"User with ID {user_id}:", response.user)
        except grpc.RpcError as e:
            print(f"Error fetching user with ID {user_id}: {e.details()} (Code: {e.code()})")
        
        # 3. CreateUser
        print("\n--- CreateUser ---")
        new_user = users_pb2.User(
            id="673999312345323",  # Nuevo ObjectId válido
            name="daniel Bassanoo",
            email="bassanoo@example.com",
            password="mypassword"
        )
        response = stub.CreateUser(users_pb2.CreateUserRequest(user=new_user))
        print("Created User:", response.user)
        
        # 4. UpdateUser
        print("\n--- UpdateUser ---")
        updated_user = users_pb2.User(
            id="673bd0c7e0c32d501bb60db3",  # ObjectId válido existente
            name="Bassano Daniel",
            email="bassanodaniel@example.com",
            password="newpassword123"
        )
        try:
            response = stub.UpdateUser(users_pb2.UpdateUserRequest(user=updated_user))
            print("Updated User:", response.user)
        except grpc.RpcError as e:
            print(f"Error updating user with ID {updated_user.id}: {e.details()} (Code: {e.code()})")
        
        # 5. DeleteUser
        print("\n--- DeleteUser ---")
        user_to_delete = "6739f416984203f168732dbb"  # ObjectId válido
        try:
            response = stub.DeleteUser(users_pb2.DeleteUserRequest(id=user_to_delete))
            print(f"Deleted User with ID {user_to_delete}: {response.id}")
        except grpc.RpcError as e:
            print(f"Error deleting user with ID {user_to_delete}: {e.details()} (Code: {e.code()})")

if __name__ == '__main__':
    logging.basicConfig()
    run()
