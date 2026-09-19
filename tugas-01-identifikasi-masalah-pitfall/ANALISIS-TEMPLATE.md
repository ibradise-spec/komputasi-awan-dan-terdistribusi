# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** JIM

| Nama | NIM | Kontribusi |
|---|---|---|
| Misael Arafian Fonataba | 103072400017 | 1, 2 |
| Julio Chrysanto Tanlain | 103072400110 | 3 |
| Ibrahimovich Paradise | 103072400122 | 4 |

## Pitfall 1: menganggap latency jaringan selalu rendah atau Latency is zero — ditulis oleh Misael Arafian Fonataba

**Bukti di skenario:** Aplikasi jadi sangat lambat, beberapa permintaan timeout.

**Kenapa ini keliru:** 
FoodGo menganggap ketika suatu server mengirim permintaan ke server atau service lainnya, respon nya akan datang dengan cepat. Padahal di dalam sistem distribusi komunikasi antar server pasti membutuhkan waktu untuk melewati berbagai perangkat jaringan  apalagi disaat server lagi sibuk. Latency tidak mungkin 0 sekecil apapun itu, jadi tidak bisa menganggap komunikasi akan terjadi secara instan.

**Dampak ke FoodGo:** 
Contoh saat promo besar, jumlah request akan meningkat sehingga waktu respons service seperti pemesanan dan pembayaran jadi lebih lama. Jika backend nya menunggu respons terlalu lama, banyak request lain nya akan tertahan dan akan membuat aplikasi jadi lambat, request nya akan mengalami timeout dan akan membuat pelanggan yang sedang checkout bingung atau yang paling parah bisa crash.  

**Solusi desain awal:** 
-Menggunakan message queue/asynchronous processing untuk proses yang tidak harus selesai secara langsung.
-Circuit breaker bisa dipakai saat service tertentu terlalu lambat/gagal berkali-kali, request nya akan dihentikan sementara agar tidak membebani service lainnya.

**Trade-off:** 
-Message queue akan membuat lebih tahan terhadap lonjakan traffic tapi akan menambah kompleksitas sistem dan mungkin bisa menyebabkan delay
-Circuit breaker bisa mencegah service yang bermasalah membebani sistem, tapi fitur yang bergantung pada server tersebut bisa sementara tidak dapat digunakan.

---

## Pitfall 2:  — ditulis oleh Misael Arafian Fonataba

**Bukti di skenario:** 
Server backend kadang crash total dan perlu di-restart manual.

**Kenapa ini keliru:** 

**Dampak ke FoodGo:** 

**Solusi desain awal:** [usulan solusi]

**Trade-off:** [apa yang dikorbankan/risiko dari solusi ini]

---

## Pitfall 3: Asumsi “The Network Is Reliable” dan Tidak Adanya Timeout — ditulis oleh Julio Chrysanto Tanlain

**Bukti di skenario:** Tim menemukan asumsi dalam kode berupa `# network is always reliable`, no need for retry. Selain itu, tidak ada timeout pada pemanggilan antarservice, sehingga modul pesanan menunggu respons modul pembayaran tanpa batas waktu.

**Kenapa ini keliru:** Asumsi “network is always reliable” keliru karena mengabaikan kemungkinan koneksi terputus, respons terlambat, atau respons tidak diterima. Anggapan “no need for retry” juga mengabaikan kemungkinan bahwa permintaan yang terganggu sementara dapat berhasil jika dicoba kembali setelah gangguan pulih, meskipun retry perlu dibatasi dan hanya dilakukan jika aman. Selain itu, tidak adanya timeout membuat modul pesanan bergantung pada respons modul pembayaran yang belum tentu datang. Akibatnya, modul pesanan bisa terus menunggu dan menahan resource yang dibutuhkan untuk menangani pesanan lain.

**Dampak ke FoodGo:** Request yang terus menunggu dapat menahan koneksi, memori, atau slot worker. Saat pesanan melonjak, kapasitas untuk melayani request baru berkurang, antrean bertambah, dan aplikasi melambat atau gagal melayani pengguna. Gangguan pada pembayaran akhirnya bisa ikut menghambat layanan pesanan. Status pesanan juga dapat tetap menunggu meskipun pembayaran sudah berhasil, apabila respons konfirmasinya belum diterima.

**Solusi desain awal:** 
**1. Memberikan timeout pada pemanggilan antarservice:**
Timeout memberikan batas waktu bagi modul pesanan untuk menunggu respons modul pembayaran. Kalau batas waktunya terlewati, modul pesanan berhenti menunggu dan melepaskan resource yang sudah tidak diperlukan. Pengguna diberi tahu bahwa hasil pembayaran belum diketahui. Sistem kemudian memeriksa hasilnya di latar belakang dengan identitas transaksi yang sama.

