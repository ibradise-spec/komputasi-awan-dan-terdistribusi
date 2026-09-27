````markdown
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
        Broker -->|Consume Event| CourierService["Modul Notifikasi & Penugasan Kurir"]
    end
```
````

````markdown
```mermaid
graph LR
    Client["Client App (Mobile/Web)"] -->|Sync HTTPS| GW["API Gateway (Reverse Proxy/Auth)"]
    
    subgraph SOA_Core ["SOA Core Services (Synchronous)"]
        GW -->|Sync GET| RestoCatalog["Katalog Resto (SOA Service)"]
        GW -->|Sync POST| OrderService["Modul Pesanan (Core SOA Service)"]
        OrderService -->|Sync Call + Timeout| PaymentService["Modul Pembayaran (SOA + Event Pub)"]
    end
    
    subgraph Event_Brokering ["Pub-Sub Messaging Layer (Asynchronous)"]
        Broker[("Message Broker (RabbitMQ / Kafka)")]
        RestoNotif["Modul Resto (Subscriber Notif)"]
        CourierService["Kurir / Notifikasi (Subscriber Dispatch)"]
    end

    PaymentService -.->|Publish: OrderPaid| Broker
    Broker -.->|Async Push| RestoNotif
    Broker -.->|Async Push| CourierService
````
