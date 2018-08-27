from kafka.serializer import Serializer, Deserializer
import json
import avro.schema
import io,os
from avro.io import DatumWriter

schema_path = os.path.dirname(os.path.realpath(__file__))+"//contract.avsc"
schema = avro.schema.Parse(open(schema_path).read())

class contract_serializer(Serializer):
    def serialize(self, topic, value):
        
        writer = avro.io.DatumWriter(schema)
        bytes_write = io.BytesIO() 
        encoder = avro.io.BinaryEncoder(bytes_write)
        writer.write(value,encoder)
        return bytes_write.getvalue()

class contract_deserializer(Deserializer):
    def deserialize(self, topic, bytes_):
        bytes_reader = io.BytesIO(bytes_)
        decoder = avro.io.BinaryDecoder(bytes_reader)
        reader = avro.io.DatumReader(schema)
        return reader.read(decoder)