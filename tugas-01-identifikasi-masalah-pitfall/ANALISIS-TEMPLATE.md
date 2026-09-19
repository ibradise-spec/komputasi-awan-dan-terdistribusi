# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** JIM

| Nama | NIM | Kontribusi |
|---|---|---|
| Misael Arafian Fonataba | 103072400017 | 1, 2 |
| Julio Chrysanto Tanlain | 103072400110 | 3 |
| Ibrahimovich Paradise | 103072400122 | 4 |

## Pitfall 1: [nama pitfall] — ditulis oleh [nama]

**Bukti di skenario:** [kutip/paraphrase bagian skenario]

**Kenapa ini keliru:** [penjelasan]

**Dampak ke FoodGo:** [mekanisme kegagalan konkret]

**Solusi desain awal:** [usulan solusi]

**Trade-off:** [apa yang dikorbankan/risiko dari solusi ini]

---

## Pitfall 2: [nama pitfall] — ditulis oleh [nama]

(ulangi struktur di atas)

---

## Pitfall 3: Asumsi “The Network Is Reliable” dan Tidak Adanya Timeout — ditulis oleh Julio Chrysanto Tanlain

**Bukti di skenario:** Tim menemukan asumsi dalam kode berupa `# network is always reliable`, no need for retry. Selain itu, tidak ada timeout pada pemanggilan antarservice, sehingga modul pesanan menunggu respons modul pembayaran tanpa batas waktu.

**Kenapa ini keliru:** Asumsi “network is always reliable” keliru karena mengabaikan kemungkinan koneksi terputus, respons terlambat, atau respons tidak diterima. Anggapan “no need for retry” juga mengabaikan kemungkinan bahwa permintaan yang terganggu sementara dapat berhasil jika dicoba kembali setelah gangguan pulih, meskipun retry perlu dibatasi dan hanya dilakukan jika aman. Selain itu, tidak adanya timeout membuat modul pesanan bergantung pada respons modul pembayaran yang belum tentu datang. Akibatnya, modul pesanan bisa terus menunggu dan menahan resource yang dibutuhkan untuk menangani pesanan lain.

**Dampak ke FoodGo:** 
1. Gangguan jaringan sementara bisa membuat pesanan tertunda atau gagal diproses jika sistem tidak menanganinya
2. Tanpa timeout, pemanggilan yang terus menunggu dapat menahan resource seperti koneksi dan memori. Kalau menggunakan pemanggilan blocking, slot worker atau thread juga bisa tertahan. Jadi, saat pesanan meningkat, resource tersebut belum bisa dipakai untuk memproses pesanan lain. Akibatnya, kapasitas yang tersedia untuk melayani permintaan baru berkurang dan waktu tunggu bisa semakin panjang.
3. Pengalaman pengguna bisa memburuk karena harus menunggu lama tanpa kejelasan apakah pesanan atau pembayarannya sudah berhasil.

**Solusi desain awal:** 
**1. Memberikan timeout pada pemanggilan antarservice.**

Timeout memberikan batas waktu bagi modul pesanan untuk menunggu respons modul pembayaran. Kalau batas waktunya terlewati, modul pesanan berhenti menunggu dan melepaskan resource yang sudah tidak diperlukan.Pengguna diberi tahu bahwa hasil pembayaran belum diketahui. Pembayaran belum bisa dianggap gagal karena layanan pembayaran mungkin masih memprosesnya atau sudah menyelesaikannya. Sistem kemudian memeriksa hasilnya di latar belakang dengan identitas transaksi yang sama, atau menerima notifikasi dari layanan pembayaran jika tersedia. Dengan cara ini, request awal tidak perlu terus menunggu. Hasil pemeriksaan perlu ditampilkan supaya pengguna bisa melihat status terbaru. Pemeriksaan status perlu diberi jeda dan batas percobaan supaya tidak menambah beban secara berlebihan. Sistem juga tidak langsung membuat transaksi pembayaran baru, karena transaksi sebelumnya mungkin sudah berhasil.

**2. Menerapkan rate limiting per pengguna.**

Rate limiting membatasi jumlah request yang dapat dikirim setiap pengguna dalam periode tertentu. Tujuannya membantu mengurangi risiko overload dan membatasi satu pengguna yang mengirim terlalu banyak permintaan. Pembatasan ini diterapkan pada permintaan pembuatan pesanan, sebelum server menjalankan pekerjaan yang lebih berat. Kalau batasnya terlampaui, permintaan tambahan ditolak sementara dan pengguna diberi tahu kapan bisa mencoba lagi. Permintaan untuk memulai pembayaran bisa memiliki batas tersendiri. Pemeriksaan status pembayaran juga perlu dibedakan dari pembuatan pesanan supaya pengguna tetap bisa mengetahui hasil transaksi yang sudah berjalan tanpa melakukan pengecekan berlebihan.Angka batas request belum ditetapkan karena belum ada data pengujian kapasitas. Penentuannya perlu mempertimbangkan penggunaan yang wajar, resource yang dibutuhkan setiap jenis request, dan kapasitas server. Pembatasan per pengguna tetap memiliki keterbatasan. Kalau banyak pengguna mengirim request secara bersamaan, total bebannya masih bisa besar meskipun setiap pengguna belum melewati batas.

**3. Menambahkan retry terbatas dengan backoff.**

Retry digunakan untuk mencoba kembali permintaan yang mengalami gangguan sementara, seperti koneksi terputus atau layanan sementara tidak tersedia. Jumlah percobaan dan total waktu penanganannya dibatasi. Setiap percobaan tetap menggunakan timeout dan diberi jeda yang bisa diperpanjang agar layanan punya kesempatan pulih. Untuk pembayaran, setiap pengulangan menggunakan kunci idempotensi yang sama untuk satu operasi pembayaran. Layanan pembayaran harus mendukung pengenalan kunci tersebut supaya request yang diulang tidak menghasilkan tagihan kedua. Kalau batas percobaan sudah tercapai, sistem menghentikan retry. Jika hasil pembayaran masih belum diketahui, statusnya tetap belum terkonfirmasi sampai ada informasi hasil transaksi yang jelas.


**Trade-off:** 
* **Timeout terlalu singkat:** sistem berhenti menunggu sebelum respons diterima, padahal prosesnya masih berpotensi berhasil.
* **Timeout terlalu panjang:** resource tertahan lebih lama sehingga permintaan lain bisa ikut menunggu.
* **Rate limiting terlalu ketat:** request pengguna yang sah bisa ditolak karena aktivitas wajarnya melewati batas yang ditetapkan terlalu rendah.
* **Pemeriksaan status setelah timeout:** sistem membutuhkan proses tambahan untuk memastikan hasil pembayaran. Pengecekan berkala menambah request, sedangkan penggunaan notifikasi perlu menangani kemungkinan notifikasi terlambat atau dikirim berulang.
* **Retry menambah request dan waktu tunggu:** percobaan tambahan bisa membantu saat gangguan sementara, tetapi juga dapat memperparah beban kalau layanan sudah kewalahan.
* **Idempotensi membutuhkan penanganan tambahan:** sistem perlu menyimpan dan memeriksa identitas operasi agar pengulangan dikenali. Kalau penanganannya tidak benar, retry pembayaran berisiko menghasilkan tagihan ganda.
* **Pemeriksaan status membutuhkan proses tambahan:** pengecekan berkala menambah request, sedangkan penggunaan notifikasi perlu menangani kemungkinan notifikasi terlambat atau dikirim berulang.

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
