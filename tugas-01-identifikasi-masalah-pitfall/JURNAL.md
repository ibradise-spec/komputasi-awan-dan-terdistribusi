# Jurnal Proses — Tugas 1

> Isi jurnal ini selama proses diskusi berlangsung, bukan ditulis ulang rapi di akhir. Tulis dengan gaya bebas — poin diskusi, kebuntuan, perubahan pikiran.

## [Tanggal diskusi 1]
- Peserta: Ibrahimovich Paradise, Misael Arafian Fonataba, Julio Chrysanto Tanlain 
- Poin diskusi: Membagi tugas terhadap 4 pitfall yang ada, membahas inti masalah yang ada di permasalahan soal.
- Perbedaan pendapat (jika ada): ...

## [Tanggal diskusi 2]
- ...

## Review Silang
- [Nama] mengomentari analisis [Nama lain]: ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
| --- | --- | --- | --- | --- |
| 19 - 09 - 2026 | Claude | Fallacies of Distributed Computing (referensi: "the network is reliable", "latency is zero", "bandwidth is infinite", "the network is secure", "topology doesn't change", "there is one administrator", "transport cost is zero", "the network is homogeneous") DAN/ATAU masalah desain sistem terdistribusi lain yang relevan (mis. single point of failure karena arsitektur monolitik). Jelaskan ke aku apa saja yang ada di fallacies of distributed computing| Oke bro, ini 8 fallacies of distributed computing (awalnya dirumuskan Peter Deutsch di Sun Microsystems, terus ditambah item ke-8 sama James Gosling). Ini asumsi-asumsi salah yang sering diam-diam dipercaya developer waktu bikin sistem terdistribusi, padahal kenyataannya nggak gitu.

1. The network is reliable
Asumsi jaringan selalu nyambung sempurna. Kenyataannya: paket bisa hilang, koneksi bisa putus kapan aja. Makanya perlu retry logic, timeout, circuit breaker.

2. Latency is zero
Ngirim data antar node dianggep instan. Padahal ada delay fisik (jarak, routing, processing). Kalau lo desain sistem kayak semua call itu local function call, bakal collapse pas skala gede.

3. Bandwidth is infinite
Dikira bisa kirim data sebanyak apapun tanpa batas. Nyatanya bandwidth terbatas, apalagi kalau banyak service saling komunikasi (chatty communication bisa bikin network jenuh).

4. The network is secure
Asumsi data yang lewat jaringan aman dari penyadapan/manipulasi. Padahal network bisa disusupi — makanya butuh enkripsi (TLS), autentikasi, dll.

5. Topology doesn't change
Dikira struktur jaringan (server mana connect ke mana) itu statis selamanya. Kenyataan: server ditambah/dihapus, IP berubah, load balancer reroute traffic — sistem harus tahan terhadap perubahan topologi.

6. There is one administrator
Diasumsikan ada satu pihak yang kontrol penuh seluruh infrastruktur. Di sistem nyata (apalagi yang melibatkan third-party service, cloud provider, multi-tim), ada banyak "administrator" dengan kebijakan beda-beda — koordinasi jadi masalah tersendiri.

7. Transport cost is zero
Dikira ngirim data itu "gratis" — nggak ada overhead. Padahal serialize/deserialize data, buka koneksi, maintain protocol overhead itu semua makan resource (CPU, biaya, waktu).

8. The network is homogeneous
Diasumsikan semua node pakai stack/protokol yang sama. Nyatanya jaringan itu campuran — beda OS, beda hardware, beda protokol (bahkan legacy system ikut nyambung). Perlu interoperability.

Kaitan ke desain sistem lain (yang lo singgung soal SPOF)

Fallacy-fallacy ini sering jadi akar dari masalah desain kayak:

Single Point of Failure (SPOF) — biasanya muncul karena orang percaya fallacy #1 (network reliable) atau #6 (satu administrator/satu server ngurusin semua). Kalau arsitekturnya monolitik, satu titik gagal bisa jatuhin seluruh sistem karena nggak ada redundancy.
Tight coupling antar service — akibat percaya latency = 0, jadi desain sinkron semua padahal harusnya ada async/queue.
Cascading failure — kalau satu service down dan yang lain nggak punya fallback/circuit breaker (karena asumsi network reliable), failure-nya nyebar ke seluruh sistem.

