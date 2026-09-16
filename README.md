# Redis_Clone

- In-memory key-value datastore with `SET`, `GET`, `DELETE`, `EXISTS`
- TTL / key expiration
- RESP protocol encoder/decoder
- Non-blocking TCP server
- I/O multiplexing with Python selectors rather than one thread per connection
- Multiple persistent requests per TCP connection
- Handling partial/buffered network reads
- Large-response / slow-client testing and socket backpressure
- Concurrent connection load testing up to ~40k connections
- AOF persistence
- RDB-style snapshot persistence
- Recovery of persisted state after restart
- VERY slow connection detection , processes that request only after entire request has come in (using buffer, and resp protocol to determine if whole message has come in ), but also services the other clients


Current Limitations - 
Cannot process 2 or 3 or n simultaneous commands together
