# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import recognitionFacial_pb2 as recognitionFacial__pb2


class recognitionFacialStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.uploadTraining = channel.stream_unary(
                '/recognitionFacial/uploadTraining',
                request_serializer=recognitionFacial__pb2.Chunk.SerializeToString,
                response_deserializer=recognitionFacial__pb2.Reply.FromString,
                )
        self.uploadRecognition = channel.stream_unary(
                '/recognitionFacial/uploadRecognition',
                request_serializer=recognitionFacial__pb2.Chunk.SerializeToString,
                response_deserializer=recognitionFacial__pb2.Reply.FromString,
                )


class recognitionFacialServicer(object):
    """Missing associated documentation comment in .proto file."""

    def uploadTraining(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def uploadRecognition(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_recognitionFacialServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'uploadTraining': grpc.stream_unary_rpc_method_handler(
                    servicer.uploadTraining,
                    request_deserializer=recognitionFacial__pb2.Chunk.FromString,
                    response_serializer=recognitionFacial__pb2.Reply.SerializeToString,
            ),
            'uploadRecognition': grpc.stream_unary_rpc_method_handler(
                    servicer.uploadRecognition,
                    request_deserializer=recognitionFacial__pb2.Chunk.FromString,
                    response_serializer=recognitionFacial__pb2.Reply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'recognitionFacial', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class recognitionFacial(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def uploadTraining(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_unary(request_iterator, target, '/recognitionFacial/uploadTraining',
            recognitionFacial__pb2.Chunk.SerializeToString,
            recognitionFacial__pb2.Reply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def uploadRecognition(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_unary(request_iterator, target, '/recognitionFacial/uploadRecognition',
            recognitionFacial__pb2.Chunk.SerializeToString,
            recognitionFacial__pb2.Reply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