Kalau lo lagi bikin tugas atau paper soal ini (kayaknya konteksnya course-related ya?), mau gue bantu kaitin tiap fallacy ke contoh kasus nyata atau ke arsitektur sistem terdistribusi tertentu (microservices, distributed database, dll)? | --- |
| 19 - 09 - 2026 | Claude | jadi ketika ada study case seperti 
Startup FoodGo (aplikasi pesan-antar makanan) mengalami kegagalan sistem saat pesanan melonjak (misalnya jam makan siang atau saat promo besar). Gejala yang dilaporkan tim engineering FoodGo:

Saat trafik naik, satu server yang menangani semua modul (pesanan, pembayaran, notifikasi kurir) kewalahan karena semuanya berjalan di satu proses monolitik yang sama.
aku bisa simpulkan bahwa ada kesalahan sistem yaitu singlepoint of failure karena beban yang diberikan kepada satu proses monolitik yang sama membuat seluruh proses berebut sumber daya komputasi yang sama sehingga ketika ada proses yang terhenti atau mengalami keterlambatan  thread yang ada d server akan terus menunggu sehingga akan menyebabkan thread pool starvation yang membuat proses lain tidak akan dapat thread untuk menjalankan prosesnya. Penumpukan yang tidak dapat dibebaskan akan menyebabkan sistem mengalami crash karena out of memory. Karena sistem terpusat pada satu proses di satu server dan terjadi sebuah kemacetan atau crash, seluruh platform akan jatuh dan meminta untuk di restart manual.

validasi dan koreksi pendapat ku | Analisis lo udah bener secara garis besar, cuma ada beberapa hal yang perlu diluruskan biar strukturnya lebih presisi secara konsep. Gue breakdown ya:

Yang udah bener:

Identifikasi SPOF karena arsitektur monolitik → tepat
Mekanisme resource contention → thread pool starvation → OOM → crash → itu chain logic yang valid dan emang gitu biasanya kejadiannya di real case

Yang perlu dikoreksi/diperjelas:

SPOF itu bukan "kesalahan" yang disebabkan oleh beban, tapi karakteristik desain yang membuat beban jadi fatal.
Kalimat lo agak kebalik: "SPOF karena beban yang diberikan kepada satu proses monolitik membuat seluruh proses berebut sumber daya" — ini nyampur root cause sama mekanisme. Yang lebih tepat:
Root cause (desain): arsitektur monolitik = semua modul (order, payment, notifikasi kurir) jalan dalam satu proses, satu server, tanpa isolasi resource. Ini yang bikin sistem punya SPOF.
Trigger: lonjakan traffic (jam makan siang/promo)
Mekanisme kegagalan: karena nggak ada isolasi, modul-modul berebut CPU/memory/thread pool yang sama → starvation → OOM → crash
Jadi urutannya: desain monolitik (kondisi) → traffic spike (trigger) → resource contention (mekanisme) → crash (akibat). SPOF-nya ada di poin pertama, bukan hasil dari beban itu sendiri.
Perlu dibedakan: ini bukan cascading failure antar service (karena cuma satu proses), tapi "internal resource exhaustion" yang menyebar antar modul dalam proses yang sama.
Di sistem microservices, biasanya istilahnya cascading failure (kegagalan satu service nular ke service lain lewat network call). Tapi di kasus FoodGo ini semuanya satu proses monolitik, jadi lebih tepat disebut modul-modul saling starve resource di dalam proses yang sama — bukan lewat network, tapi lewat shared memory/CPU/thread pool. Bedanya penting kalau lo mau kasih solusi (solusinya beda: microservices decomposition vs. circuit breaker antar service).
Tambahan poin yang bisa memperkuat analisis lo: nggak ada resource isolation (bulkhead pattern) dan nggak ada horizontal scaling. Karena semua modul di satu proses/server, pas notifikasi kurir misalnya nge-hang (nunggu response provider eksternal), thread yang dipakai buat modul itu ketahan, padahal thread pool itu shared sama modul pesanan & pembayaran. Ini yang bikin efeknya nyebar ke semua fitur padahal masalahnya cuma di satu modul.
Soal "manual restart" — ini valid sebagai konsekuensi SPOF (nggak ada redundancy/failover otomatis), tapi worth disebutin eksplisit sebagai bagian dari kelemahan desain: nggak ada health check + auto-restart atau multiple instance dengan load balancer.

