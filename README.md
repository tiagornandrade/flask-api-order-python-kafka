# tcc-api-order-python-kafka

This project is being developed for my final paper. The basic idea is to create a microservice api using Kafka as a messenger.

It is being built in:
- Flask
- Kafka-Python

## Architecture

```mermaid
flowchart LR

subgraph Publish
    create_item
end

subgraph Broker/Topic
    order_details
end

subgraph Subscriber1
    order_created
end

subgraph Subscriber2
    order_deleted
end

subgraph Subscriber3
    transaction_created
end

create_item --> Broker/Topic
Broker/Topic --> Subscriber1
Broker/Topic --> Subscriber2
Broker/Topic --> Subscriber3
```

## Schemas
```mermaid
erDiagram

order_created {
    TEXT id
	TEXT name
    TEXT description
    FLOAT price
}

order_deleted {
    TEXT id
    TEXT id_created
	TEXT name
    TEXT description
    FLOAT price
}

transaction_created {
    TEXT trsansaction_id
	JSON trsansaction
}
```


## Script
```sql
CREATE table if not EXISTS order_created (
	id TEXT,
	name TEXT,
    description TEXT,
    price FLOAT
);

CREATE table if not EXISTS order_deleted (
	id TEXT,
	id_created TEXT,
	name TEXT,
    description TEXT,
    price FLOAT
);

CREATE table if not EXISTS transaction_created (
	trsansaction_id TEXT,
	transaction json
);
```