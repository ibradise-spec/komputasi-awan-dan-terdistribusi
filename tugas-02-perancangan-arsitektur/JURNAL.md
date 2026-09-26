Jurnal Proses — Tugas 2

[Tanggal]

Opsi arsitektur yang dipertimbangkan: kombinasi Service-Oriented Architecture (SOA) dan Publish-Subscribe (Pub-Sub

Kenapa akhirnya pilih [SOA/Pub-Sub]: Kami memilih kombinasi Service-Oriented Architecture (SOA) dan Publish-Subscribe (Pub-Sub). SOA digunakan untuk memisahkan sistem menjadi beberapa service berdasarkan fungsi, seperti modul pesanan (Order Service), modul pembayaran (Payment Service), modul katalog restoran, serta modul kurir dan notifikasi. Sementara itu, Pub-Sub digunakan untuk komunikasi asynchronous pada proses yang tidak harus menunggu respons secara langsung.

Pemilihan kombinasi ini didasarkan pada masalah pada sistem FoodGo sebelumnya yang masih berbentuk monolitik. Semua modul berjalan dalam satu aplikasi sehingga ketika salah satu bagian mengalami beban tinggi atau gangguan, bagian lain dapat ikut terdampak. Pada Tugas 1, masalah tersebut berkaitan dengan Single Point of Failure, tidak adanya isolasi sumber daya, serta kemungkinan terjadinya cascading failure.

Dengan SOA, setiap modul dapat dikembangkan dan dijalankan secara lebih mandiri sehingga ketergantungan antar-modul dapat dikurangi. Kemudian, Pub-Sub digunakan untuk proses asynchronous, misalnya setelah pembayaran berhasil, event dapat dikirim melalui Message Broker dan diterima oleh modul notifikasi restoran serta modul kurir secara independen. Hal ini membuat komunikasi antar-service menjadi lebih loosely coupled.

Kombinasi ini juga memiliki trade-off, yaitu sistem menjadi lebih kompleks karena membutuhkan beberapa service dan Message Broker. Selain itu, proses debugging menjadi lebih sulit karena alur asynchronous tidak selalu berjalan secara linear. Namun, pendekatan ini sesuai dengan permasalahan FoodGo karena dapat membantu mengurangi ketergantungan antar-modul dan membatasi dampak kegagalan satu bagian terhadap sistem secara keseluruhan

Revisi diagram (versi 1 → versi 2, apa yang berubah dan kenapa): ...

Log Penggunaan AI (Level 2)

Wajib diisi sesuai kebijakan Level 2 di ../RUBRIK-UMUM.md. Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

Tanggal

Tool AI

Prompt yang diberikan

Ringkasan saran/ide AI

Bagaimana diolah jadi tulisan/kode sendiri

26/09/2026

Chatgpt

hei gpt pada studi kasus di bawah ini kan sebelumnya kelompokku sudah pernah membahas dan hasil yang kita pakai adalah hybrid antara  Service-Oriented Architecture (SOA) atau Publish-Subscribe.  , tapi kenapa sih harus hybrid? kasih aku kelebihan dan kekurangan(trade off) kalau cuman pake SOA saja , publish-subscribe saja, dan hybrid keduanya? dan menurutmu mana yang di rekomendasi dalam studi kasus ini, kasih alasannya yang konkrit, dan aku mau harus objektif dan tidak bias

 Tugas 1: FoodGo butuh sistem yang decoupled agar tim kurir dan tim resto tidak saling mengganggu ketika salah satu modul diperbarui/deploy ulang. Saat ini semua modul (pesanan, pembayaran, notifikasi kurir, katalog resto) berjalan sebagai satu aplikasi monolitik — sekali deploy, semua modul ikut restart dan berisiko downtime total. | Iya, kalau kita benar-benar objektif, pertanyaannya bukan “hybrid pasti lebih bagus karena menggabungkan dua hal”, tetapi bagian mana dari masalah FoodGo yang cocok diselesaikan oleh SOA, bagian mana yang cocok oleh Pub-Sub, dan apakah ada alasan nyata untuk memakai keduanya sekaligus.

Ada satu koreksi konsep yang penting dari pembahasan kita sebelumnya: SOA dan Pub-Sub sebenarnya bukan dua pilihan yang sepenuhnya berada pada level yang sama. SOA mengatur bagaimana sistem dibagi menjadi service, sedangkan Pub-Sub mengatur bagaimana komponen berkomunikasi. Karena itu, sebuah SOA bisa saja memakai Pub-Sub. Dalam praktik, pola komunikasi hybrid juga memang digunakan ketika sebagian alur membutuhkan komunikasi sinkron dan sebagian lainnya cocok asynchronous. (Microsoft Learn)

Untuk studi kasus FoodGo, perbandingannya kira-kira seperti ini.

Aspek

SOA saja

Pub-Sub saja

Hybrid SOA + Pub-Sub

Pemisahan modul

Sangat cocok

Bisa, tetapi bukan fokus utamanya

Sangat cocok

Request yang butuh respons langsung

Cocok

Kurang cocok

Cocok

Notifikasi/broadcast ke banyak pihak

Bisa, tetapi perlu direct call ke consumer

Sangat cocok

Sangat cocok

Loose coupling

Cukup, tetapi direct call masih membuat dependency

Sangat tinggi

Tinggi

Deployment independen

Bisa dicapai melalui pemisahan service

Bisa pada consumer/producer yang terpisah

Bisa

Debugging

Relatif lebih mudah

Lebih sulit

Sedang–sulit

Konsistensi data

Lebih mudah dikontrol

Lebih mudah terjadi eventual consistency

Bisa dipilih sesuai kebutuhan

Kompleksitas

Sedang

Tinggi

Tinggi

Kesesuaian dengan FoodGo

Cukup

Kurang jika dipakai untuk semua komunikasi

Paling sesuai dengan pola kebutuhan kasus

1. Kalau FoodGo hanya menggunakan SOA

Bayangkan:

Client
   ↓
Order Service
   ↓
Payment Service
   ↓
Courier Service
   ↓
Notification Service

Masing-masing sudah menjadi service terpisah. Jadi masalah monolitik memang sudah jauh berkurang.

Kelebihan

Pertama, pemisahan tanggung jawab jelas. Order, Payment, Catalog, dan Courier bisa dikembangkan dan di-deploy secara terpisah.

Kedua, komunikasi request-response cocok untuk proses yang memang membutuhkan hasil langsung. Misalnya Order Service meminta Payment Service memproses pembayaran dan membutuhkan hasil berhasil/gagal sebelum melanjutkan.

Ketiga, debugging relatif lebih mudah. Alurnya masih cukup linear:

Order → Payment → Response

dan tidak ada broker/event chain yang harus ditelusuri.

Kekurangan / trade-off

Masalah utamanya adalah dependency antar-service masih cukup kuat kalau komunikasi dilakukan secara direct synchronous call.

Contohnya:

Order Service
     ↓
Payment Service

Kalau Payment lambat, Order ikut menunggu. Ini persis berkaitan dengan masalah Tugas 1 tentang tidak adanya timeout dan asumsi bahwa network selalu reliable. Request yang terus menunggu dapat menahan resource dan memperburuk kondisi saat traffic tinggi.

Masalah lain muncul ketika satu event harus dikirim ke banyak komponen:

Payment
  ├──→ Resto
  ├──→ Courier
  └──→ Notification

Payment harus mengetahui siapa saja yang perlu dipanggil. Kalau nanti ada consumer baru, misalnya Analytics, Payment Service harus berpotensi diubah lagi. Ini berarti coupling masih ada.

Jadi SOA saja bisa menyelesaikan masalah monolitik, tetapi belum menghilangkan semua coupling komunikasi.

2. Kalau FoodGo hanya menggunakan Pub-Sub

Sekarang kita balik:

Order → Broker
          ├── Payment
          ├── Resto
          └── Courier

Semua komunikasi sebisa mungkin dibuat event-driven.

Kelebihan

Ini sangat kuat untuk decoupling.

Publisher tidak perlu tahu siapa subscribernya. Consumer baru bisa ditambahkan tanpa harus mengubah publisher. Itu memang merupakan salah satu tujuan utama Pub-Sub. (Dokumen AWS)

Contohnya:

OrderPaid
   ↓
Broker
 ├── Resto
 ├── Courier
 ├── Notification
 └── Analytics

Order atau Payment tidak perlu melakukan direct call satu per satu.

Pub-Sub juga cocok untuk kasus FoodGo yang memiliki broadcasting event dan proses yang dapat berjalan asynchronous. Microsoft dan AWS sama-sama menjelaskan bahwa pola ini cocok ketika satu event perlu diproses oleh banyak consumer dan producer tidak perlu mengetahui consumer secara langsung. (Microsoft Learn)

Kekurangan / trade-off

Masalahnya adalah tidak semua proses FoodGo cocok dijadikan event asynchronous.

Contoh paling jelas:

Customer:
"Apakah makanan ini tersedia?"


Customer mengharapkan jawaban.

Sulit membayangkan:

Client
  ↓
Publish "CheckMenu"
  ↓
Broker
  ↓
Catalog
  ↓
event response

hanya untuk mendapatkan informasi menu. Bisa dibuat, tetapi kompleksitasnya tidak sebanding dengan kebutuhannya.

Microsoft juga mencatat bahwa event-driven/Pub-Sub kurang cocok untuk workflow sederhana yang memang membutuhkan request-response langsung, atau ketika strong consistency diperlukan. (Microsoft Learn)

Selain itu, Pub-Sub membawa trade-off:

eventual consistency;

kemungkinan masalah ordering;

error handling lebih rumit;

debugging lebih sulit;

perlu menangani delivery/retry/idempotency;

tracing satu transaksi menjadi lebih sulit karena tidak lagi berupa satu call chain. (Microsoft Learn)

Jadi kalau semua dipaksa menjadi Pub-Sub, FoodGo justru bisa over-engineered.

3. Kalau menggunakan Hybrid SOA + Pub-Sub

Nah, di sini mulai terlihat alasan teknis kenapa kelompok kalian memilih hybrid.

Bukan karena:

“SOA bagus + Pub-Sub bagus = pasti lebih bagus.”

Tetapi karena FoodGo memiliki dua jenis kebutuhan komunikasi yang berbeda.

Kebutuhan pertama: perlu jawaban langsung

Contohnya:

Client
  ↓
Order Service
  ↓
Payment Service
  ↑
hasil pembayaran

Ini cocok menggunakan request-response.

Kebutuhan kedua: event harus diteruskan ke beberapa pihak

Setelah pembayaran sukses:

Payment
    ↓
PaymentSucceeded
    ↓
Broker
   ├──→ Restaurant Notification
   └──→ Courier Service

Ini cocok menggunakan Pub-Sub.

Jadi arsitekturnya tidak memaksakan satu pola komunikasi untuk semua masalah.

4. Kenapa ini relevan banget dengan studi kasus FoodGo?

Lihat requirement-nya:

FoodGo butuh sistem yang decoupled agar tim kurir dan tim resto tidak saling mengganggu ketika salah satu modul diperbarui/deploy ulang.

Ada dua kebutuhan di kalimat itu.

Kebutuhan A — Service harus independen

Ini dijawab oleh SOA:

Order Service
Payment Service
Catalog Service
Courier Service

Service dipisahkan berdasarkan tanggung jawab sehingga tidak lagi satu aplikasi monolitik.

Kebutuhan B — Service tidak terlalu bergantung satu sama lain

Ini dibantu oleh Pub-Sub:

Payment
   ↓
Broker
   ├── Resto
   └── Courier

Payment tidak perlu memiliki direct dependency ke Resto dan Courier.

Inilah alasan hybrid punya dasar yang konkret.

5. Tapi ada satu hal yang harus diluruskan

Pub-Sub bukan penyebab utama deployment independence.

Deployment independence terutama datang dari:

Monolith
   ↓
separate services

yaitu pemisahan service.

Pub-Sub kemudian membantu mengurangi coupling antar-service, terutama pada komunikasi asynchronous.

Jadi jangan menulis:

“Karena menggunakan Pub-Sub, service bisa di-deploy independen.”

Itu terlalu menyederhanakan.

Lebih tepat:

SOA memisahkan modul menjadi service yang dapat dikembangkan dan dideploy secara lebih independen, sedangkan Pub-Sub mengurangi ketergantungan langsung antar-service pada proses asynchronous.

6. Jadi mana yang paling sesuai?

Untuk studi kasus FoodGo yang diberikan, secara objektif aku akan memilih Hybrid SOA + Pub-Sub.

Bukan karena hybrid selalu paling baik, tetapi karena kebutuhan FoodGo memang campuran.

Contohnya:

                     FOODGO
                        │
            ┌───────────┴───────────┐
            │                       │
     Direct interaction        Event interaction
            │                       │
            ▼                       ▼
       SOA Services              Pub-Sub
            │                       │
     Order ↔ Payment          Payment → Broker
     Client → Catalog            ↙         ↘
                              Resto       Courier

SOA menangani bagian yang sifatnya langsung dan membutuhkan respons, sedangkan Pub-Sub menangani bagian yang sifatnya event/broadcast dan tidak perlu memblokir proses utama.

Itu juga sejalan dengan Tugas 1 kalian: sebelumnya kalian menemukan latency, network reliability, SPoF, resource isolation, dan cascading failure sebagai masalah, lalu mengusulkan pemisahan modul serta asynchronous message queue untuk proses yang tidak harus selesai langsung.

Tetapi bukan berarti hybrid tanpa kelemahan

Justru kelemahannya adalah kompleksitas paling tinggi dibanding dua pilihan lainnya.

Kalian harus mengurus:

Service
+ API
+ Message Broker
+ Event
+ Retry
+ Error Handling
+ Monitoring
+ Distributed Tracing

dan asynchronous processing membawa eventual consistency serta debugging yang lebih sulit. (Microsoft Learn)

Jadi secara objektif:

SOA saja: lebih sederhana, tetapi coupling antar-service masih lebih kuat.

Pub-Sub saja: decoupling sangat kuat, tetapi terlalu asynchronous untuk semua kebutuhan FoodGo dan membuat workflow sederhana menjadi lebih kompleks.

Hybrid: paling kompleks, tetapi paling sesuai karena FoodGo memang membutuhkan dua pola komunikasi yang berbeda.

Jadi alasan rekomendasinya bukan “hybrid punya kelebihan paling banyak”, melainkan “hybrid paling cocok dengan karakter komunikasi yang berbeda dalam sistem FoodGo.”

| ... |
| 26/09/2026 | Chatgpt | okeh secara singkat SOA itu membagi layanan menjadi service service gitu kan trus pub sub seperti kita memakai broker jadi dia yang mengurus ini tuh harus ngapain ini harus ngapain? | Iya, kurang lebih begitu, tapi ada sedikit pelurusan biar konsepnya tepat:

SOA → membagi sistem besar menjadi beberapa service berdasarkan tanggung jawabnya.
Contoh: Order Service, Payment Service, Catalog Service, Courier Service.

Pub-Sub → mengatur bagaimana service berkomunikasi lewat event. Service yang menghasilkan informasi publish event ke broker, lalu broker meneruskan event itu ke service yang subscribe dan memang membutuhkan informasi tersebut.

Contoh FoodGo:

Payment Service
      │
      │ publish: PaymentSucceeded
      ▼
 Message Broker
      │
      ├────► Resto Notification
      │
      └────► Courier Service

Jadi broker bukan benar-benar “menentukan sendiri ini harus ngapain”. Yang menentukan aksi tetap masing-masing service.

Lebih tepatnya:

Service menghasilkan atau membutuhkan event → broker mengantarkan event tersebut ke subscriber yang sesuai → subscriber memproses event sesuai tugasnya.

Gampangnya:

SOA = “siapa yang mengerjakan apa”
Pub-Sub = “bagaimana informasi/event dikirim ke yang membutuhkan”
| kami memilih kombinasi Service-Oriented Architecture (SOA) dan Publish-Subscribe (Pub-Sub). SOA digunakan untuk memisahkan sistem menjadi beberapa service berdasarkan fungsi, seperti modul pesanan (Order Service), modul pembayaran (Payment Service), modul katalog restoran, serta modul kurir dan notifikasi. Sementara itu, Pub-Sub digunakan untuk komunikasi asynchronous pada proses yang tidak harus menunggu respons secara langsung.

Pemilihan kombinasi ini didasarkan pada masalah pada sistem FoodGo sebelumnya yang masih berbentuk monolitik. Semua modul berjalan dalam satu aplikasi sehingga ketika salah satu bagian mengalami beban tinggi atau gangguan, bagian lain dapat ikut terdampak. Pada Tugas 1, masalah tersebut berkaitan dengan Single Point of Failure, tidak adanya isolasi sumber daya, serta kemungkinan terjadinya cascading failure.

Dengan SOA, setiap modul dapat dikembangkan dan dijalankan secara lebih mandiri sehingga ketergantungan antar-modul dapat dikurangi. Kemudian, Pub-Sub digunakan untuk proses asynchronous, misalnya setelah pembayaran berhasil, event dapat dikirim melalui Message Broker dan diterima oleh modul notifikasi restoran serta modul notifikasi dan penugasan kurir secara independen. Hal ini membuat komunikasi antar service menjadi lebih tidak saling ketergantungan.

Kombinasi ini juga memiliki trade-off, yaitu sistem menjadi lebih kompleks karena membutuhkan beberapa service dan Message Broker. Selain itu, proses debugging menjadi lebih sulit karena alur asynchronous tidak selalu berjalan secara linear. Namun, pendekatan ini sesuai dengan permasalahan FoodGo karena dapat membantu mengurangi ketergantungan antar-modul dan membatasi dampak kegagalan satu bagian terhadap sistem secara keseluruhan. |

| 26/09/2026 | Chatgpt | ini adalah graph sederhana yang sudah di buat temanku dari apa yang sudah kita bahas dari tadi, memang masih belum spesifik tapi kita akan pakai ini, di sini kan pertama tama sudah nih client kirim request trus gateaway  mengirimkan query catalog ke modil katalog resto dan di tunjukan ke client, trus kalau pesan maka akan masuk ke modul pesanan, trus di verivikasi modul pembayaran, setelahpembayaran berhasil maka akan di publis event paid event di mana kita pake broker rabbitMQ/kafka, nanti broker ini akan mengirimkan ke subcribe nya yaity modul notifkasi resto, trus modul notifakasi dan penugasan kurir, apakah ada yang salah dari penjelasanku????

graph LR
Client["Client App (Mobile/Web)"] -->|HTTPS Request| GW["API Gateway / Reverse Proxy"]

subgraph SOA_Core ["SOA Core Services (Synchronous / Request-Response)"]
    GW -->|Query Menu| RestoCatalog["Modul Katalog Resto"]
    GW -->|Buat Pesanan| OrderService["Modul Pesanan"]
    OrderService -->|Verifikasi Pembayaran <br/> | PaymentService["Modul Pembayaran"]
end

subgraph Event_Brokering ["Pub-Sub Messaging Layer (Asynchronous / Decoupled)"]
    PaymentService -->|Publish: OrderPaid Event| Broker["Message Broker <br/> (RabbitMQ / Kafka)"]
    
    Broker -->|Consume Event| RestoNotif["Modul Notifikasi Resto"]
    Broker -->|Consume Event| CourierService["Modul Notifikasi & Penugasan Kurir"]
end

|Penjelasanmu secara keseluruhan sudah benar dan sudah sesuai dengan logika graph yang kalian buat. Ada beberapa bagian yang perlu diperjelas sedikit supaya saat presentasi tidak menimbulkan salah pengertian.

Alur yang kamu jelaskan

Client
  ↓
API Gateway
  ↓
Resto Catalog
  ↓
Client menerima data katalog

Client membuat pesanan
  ↓
API Gateway
  ↓
Order Service
  ↓
Payment Service
  ↓
Pembayaran berhasil
  ↓
Publish event
  ↓
RabbitMQ / Kafka
  ↓             ↓
Resto Notif    Courier/Notif

Itu sudah nyambung.

Yang perlu diluruskan

1. Gateway bukan yang “menampilkan” katalog ke client.

Lebih tepat:

Client mengirim request ke API Gateway, lalu Gateway meneruskan request ke Modul Katalog Resto. Modul Katalog memberikan response kembali melalui Gateway ke Client.

Jadi:

Client → Gateway → Catalog
Client ← Gateway ← Catalog

2. “Order diverifikasi oleh Payment” sedikit kurang spesifik.

Di graph kalian tertulis:

OrderService
    ↓
Verifikasi Pembayaran
    ↓
PaymentService

Secara sederhana masih bisa diterima. Tetapi saat menjelaskan, lebih aman bilang:

Order Service mengirim request ke Payment Service untuk memproses atau memverifikasi pembayaran.

Jangan sampai terdengar seolah-olah Payment Service yang memverifikasi seluruh order.

3. Setelah pembayaran berhasil, Payment Service publish event — ini valid.

Jadi alurnya:

Payment Service
      ↓
Publish: OrderPaid Event
      ↓
Message Broker

Kemudian broker meneruskan event ke subscriber:

Broker
  ├──→ Modul Notifikasi Resto
  └──→ Modul Notifikasi & Penugasan Kurir

Ini memang inti Pub-Sub.

Yang penting, broker bukan yang menentukan bisnisnya harus ngapain. Broker hanya meneruskan event kepada subscriber. Kemudian:

Resto Notification
→ memberi notifikasi ke restoran

Courier Service
→ memproses penugasan / notifikasi kurir

Jadi kalau kamu menjelaskan graph ini di depan kelas

Kamu bisa bilang kurang lebih:

“Pertama, client mengirim request melalui API Gateway. Gateway meneruskan request ke modul katalog untuk mengambil informasi menu, kemudian hasilnya dikembalikan ke client. Ketika client membuat pesanan, request diteruskan ke modul pesanan. Selanjutnya modul pesanan berkomunikasi dengan modul pembayaran untuk memproses atau memverifikasi pembayaran. Setelah pembayaran berhasil, Payment Service mem-publish event OrderPaid ke Message Broker seperti RabbitMQ atau Kafka. Broker kemudian meneruskan event tersebut kepada subscriber, yaitu modul notifikasi restoran dan modul notifikasi serta penugasan kurir. Kedua modul tersebut dapat memproses event secara asynchronous dan independen.”

Itu sudah cukup tepat untuk menjelaskan alur graph kalian.

Satu catatan kecil saja: label “SOA Core Services (Synchronous / Request-Response)” sebenarnya sedikit menyederhanakan konsep SOA, karena SOA tidak berarti harus synchronous. Tapi untuk graph tugas kalian, label itu masih bisa dipakai untuk menunjukkan bahwa bagian tersebut menggunakan komunikasi request-response.|Alur dimulai ketika pelanggan mengirim request melalui Client App ke API Gateway menggunakan HTTPS. Gateway kemudian meneruskan request ke Modul Katalog Resto untuk mengambil informasi menu secara sinkron dengan pola request-response, lalu hasilnya dikembalikan ke pelanggan.

Setelah pelanggan memilih menu dan membuat pesanan, request diteruskan oleh Gateway ke Modul Pesanan (Order Service). Modul Pesanan kemudian berkomunikasi dengan Modul Pembayaran (Payment Service) untuk memproses atau memverifikasi pembayaran secara sinkron dengan pola request-response.

Setelah pembayaran berhasil, Payment Service mengirimkan event OrderPaid ke Message Broker seperti RabbitMQ atau Kafka secara asynchronous. Broker kemudian meneruskan event tersebut kepada subscriber, yaitu Modul Notifikasi Resto dan Modul Notifikasi & Penugasan Kurir. Kedua modul tersebut memproses event secara asynchronous untuk memberikan notifikasi kepada restoran dan melakukan proses penugasan atau notifikasi kurir.|