Ringkasnya, kesimpulan lo soal SPOF udah tepat, tinggal diperbaiki urutan sebab-akibatnya: desain monolitik → jadi SPOF secara struktural, dan resource contention/thread starvation/OOM itu mekanisme teknis yang menjelaskan kenapa SPOF ini fatal saat traffic naik, bukan penyebab SPOF itu sendiri.

Mau gue bantu susun ini jadi format analisis yang lebih terstruktur (root cause – mechanism – impact – rekomendasi solusi) buat laporan/tugasnya? | Bukti di skenario:
Saat trafik naik, satu server yang menangani semua modul (pesanan, pembayaran, notifikasi kurir) kewalahan karena semuanya berjalan di satu proses monolitik yang sama yang berujung pada Server backend kadang crash total dan perlu di-restart manual.

Kenapa ini keliru:
Desain arsitektur FoodGo menyatukan seluruh domain bisnis ke dalam satu proses tunggal (shared runtime) tanpa isolasi sumber daya (failure domain isolation atau bulkhead pattern). Mengasumsikan satu proses server dapat menyerap beban heterogen secara seragam adalah kekeliruan. Modul pesanan yang butuh latensi rendah harus berbagi CPU, thread pool, dan memory dengan modul pembayaran dan notifikasi yang bergantung pada I/O jaringan eksternal.

Dampak ke FoodGo:
Ketika modul pembayaran atau notifikasi mengalami keterlambatan eksternal, thread eksekusi tertahan (thread starvation). Karena pool thread digunakan bersama, modul pesanan yang kodenya sehat tidak lagi mendapat jatah komputasi. Antrean request yang menumpuk tak terkelola memicu lonjakan memori hingga OS melakukan terminasi paksa (Out-Of-Memory kill). Ketiadaan redundansi (Single Point of Failure) dan mekanisme self-healing/health-check membuat satu kegagalan modul melumpuhkan seluruh platform FoodGo secara total dan menuntut restart manual. |

| 19 - 09 - 2026 | Claude | dari masalah itu solusi yang diberikan apa? aku cuma bisa mikir untuk memisahkan modul nya dan menggunakan load balancer supaya ketidakadaan satu server tidak langsung mematikan operasional secara keseluruhan | Arah lo udah bener, itu dua pilar utama solusinya. Gue lengkapin biar lebih komprehensif dan bisa dipetakan balik ke tiap fallacy/masalah yang udah diidentifikasi:

1. Decompose monolitik → microservices (poin lo)
Pisahin jadi service independen: Order Service, Payment Service, Notification/Courier Service, dst. Masing-masing punya proses, resource (CPU/memory/thread pool), bahkan database sendiri kalau perlu. Efeknya: kalau Notification Service ngalamin delay (misal nunggu provider eksternal), dia nggak akan makan thread pool yang dipakai Payment atau Order Service. Ini langsung ngatasin akar masalah resource contention yang lo bahas sebelumnya.

2. Load balancer + horizontal scaling (poin lo)
Setiap service dijalankan di multiple instance, load balancer distribusiin traffic ke instance yang available. Kalau satu instance/server down, LB otomatis reroute ke instance lain → nggak ada downtime total. Ini yang ngilangin karakteristik SPOF.

3. Tambahan yang penting buat melengkapi:

Message Queue / Asynchronous Processing (misal RabbitMQ, Kafka): Order masuk, notifikasi ke kurir nggak perlu diproses synchronous langsung. Order Service cukup publish event ke queue, Notification Service consume kapan pun dia siap. Ini motong ketergantungan langsung antar modul dan nyerap lonjakan traffic (buffer saat spike).
Circuit Breaker Pattern: kalau salah satu service (misal Payment) mulai lambat/gagal, circuit breaker "matiin sementara" pemanggilan ke situ biar nggak nyeret service lain ikut lambat (mencegah cascading failure antar service setelah dipecah jadi microservices).
Auto-scaling: instance ditambah otomatis pas traffic naik (jam makan siang/promo), dikurangin lagi pas sepi. Ini langsung ngatasin trigger dari kasus lo (lonjakan traffic yang predictable/periodik).
Database per service / connection pool terpisah: biar Payment Service nggak ikut lambat gara-gara Order Service query berat ke database yang sama.
Health check + auto-restart/self-healing: kalau satu instance crash, orchestrator (misal Kubernetes) otomatis restart instance itu tanpa perlu manual intervention — ini jawab langsung soal "manual restart" yang lo sebut di analisis sebelumnya.
Rate limiting / request throttling: buat nahan traffic supaya nggak semua request masuk sekaligus pas promo, kasih graceful degradation (misal nomor antrian) daripada sistem collapse total.

