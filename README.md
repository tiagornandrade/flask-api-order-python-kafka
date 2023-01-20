# tcc-api-order-python-kafka

This project is being developed for my final paper. The basic idea is to create a microservice api using Kafka as a messenger.

It is being built in:
- Flask
- Kafka-Python

# Schemas

```mermaid
erDiagram


checkout_item_cart ||--|{ create_item_cart : contains
create_item_cart {
    string item_id
    string item_name
    string item_description
    string item_price
} 

checkout_item_cart {
    string cart_id
    string item__item_id
    string item__item_name
    string item__item_description
    string item__item_price
} 

```