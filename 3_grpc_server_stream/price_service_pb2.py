# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: price_service.proto
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
    'price_service.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13price_service.proto\x12\rprice_service\"\x1e\n\x0cPriceRequest\x12\x0e\n\x06symbol\x18\x01 \x01(\t\"A\n\rPriceResponse\x12\x0e\n\x06symbol\x18\x01 \x01(\t\x12\r\n\x05price\x18\x02 \x01(\x01\x12\x11\n\ttimestamp\x18\x03 \x01(\t2]\n\x0cPriceService\x12M\n\x0cStreamPrices\x12\x1b.price_service.PriceRequest\x1a\x1c.price_service.PriceResponse\"\x00\x30\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'price_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_PRICEREQUEST']._serialized_start=38
  _globals['_PRICEREQUEST']._serialized_end=68
  _globals['_PRICERESPONSE']._serialized_start=70
  _globals['_PRICERESPONSE']._serialized_end=135
  _globals['_PRICESERVICE']._serialized_start=137
  _globals['_PRICESERVICE']._serialized_end=230
# @@protoc_insertion_point(module_scope)