Pemetaan balik ke root cause:

Masalah	Solusi
Modul jadi satu proses (SPOF)	Decompose ke microservices
Nggak ada redundancy	Load balancer + multiple instance
Resource contention/thread starvation	Isolasi resource per service + async queue
Nggak ada mekanisme scaling	Auto-scaling
Kegagalan satu titik nyebar	Circuit breaker
Restart manual	Health check + self-healing (orchestration)

Kalau lo mau, gue bisa bantu gambarin ini jadi diagram arsitektur before-after (monolitik vs microservices) biar lebih gampang dipresentasiin di tugas. | Solusi desain awal:

Penerapan Redundansi Horizontal (Short-term): Menjalankan beberapa instance backend monolitik secara bersamaan di balik Load Balancer + horizontal scaling untuk mengeliminasi SPoF.
Asynchronous Decoupling via Message Queue: Mengisolasi modul notifikasi dan proses downstream pembayaran ke antrean pesan (event-driven worker), sehingga modul pesanan tidak menunggu proses I/O selesai.
Pemisahan Modul Bertahap (Modular Monolith to Microservices): Memisahkan modul pembayaran dan notifikasi menjadi service terpisah dengan alokasi resource komputasi mandiri. |

| 19 - 09 - 2026 | Claude | terus ada trade off nya ngga? bukannya kalau dipisahkan bakal lebih mahal untuk server nya ya | Ada, dan itu poin penting yang sering diabaikan orang pas buru-buru bilang "microservices is the answer". Trade-off-nya nyata, bukan cuma soal biaya server doang. Gue breakdown:

1. Biaya infrastruktur naik (poin lo bener)
Monolitik: 1 server bisa handle semua modul.
Microservices: tiap service butuh instance sendiri (minimal 2 buat redundancy), plus load balancer, plus message queue, plus mungkin database terpisah per service. Total resource yang di-provision jauh lebih banyak, walaupun total traffic-nya sama. Ini yang disebut operational overhead cost.

2. Kompleksitas operasional meningkat drastis

Butuh orchestration tool (Kubernetes, dll) buat ngatur deployment, scaling, health check — ini sendiri butuh keahlian khusus (DevOps/SRE) yang mahal dari sisi SDM.
Monitoring & debugging jadi lebih susah: dulu error di satu proses, sekarang error bisa nyebar lintas service, butuh distributed tracing (misal Jaeger, Zipkin) buat nelusurin request yang lewat banyak service.
Deployment jadi lebih ribet: harus mikirin versioning API antar service, backward compatibility, dll.

