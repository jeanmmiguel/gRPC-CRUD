from concurrent import futures
import logging
import sqlalchemy
import grpc
import users_pb2
import users_pb2_grpc
from models import User, SessionLocal

import argparse
from concurrent import futures
import contextlib
import logging
import users_pb2
import users_pb2_grpc
import grpc

users_pb2, users_pb2_grpc = grpc.protos_and_services(
    "users.proto"
)

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.INFO)

_LISTEN_ADDRESS_TEMPLATE = "localhost:%d"
_SIGNATURE_HEADER_KEY = "x-signature"


class SignatureValidationInterceptor(grpc.ServerInterceptor):
    def __init__(self):
        def abort(ignored_request, context):
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid signature")

        self._abortion = grpc.unary_unary_rpc_method_handler(abort)

    def intercept_service(self, continuation, handler_call_details):
        # Example HandlerCallDetails object:
        #     _HandlerCallDetails(
        #       method=u'/helloworld.Greeter/SayHello',
        #       invocation_metadata=...)
        method_name = handler_call_details.method.split("/")[-1]
        expected_metadata = (_SIGNATURE_HEADER_KEY, method_name[::-1])
        if expected_metadata in handler_call_details.invocation_metadata:
            return continuation(handler_call_details)
        else:
            return self._abortion

    def GetUserById(self, request, context):
        session = SessionLocal()
        user_data = request.id
        user = session.query(User).filter_by(id=int(request.id)).first()
        
        if not user:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Usuário não encontrado")
            session.close()
            return users_pb2.GetUserByIdResponse()
        if user:
            return users_pb2.GetUserByIdResponse(
                 user=users_pb2.User(id=str(user.id),
                            name=user.name,
                            email=user.email,
                            password=user.password
                        )
                )
    
    def CreateUser(self, request, context):
        
        session = SessionLocal()
        user_data = request.user
        new_user = User(
                    user_data.name,
                    user_data.email,
                    user_data.password
                )
        session.add(new_user)
        session.commit()
        

        response =  users_pb2.CreateUserResponse(
                    user=users_pb2.User(
                        id=str(new_user.id),
                        name=new_user.name,
                        email=new_user.email,
                        password=new_user.password
                    )
                )
       
        session.close()
        return response
     
               
    def UpdateUser(self, request, context):
        
        session = SessionLocal()
        user_data = request.id
        user = session.query(User).filter_by(id=int(user_data.id)).first()
        user.name = user_data.name
        user.email = user_data.email
        user.password = user_data.password
        session.commit()
        

        response =  users_pb2.UpdateUserResponse(
                    user=users_pb2.User(
                        id=str(user.id),
                        name=user.name,
                        email=user.email,
                        password=user.password
                    )
                )
       
        session.close()
        return response
    
    def DeleteUser(self, request, context):
        
        session = SessionLocal()
        user = session.query(User).filter_by(id=int(request.id)).first()
        
        if user is not None:
            session.delete(user)
            session.commit()
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Usuário não encontrado")
            session.close()
           
        response = users_pb2.DeleteUserResponse(
              user = users_pb2.User(id=str(request.id),
                name=user.name,
                email=user.email,
                password=user.password
              )
            
        )
        session.close()
    
        return response
    
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10, ), interceptors=SignatureValidationInterceptor())
    users_pb2_grpc.add_UsersServicer_to_server(User(),server)
    server.add_insecure_port('localhost:50051')
    server.start()
    server.wait_for_termination()
    

if __name__ == '__main__':
    logging.basicConfig()
    serve()