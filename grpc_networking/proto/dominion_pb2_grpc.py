# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import grpc_networking.proto.dominion_pb2 as dominion__pb2


class DominionServerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Join = channel.unary_stream(
            '/DominionServer/Join',
            request_serializer=dominion__pb2.PlayerInfo.SerializeToString,
            response_deserializer=dominion__pb2.Message.FromString,
        )
        self.Start = channel.unary_unary(
            '/DominionServer/Start',
            request_serializer=dominion__pb2.PlayerInfo.SerializeToString,
            response_deserializer=dominion__pb2.Response.FromString,
        )
        self.PlayCard = channel.unary_unary(
            '/DominionServer/PlayCard',
            request_serializer=dominion__pb2.Card.SerializeToString,
            response_deserializer=dominion__pb2.Response.FromString,
        )
        self.Buy = channel.unary_unary(
            '/DominionServer/Buy',
            request_serializer=dominion__pb2.Card.SerializeToString,
            response_deserializer=dominion__pb2.Response.FromString,
        )
        self.Done = channel.unary_unary(
            '/DominionServer/Done',
            request_serializer=dominion__pb2.PlayerInfo.SerializeToString,
            response_deserializer=dominion__pb2.Response.FromString,
        )


class DominionServerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Join(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Start(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PlayCard(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Buy(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Done(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DominionServerServicer_to_server(servicer, server):
    rpc_method_handlers = {
        'Join': grpc.unary_stream_rpc_method_handler(
            servicer.Join,
            request_deserializer=dominion__pb2.PlayerInfo.FromString,
            response_serializer=dominion__pb2.Message.SerializeToString,
        ),
        'Start': grpc.unary_unary_rpc_method_handler(
            servicer.Start,
            request_deserializer=dominion__pb2.PlayerInfo.FromString,
            response_serializer=dominion__pb2.Response.SerializeToString,
        ),
        'PlayCard': grpc.unary_unary_rpc_method_handler(
            servicer.PlayCard,
            request_deserializer=dominion__pb2.Card.FromString,
            response_serializer=dominion__pb2.Response.SerializeToString,
        ),
        'Buy': grpc.unary_unary_rpc_method_handler(
            servicer.Buy,
            request_deserializer=dominion__pb2.Card.FromString,
            response_serializer=dominion__pb2.Response.SerializeToString,
        ),
        'Done': grpc.unary_unary_rpc_method_handler(
            servicer.Done,
            request_deserializer=dominion__pb2.PlayerInfo.FromString,
            response_serializer=dominion__pb2.Response.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        'DominionServer', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class DominionServer(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Join(request,
             target,
             options=(),
             channel_credentials=None,
             call_credentials=None,
             compression=None,
             wait_for_ready=None,
             timeout=None,
             metadata=None):
        return grpc.experimental.unary_stream(request, target, '/DominionServer/Join',
                                              dominion__pb2.PlayerInfo.SerializeToString,
                                              dominion__pb2.Message.FromString,
                                              options, channel_credentials,
                                              call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Start(request,
              target,
              options=(),
              channel_credentials=None,
              call_credentials=None,
              compression=None,
              wait_for_ready=None,
              timeout=None,
              metadata=None):
        return grpc.experimental.unary_unary(request, target, '/DominionServer/Start',
                                             dominion__pb2.PlayerInfo.SerializeToString,
                                             dominion__pb2.Response.FromString,
                                             options, channel_credentials,
                                             call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def PlayCard(request,
                 target,
                 options=(),
                 channel_credentials=None,
                 call_credentials=None,
                 compression=None,
                 wait_for_ready=None,
                 timeout=None,
                 metadata=None):
        return grpc.experimental.unary_unary(request, target, '/DominionServer/PlayCard',
                                             dominion__pb2.Card.SerializeToString,
                                             dominion__pb2.Response.FromString,
                                             options, channel_credentials,
                                             call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Buy(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/DominionServer/Buy',
                                             dominion__pb2.Card.SerializeToString,
                                             dominion__pb2.Response.FromString,
                                             options, channel_credentials,
                                             call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Done(request,
             target,
             options=(),
             channel_credentials=None,
             call_credentials=None,
             compression=None,
             wait_for_ready=None,
             timeout=None,
             metadata=None):
        return grpc.experimental.unary_unary(request, target, '/DominionServer/Done',
                                             dominion__pb2.PlayerInfo.SerializeToString,
                                             dominion__pb2.Response.FromString,
                                             options, channel_credentials,
                                             call_credentials, compression, wait_for_ready, timeout, metadata)