3. Latency antar service (ini balik lagi ke fallacy #2 & #3 yang lo pelajarin!)
Di monolitik, komunikasi antar modul itu function call langsung (dalam memory, hampir instan). Di microservices, komunikasi antar service itu network call (HTTP/gRPC) — ada latency, ada kemungkinan gagal (fallacy "latency is zero" dan "network is reliable" jadi relevan lagi di sini, ironisnya solusi buat SPOF ini malah "menghidupkan" fallacy lain kalau nggak dikelola dengan baik).

4. Data consistency jadi masalah baru
Kalau Order Service dan Payment Service punya database sendiri-sendiri, gimana caranya mastiin data konsisten (misal order udah dibuat tapi payment gagal)? Ini butuh pattern tambahan kayak Saga Pattern atau eventual consistency, yang nggak perlu dipikirin sama sekali di monolitik (transaksi ACID biasa cukup).

5. Butuh tim & skill yang lebih matang
Microservices cocok kalau tim udah besar dan bisa dipecah per service ownership. Buat startup kecil/early-stage, ini malah overhead yang nggak sepadan — makanya sering ada saran "jangan mulai dari microservices, mulai dari monolitik yang well-structured (modular monolith), baru pecah kalau emang udah kebukti butuh scale di titik tertentu."

Kesimpulan buat kasus FoodGo:
Kalau FoodGo masih startup kecil, mungkin solusi paling proporsional bukan langsung full microservices, tapi:

Tahap 1 (short-term/murah): modular monolith + horizontal scaling (multiple instance dari monolitik yang sama di belakang load balancer) + async queue buat notifikasi kurir. Ini udah ngurangin SPOF signifikan tanpa overhead microservices penuh.
Tahap 2 (kalau udah scale besar): baru pecah jadi microservices per modul yang emang butuh scale independen (misal Payment Service beda kebutuhan scaling-nya dari Notification Service).

Ini namanya trade-off antara availability/scalability vs. cost & complexity — nggak ada solusi gratis, cuma milih mana yang worth it sesuai skala masalah.

Mau gue bantu bikin tabel perbandingan cost-benefit monolitik vs microservices buat pertimbangan tugas lo? | Trade-off:
Pemisahan arsitektur dan desentralisasi proses membawa biaya operasional (operational overhead) yang signifikan:

Kembalinya Fallacies Jaringan: Komunikasi antar modul yang awalnya in-memory berubah menjadi network calls, yang menimbulkan latensi tambahan dan overhead serialisasi (transport cost).
Integritas Data & Kompleksitas: Hilangnya transaksi atomik basis data (single ACID transaction) memaksa tim mengelola eventual consistency atau Saga Pattern, yang jauh lebih rawan bug logika dan menuntut distributed tracing untuk debugging. |


|19 -09-2026 |Chatgpt|Aku sedang mengerjakan tugas analisis pitfall sistem terdistribusi dengan aturan AI Level 2. AI boleh membantu brainstorming dan menyusun kerangka berpikir, tetapi analisis akhir harus kutulis sendiri.
Bagian skenario yang menjadi tanggung jawabku:
di studi kasus foodGo aplikasi pesan-antar makanan) mengalami kegagalan sistem saat pesanan melonjak (misalnya jam makan siang atau saat promo besar).  
Tim menemukan bahwa kode mereka menulis asumsi seperti `# network is always reliable, no need for retry` dan tidak ada *timeout* sama sekali pada pemanggilan antar service (modul pesanan memanggil modul pembayaran dan menunggu tanpa batas waktu)  
pemikiran awalku :
1. Aku sudah memahami bahwa pitfall-nya berkaitan dengan kesalahan menganggap jaringan selalu bisa diandalkan.
2. anggapan network always reliable salah satu sumber masalah ini dan dengan tidak adanya timeout juga menjadi masalah karena modul pesanan bisa terus menunggu respons pembayaran.
3. pitfallnnya berkaitan dengan anggapan network selalu realible
4. trus karna tanpa time out jadinya menghabiskan resource, akibatnya jadi ngelag
5.  solusi awalku yaity membatasi jumlah request dan memberikan time out, tapi aaku masih butuh penjelasan kedua solusi tersebut
nah aku juga butuh tau trade off dari pemikiran awalku, dan apakah ada solusi yang lebih baik , dan jika ada apakah ada resiko dari solusi tersebut?|Identifikasi kamu sudah tepat, Julio. Yang masih perlu diperjelas adalah mekanisme dampaknya dan fungsi masing-masing solusi. Penilaianku:

Asumsi “network is always reliable” sudah benar kamu identifikasi. Ketiadaan timeout merupakan keputusan desain yang perlu kamu bahas bersama asumsi tersebut.
“Memboroskan sumber daya dan membuat server berat” masih terlalu umum. Coba pikirkan: sumber daya apa yang tertahan saat menunggu? Bisa berupa koneksi, memori, atau slot worker, bergantung implementasinya. Menunggu respons tidak otomatis berarti CPU bekerja keras. Penjelasan sumber daya yang tertahan.

Ide membatasi 10 request per menit disebut rate limiting. Itu bisa membantu mengendalikan beban, tetapi fungsinya berbeda dengan timeout:

Mekanisme	Yang dibatasi
Rate limiting	Jumlah request dalam rentang waktu tertentu
Timeout	Lama menunggu suatu operasi

Request yang sudah diterima tetap bisa menunggu terlalu lama meskipun jumlah request dibatasi. Angka 10 per menit juga masih contoh: perlu dijelaskan berlaku per pengguna atau seluruh sistem, serta dasar pemilihannya. Penjelasan rate limiting.

