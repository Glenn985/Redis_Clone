class RespParser:
    def __init__(self, stream):
        self.stream = stream  #  EXPECT STREAM NOT TO ARRIVE AT ONCE 
        
    def parse(self):
        line = self.stream.readline()
        if not line:
            raise EOFError("Connection closed")

        prefix = chr(line[0])
        payload = line[1:].rstrip(b"\r\n").decode()

        dispatch = {
            "+": self._simple_string,
            "-": self._error,
            ":": self._integer,
            "$": self._bulk_string,
            "*": self._array,
        }

        handler = dispatch.get(prefix)
        if not handler:
            raise ValueError(f"Unknown RESP type byte: {prefix!r}")
        return handler(payload)

    def _simple_string(self, data):
        return data

    def _error(self, data):
        # Prefix like "ERR" or "WRONGTYPE" comes before the message
        parts = data.split(" ", 1)
        raise RedisError(parts[1] if len(parts) > 1 else data)

    def _integer(self, data):
        return int(data)

    def _bulk_string(self, data):
        length = int(data)
        if length == -1:
            return None  # null bulk string
        value = self.stream.read(length)
        self.stream.read(2)  # discard trailing \r\n
        return value.decode()

    def _array(self, data):
        count = int(data)
        if count == -1:
            return None  # null array
        return [self.parse() for _ in range(count)]

class RedisError(Exception):
    pass