import unittest
from unittest.mock import patch, MagicMock
import grpc
import users_pb2
import users_pb2_grpc

class TestUserServiceClient(unittest.TestCase):

    @patch('grpc.insecure_channel')
    @patch('users_pb2_grpc.UsersStub')
    def test_get_users(self, MockUsersStub, MockChannel):
        # Setup mock objects
        channel_mock = MagicMock()
        stub_mock = MockUsersStub.return_value
        
        MockChannel.return_value = channel_mock
        stub_mock.GetUsers.return_value = users_pb2.GetUsersResponse(users=[
            users_pb2.User(id="1", name="John Doe", email="john@example.com", role="USER"),
            users_pb2.User(id="2", name="Jane Doe", email="jane@example.com", role="ADMIN"),
        ])

        # Run the function under test
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = users_pb2_grpc.UsersStub(channel)
            response = stub.GetUsers(users_pb2.GetUsersRequest(token="fake_token"))
        
        # Assertions
        self.assertEqual(len(response.users), 2)
        self.assertEqual(response.users[0].name, "John Doe")
        self.assertEqual(response.users[1].email, "jane@example.com")

    @patch('grpc.insecure_channel')
    @patch('users_pb2_grpc.UsersStub')
    def test_get_user_by_id(self, MockUsersStub, MockChannel):
        # Setup mock objects
        channel_mock = MagicMock()
        stub_mock = MockUsersStub.return_value
        
        MockChannel.return_value = channel_mock
        stub_mock.GetUserById.return_value = users_pb2.GetUserByIdResponse(
            user=users_pb2.User(id="1", name="John Doe", email="john@example.com", role="USER")
        )

        # Run the function under test
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = users_pb2_grpc.UsersStub(channel)
            response = stub.GetUserById(users_pb2.GetUserByIdRequest(id="1"))

        # Assertions
        self.assertEqual(response.user.name, "John Doe")
        self.assertEqual(response.user.id, "1")

    @patch('grpc.insecure_channel')
    @patch('users_pb2_grpc.UsersStub')
    def test_create_user(self, MockUsersStub, MockChannel):
        # Setup mock objects
        channel_mock = MagicMock()
        stub_mock = MockUsersStub.return_value
        
        MockChannel.return_value = channel_mock
        new_user = users_pb2.User(id="3", name="Alice", email="alice@example.com", role="user")
        stub_mock.Register.return_value = users_pb2.RegisterResponse(user=new_user, message="User created successfully")

        # Run the function under test
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = users_pb2_grpc.UsersStub(channel)
            response = stub.Register(users_pb2.RegisterRequest(name="Alice", email="alice@example.com", password="password", role="user"))

        # Assertions
        self.assertEqual(response.user.name, "Alice")
        self.assertEqual(response.user.email, "alice@example.com")
        self.assertEqual(response.message, "User created successfully")

    @patch('grpc.insecure_channel')
    @patch('users_pb2_grpc.UsersStub')
    def test_update_user(self, MockUsersStub, MockChannel):
        # Setup mock objects
        channel_mock = MagicMock()
        stub_mock = MockUsersStub.return_value
        
        MockChannel.return_value = channel_mock
        updated_user = users_pb2.User(id="1", name="Alice Updated", email="alice_updated@example.com", role="user")
        stub_mock.UpdateUser.return_value = users_pb2.UpdateUserResponse(user=updated_user)

        # Run the function under test
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = users_pb2_grpc.UsersStub(channel)
            response = stub.UpdateUser(users_pb2.UpdateUserRequest(user=updated_user))

        # Assertions
        self.assertEqual(response.user.name, "Alice Updated")
        self.assertEqual(response.user.email, "alice_updated@example.com")

    @patch('grpc.insecure_channel')
    @patch('users_pb2_grpc.UsersStub')
    def test_delete_user(self, MockUsersStub, MockChannel):
        # Setup mock objects
        channel_mock = MagicMock()
        stub_mock = MockUsersStub.return_value
        
        MockChannel.return_value = channel_mock
        stub_mock.DeleteUser.return_value = users_pb2.DeleteUserResponse(id="1")

        # Run the function under test
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = users_pb2_grpc.UsersStub(channel)
            response = stub.DeleteUser(users_pb2.DeleteUserRequest(id="1"))

        # Assertions
        self.assertEqual(response.id, "1")

if __name__ == '__main__':
    unittest.main(verbosity=2)