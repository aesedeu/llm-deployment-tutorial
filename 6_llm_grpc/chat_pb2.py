# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: chat.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'chat.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nchat.proto\x12\x04\x63hat\"/\n\nUserPrompt\x12\x0c\n\x04text\x18\x01 \x01(\t\x12\x13\n\x0btemperature\x18\x02 \x01(\x02\"\x1f\n\x0eGeneratedToken\x12\r\n\x05token\x18\x01 \x01(\t2D\n\nGPTService\x12\x36\n\x08Generate\x12\x10.chat.UserPrompt\x1a\x14.chat.GeneratedToken(\x01\x30\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chat_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_USERPROMPT']._serialized_start=20
  _globals['_USERPROMPT']._serialized_end=67
  _globals['_GENERATEDTOKEN']._serialized_start=69
  _globals['_GENERATEDTOKEN']._serialized_end=100
  _globals['_GPTSERVICE']._serialized_start=102
  _globals['_GPTSERVICE']._serialized_end=170
# @@protoc_insertion_point(module_scope)
