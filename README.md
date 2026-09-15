# Redis_Clone
In-memory key-value datastore with SET, GET, DELETE, EXISTS
TTL / key expiration
RESP protocol encoder/decoder rather than JSON/plain-text messaging
Non-blocking TCP server
I/O multiplexing with Python selectors rather than one thread per connection
Multiple persistent requests per TCP connection
Handling partial/buffered network reads
Large-response / slow-client testing and exploration of socket backpressure
Concurrent connection load testing up to ~40k connections
AOF persistence
RDB-style snapshot persistence
recovery of persisted state after restart