Ide timeout relevan, tetapi tentukan tempat penerapannya. Untuk bagianmu, pikirkan batas tunggu pada pemanggilan ke layanan pembayaran. Menghentikan animasi loading di layar saja tidak cukup. Ingat juga: pemanggil berhenti menunggu belum membuktikan pembayaran gagal atau berhenti diproses. Karena itu, mencoba ulang pembayaran perlu mempertimbangkan risiko operasi ganda. Penjelasan retry dan idempotensi.
Saat pemanggilan layanan menunggu, sumber daya seperti koneksi, memori, atau slot worker dapat tetap terpakai, bergantung implementasinya. Jadi, “server berat” belum tentu berarti CPU bekerja keras; bisa juga kapasitas untuk melayani permintaan lain semakin terbatas. Penjelasan sumber daya yang tertahan.

Trade-off berarti konsekuensi yang kamu terima untuk mendapatkan suatu manfaat. Solusi bisa memperbaiki satu sisi sekaligus menambah batasan atau risiko di sisi lain.

Untuk dua ide awalmu, perbedaannya seperti ini:

Solusi	Cara kerja dan manfaat	Trade-off
Rate limiting	Membatasi jumlah request dalam periode tertentu, misalnya per pengguna per menit. Membantu mengendalikan laju permintaan.	Batas terlalu ketat bisa menolak permintaan pengguna yang sah. Batas terlalu longgar kurang membantu melindungi kapasitas.
Timeout	Menentukan berapa lama pemanggil bersedia menunggu respons sebelum berhenti menunggu.	Terlalu singkat bisa membuat respons yang sebenarnya masih akan berhasil dianggap terlambat. Terlalu panjang membuat sumber daya tertahan lebih lama.

Rate limiting mengendalikan berapa banyak request yang boleh masuk atau dikirim. Ia tidak menentukan kapan penantian suatu request berakhir. Karena itu, keduanya bisa saling melengkapi. Angka seperti 10 request per menit perlu punya dasar kapasitas dan kejelasan cakupan: per pengguna, per layanan, atau seluruh sistem. Penjelasan rate limiting.

Ada satu hal penting tentang timeout: berhenti menunggu tidak otomatis menghentikan pekerjaan di layanan tujuan. Misalnya, sebuah operasi mungkin sudah berhasil, tetapi responsnya belum sampai. Timeout membuat hasilnya belum diketahui oleh pemanggil; bukan bukti pasti bahwa operasinya gagal. Penjelasan kegagalan respons dan pengulangan operasi.

Untuk mengembangkan pilihan solusi, kamu bisa mempertimbangkan dua mekanisme berikut:

Retry terbatas dengan backoff, untuk kegagalan sementara.
Retry berarti mencoba kembali. Backoff berarti memberi jeda yang semakin panjang sebelum mencoba lagi. Jumlah percobaannya tetap dibatasi.

Manfaatnya: operasi mendapat kesempatan berhasil setelah gangguan sementara pulih.

Risikonya: percobaan tambahan dapat memperberat layanan yang sudah kewalahan. Pengulangan juga bisa menggandakan tindakan jika operasinya tidak aman diulang. Karena itu, pelajari idempotensi, yaitu pengulangan operasi yang tidak menambah efek setelah pelaksanaan pertama. Penjelasan retry dan risikonya.

Circuit breaker, untuk kegagalan yang berulang.
Mekanisme ini memantau kegagalan. Ketika ambang tertentu tercapai, panggilan ke layanan tersebut dihentikan sementara. Setelah jeda, sejumlah kecil panggilan dicoba kembali untuk memeriksa pemulihan.

Manfaatnya: mengurangi panggilan yang kemungkinan besar akan gagal dan memberi layanan kesempatan pulih.
Risikonya: ambang yang kurang tepat bisa menghentikan panggilan terlalu cepat, atau membuat layanan yang sudah pulih belum segera digunakan kembali. Pengaturannya juga menambah kerumitan. Penjelasan circuit breaker.
Untuk masalah menunggu tanpa batas, timeout pada pemanggilan antarservice merupakan prioritas paling langsung. Setelah itu, pertimbangkan retry untuk gangguan sementara yang aman dicoba ulang, dan circuit breaker bila kegagalan terus berulang. Rate limiting tetap relevan sebagai pengendalian trafik, tetapi alasan penggunaannya perlu kamu jelaskan tersendiri.|**Bukti di skenario:** Tim menemukan asumsi dalam kode berupa `# network is always reliable`, no need for retry. Selain itu, tidak ada timeout pada pemanggilan antarservice, sehingga modul pesanan menunggu respons modul pembayaran tanpa batas waktu.

