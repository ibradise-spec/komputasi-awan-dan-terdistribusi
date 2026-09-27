```mermaid
graph LR
    Client["Client App (Mobile/Web)"] -->|HTTPS Request| GW["API Gateway / Reverse Proxy"]

    subgraph SOA_Core ["SOA Core Services (Synchronous / Request-Response)"]
        GW -->|Query Menu| RestoCatalog["Modul Katalog Resto"]
        GW -->|Buat Pesanan| OrderService["Modul Pesanan"]
        OrderService -->|Verifikasi Pembayaran| PaymentService["Modul Pembayaran"]
    end

    subgraph Event_Brokering ["Pub-Sub Messaging Layer (Asynchronous / Decoupled)"]
        PaymentService -->|Publish: OrderPaid Event| Broker["Message Broker (RabbitMQ / Kafka)"]
        Broker -->|Consume Event| RestoNotif["Modul Notifikasi Resto"]
        Broker -->|Consume Event| CourierService["Modul Notifikasi dan Penugasan Kurir"]
    end
```