**2. Menambahkan retry terbatas dengan backoff:**
Retry digunakan untuk mencoba kembali permintaan yang mengalami gangguan sementara, seperti koneksi terputus atau layanan sementara tidak tersedia. Jumlah percobaan dan total waktu penanganannya dibatasi. Setiap percobaan tetap menggunakan timeout dan diberi jeda yang bisa diperpanjang agar layanan punya kesempatan pulih. Kalau batas percobaan sudah tercapai, sistem menghentikan retry.

**3. Circuit breaker, untuk kegagalan yang berulang:**
Mekanisme ini memantau kegagalan. Ketika ambang tertentu tercapai, panggilan ke layanan tersebut dihentikan sementara

**Trade-off:** 
* **Timeout terlalu singkat:** sistem berhenti menunggu sebelum respons diterima, padahal prosesnya masih berpotensi berhasil.
* **Timeout terlalu panjang:** resource tertahan lebih lama sehingga permintaan lain bisa ikut menunggu.
* **Retry menambah request dan waktu tunggu:** percobaan tambahan bisa membantu saat gangguan sementara, tetapi juga dapat memperparah beban kalau layanan sudah kewalahan.
* **circuit breaker memperlambat layanan yang sudah pulih terlambat digunakan kembali:** Circuit breaker berisiko menolak request terlalu cepat atau tetap membatasi akses saat layanan sudah pulih. Pengaturan ambangnya juga menambah kerumitan.

---

## Pitfall 4: Single Point of Failure (SPoF) & Ketiadaan Isolasi Sumber Daya (Bulkhead) pada Monolitik — ditulis oleh Ibrahimovich Paradise

**Bukti di skenario:**  
Saat trafik naik, satu server yang menangani semua modul (pesanan, pembayaran, notifikasi kurir) kewalahan karena semuanya berjalan di satu proses monolitik yang sama yang berujung pada Server backend kadang crash total dan perlu di-restart manual.

**Kenapa ini keliru:**  
Desain arsitektur FoodGo menyatukan seluruh domain bisnis ke dalam satu proses tunggal (shared runtime) tanpa isolasi sumber daya (failure domain isolation atau bulkhead pattern). Mengasumsikan satu proses server dapat menyerap beban heterogen secara seragam adalah kekeliruan. Modul pesanan yang butuh latensi rendah harus berbagi CPU, thread pool, dan memory dengan modul pembayaran dan notifikasi yang bergantung pada I/O jaringan eksternal.

**Dampak ke FoodGo:**  
Ketika modul pembayaran atau notifikasi mengalami keterlambatan eksternal, thread eksekusi tertahan (thread starvation). Karena pool thread digunakan bersama, modul pesanan yang kodenya sehat tidak lagi mendapat jatah komputasi. Antrean request yang menumpuk tak terkelola memicu lonjakan memori hingga OS melakukan terminasi paksa (Out-Of-Memory kill). Ketiadaan redundansi (Single Point of Failure) dan mekanisme self-healing/health-check membuat satu kegagalan modul melumpuhkan seluruh platform FoodGo secara total dan menuntut restart manual.

**Solusi desain awal:**  
1. **Penerapan Redundansi Horizontal (Short-term):** Menjalankan beberapa instance backend monolitik secara bersamaan di balik Load Balancer + horizontal scaling untuk mengeliminasi SPoF.
2. **Asynchronous Decoupling via Message Queue:** Mengisolasi modul notifikasi dan proses downstream pembayaran ke antrean pesan (event-driven worker), sehingga modul pesanan tidak menunggu proses I/O selesai.
3. **Pemisahan Modul Bertahap (*Modular Monolith to Microservices*):** Memisahkan modul pembayaran dan notifikasi menjadi service terpisah dengan alokasi resource komputasi mandiri.

**Trade-off:**  
Pemisahan arsitektur dan desentralisasi proses membawa biaya operasional (operational overhead) yang signifikan:
- **Kembalinya Fallacies Jaringan:** Komunikasi antar modul yang awalnya in-memory berubah menjadi network calls, yang menimbulkan latensi tambahan dan overhead serialisasi (transport cost).
- **Integritas Data & Kompleksitas:** Hilangnya transaksi atomik basis data (single ACID transaction) memaksa tim mengelola eventual consistency atau Saga Pattern, yang jauh lebih rawan bug logika dan menuntut distributed tracing untuk debugging.

---

## Kesimpulan Kelompok

[Ringkasan: jika FoodGo memperbaiki ketiga pitfall ini, apa arsitektur yang disarankan secara garis besar? Kaitkan dengan Tugas 2.]