**Kenapa ini keliru:** Asumsi “network is always reliable” keliru karena mengabaikan kemungkinan koneksi terputus, respons terlambat, atau respons tidak diterima. Anggapan “no need for retry” juga mengabaikan kemungkinan bahwa permintaan yang terganggu sementara dapat berhasil jika dicoba kembali setelah gangguan pulih, meskipun retry perlu dibatasi dan hanya dilakukan jika aman. Selain itu, tidak adanya timeout membuat modul pesanan bergantung pada respons modul pembayaran yang belum tentu datang. Akibatnya, modul pesanan bisa terus menunggu dan menahan resource yang dibutuhkan untuk menangani pesanan lain.
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
* **Pemeriksaan status setelah timeout:** sistem membutuhkan proses tambahan untuk memastikan hasil pembayaran. Pengecekan berkala menambah request, sedangkan penggunaan notifikasi perlu menangani kemungkinan notifikasi terlambat atau dikirim berulang.
* **Retry menambah request dan waktu tunggu:** percobaan tambahan bisa membantu saat gangguan sementara, tetapi juga dapat memperparah beban kalau layanan sudah kewalahan.
* **Retry menambah beban :** percobaan tambahan dapat memperberat layanan.
* **circuit breaker memperlambat layanan yang sudah pulih terlambat digunakan kembali:** Circuit breaker berisiko menolak request terlalu cepat atau tetap membatasi akses saat layanan sudah pulih. Pengaturan ambangnya juga menambah kerumitan.

  |
| 19-09-2026 | Chatgpt | okeh lanjut, cukup dengan solusi dan trade off, 

 walaupun kita sudah bahas sejauh ini dari yang sudah kita bahas sebelumnya, tapi apa sih dampak spesifik dan kenapa sih anggapan "Tim menemukan asumsi dalam kode berupa `# network is always reliable`, no need for retry. Selain itu, tidak ada timeout pada pemanggilan antarservice, sehingga modul pesanan menunggu respons modul pembayaran tanpa batas waktu.  " keliru aku butuh penjelasan lebih spesifik dan penjelasan yang lebih jelas | Julio, **dugaanmu masuk akal: penantian tanpa batas bisa membuat gangguan di layanan pembayaran ikut menghambat layanan pesanan.** Hubungan sebab-akibatnya perlu dijelaskan lebih jauh daripada sekadar “server menjadi berat”.

