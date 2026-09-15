from io import StringIO
class RespParser_decoder:
    def __init__(self, message):
        self.stream = StringIO(message) #use file like funcitons 

    def parse(self):
        # Read ONE RESP header line
        line = self.stream.readline()

        if not line:
            raise EOFError("Connection closed")

        prefix = line[0]
        payload = line[1:].rstrip("\r\n")

        dispatch = {
            "+": self._simple_string,
            "-": self._error,
            ":": self._integer,
            "$": self._bulk_string,
            "*": self._array,
        }

        handler = dispatch.get(prefix)

        if not handler:
            raise ValueError(f"Unknown RESP type: {prefix!r}")

        return handler(payload)

    def _simple_string(self, data):
        return data

    def _error(self, data):
        parts = data.split(" ", 1)
        raise RedisError(parts[1] if len(parts) > 1 else data)

    def _integer(self, data):
        return int(data)

    def _bulk_string(self, data):
        length = int(data)

        if length == -1:
            return None

        # Read exactly `length` characters
        value = self.stream.read(length)

        # Consume the \r\n after the value
        self.stream.read(2)

        return value

    def _array(self, data):
        count = int(data)
        if count == -1:
            return None
        return [self.parse() for _ in range(count)]


class RedisError(Exception):
    pass


# message = '*3\r\n$3\r\nSET\r\n$5\r\nglenn\r\n$4\r\n1231\r\n'

# decoder = RespParser_decoder(message)

# result = decoder.parse()

# print(result)