# tcc-api-order-python-kafka

This project is being developed for my final paper. The basic idea is to create a microservice api using Kafka as a messenger.

It is being built in:
- Flask
- Kafka-Python

## Architecture

```mermaid
flowchart LR

subgraph Publish1
    1[producer_order]
end

subgraph Broker/Topic
    a[create_order_topic]
    b[delete_order_topic]
    c[update_order_topic]
end

subgraph Subscriber1
    order
end

subgraph Subscriber2
    transaction
end

1 --> a
1 --> b
1 --> c
a --> Subscriber1
a --> Subscriber2
b --> Subscriber1
b --> Subscriber2
c --> Subscriber1
c --> Subscriber2
```

## Schemas
```mermaid
erDiagram

order {
    TEXT user_id
    TEXT event_key
	TEXT product_name
    TEXT description
    FLOAT price
    TIMESTAMP event_timestamp
    TEXT operation
}

transaction {
    TEXT trsansaction_id
	JSON trsansaction
}
```