Anggapan **`network is always reliable`** keliru karena komunikasi antarservice bisa mengalami gangguan, sekalipun kode kedua layanan sudah benar. Misalnya, koneksi terputus sementara atau komunikasi melambat saat trafik tinggi. Layanan pembayaran juga bisa terlambat merespons karena sedang kewalahan. Artinya, **mengirim request tidak menjamin respons berhasil diterima dalam waktu yang dibutuhkan.** [Microsoft: gangguan sementara pada komunikasi layanan](https://learn.microsoft.com/en-us/azure/architecture/best-practices/transient-faults).

Komentar **`no need for retry`** menunjukkan bahwa kemungkinan gangguan sementara tersebut diabaikan. Contohnya, koneksi gagal sesaat dan pemanggilan mengembalikan error. Operasi pesanan bisa berakhir gagal walaupun layanan kembali normal beberapa detik kemudian. Keputusan memakai retry memang bergantung pada jenis operasi, tetapi alasan “tidak perlu karena jaringan pasti andal” tidak tepat. [Microsoft: Retry pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/retry).

**Ketiadaan timeout membuat modul pesanan tidak memiliki batas waktu tunggu yang ditentukan aplikasi.** Jika respons tidak datang dan tidak ada error atau mekanisme lain yang menghentikan panggilan, request dapat terus menggantung. Selama itu, sebagian sumber daya masih terikat pada pekerjaan yang belum selesai.

Bayangkan contoh berikut. **Angka ini hanya ilustrasi**, dengan asumsi server pesanan memiliki **10 worker**, yaitu proses atau thread yang masing-masing menangani satu request sampai selesai:

1. Sepuluh pengguna membuat pesanan. Semua worker memanggil layanan pembayaran.
2. Layanan pembayaran mengalami gangguan sehingga responsnya tidak kunjung datang.
3. Kesepuluh worker tetap menunggu. Belum ada worker yang bebas untuk menangani request berikutnya.
4. Pengguna ke-11 harus mengantre, bahkan sebelum pesanannya sempat diproses. Ketika pengguna terus berdatangan, antrean bertambah.

Dalam contoh ini, sumber daya yang dapat tertahan adalah:

| Sumber daya               | Apa yang terjadi selama menunggu?                                                                    |
| ------------------------- | ---------------------------------------------------------------------------------------------------- |
| **Slot worker**           | Tetap ditempati request lama sehingga kapasitas untuk menangani request baru berkurang.              |
| **Koneksi ke pembayaran** | Koneksi yang masih digunakan oleh panggilan tertunda belum tersedia untuk panggilan lain.            |
| **Memori**                | Data dan status request yang belum selesai tetap disimpan. Antrean tambahan juga membutuhkan memori. |

Lama menunggu memang dapat memperpanjang penggunaan koneksi, thread, dan memori. Sumber daya yang benar-benar tertahan bergantung pada implementasi servernya. [Microsoft: dampak waktu tunggu terhadap sumber daya](https://learn.microsoft.com/en-us/azure/architecture/best-practices/transient-faults).

Dampak spesifiknya pada FoodGo kemudian bisa berupa:

* **Waktu respons meningkat:** pengguna menunggu giliran diproses, lalu masih harus menunggu pembayaran.
* **Jumlah pesanan yang selesai per detik menurun:** banyak kapasitas tertahan untuk menunggu.
* **Request baru gagal dilayani:** antrean atau kapasitas koneksi bisa mencapai batas.
* **Gangguan menyebar:** masalah yang awalnya terjadi pada pembayaran ikut membuat layanan pesanan tidak tersedia. Penyebaran gangguan seperti ini disebut *cascading failure*. [Google SRE: kegagalan berantai dan kehabisan sumber daya](https://sre.google/sre-book/addressing-cascading-failures/).

**Menunggu tidak otomatis membuat CPU bekerja keras.** Dalam contoh tadi, server kesulitan melayani pengguna karena slot penanganannya penuh, walaupun pekerjaan yang menempatinya sedang menunggu.

Ada juga dampak pada **kejelasan status transaksi**. Pembayaran mungkin sudah berhasil diproses, tetapi respons konfirmasinya gagal sampai ke modul pesanan. Akibatnya, pengguna bisa sudah terbayar sementara pesanan masih terlihat menunggu konfirmasi. **Belum menerima respons tidak cukup untuk memastikan pembayaran gagal.** [Microsoft: operasi berhasil tetapi respons tidak terkirim](https://learn.microsoft.com/en-us/azure/architecture/patterns/retry).
 | Kenapa ini keliru: Asumsi “network is always reliable” keliru karena mengabaikan kemungkinan koneksi terputus, respons terlambat, atau respons tidak diterima. Anggapan “no need for retry” juga mengabaikan kemungkinan bahwa permintaan yang terganggu sementara dapat berhasil jika dicoba kembali setelah gangguan pulih, meskipun retry perlu dibatasi dan hanya dilakukan jika aman. Selain itu, tidak adanya timeout membuat modul pesanan bergantung pada respons modul pembayaran yang belum tentu datang. Akibatnya, modul pesanan bisa terus menunggu dan menahan resource yang dibutuhkan untuk menangani pesanan lain.

Dampak ke FoodGo: Request yang terus menunggu dapat menahan koneksi, memori, atau slot worker. Saat pesanan melonjak, kapasitas untuk melayani request baru berkurang, antrean bertambah, dan aplikasi melambat atau gagal melayani pengguna. Gangguan pada pembayaran akhirnya bisa ikut menghambat layanan pesanan. Status pesanan juga dapat tetap menunggu meskipun pembayaran sudah berhasil, apabila respons konfirmasinya belum diterima. |
