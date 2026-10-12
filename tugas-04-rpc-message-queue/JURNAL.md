# Jurnal Proses — Tugas 4

## Jalur yang dipilih
- Keduanya, alasan: Studi kasus FoodGo memiliki dua karakteristik kebutuhan komunikasi yang berbeda. Kami membutuhkan komunikasi sinkron (RPC) untuk operasi cek status saldo yang mengharuskan modul pesanan mendapat respons seketika untuk validasi kelanjutan transaksi. Di sisi lain, kami membutuhkan komunikasi asinkron (MQ) untuk proses pengiriman notifikasi ke kurir supaya modul pembayaran bisa tetap responsif dan tidak terblokir meskipun modul kurir sedang sibuk atau down.

## Kendala teknis
- Error saat setup (mis. koneksi RabbitMQ ditolak, port bentrok): ...

## Uji "pesan tidak hilang" (khusus Jalur B)
- Langkah uji: matikan consumer → jalankan publisher → nyalakan consumer
- Hasil yang diamati: Ketika consumer dalam keadaan mati dan publisher dijalankan untuk mengirim 3 event pesanan, pesan tersebut tidak hilang melainkan ditampung dengan aman di dalam antrean. Hal ini dibuktikan dari dasbor RabbitMQ yang menunjukkan ada 3 pesan berstatus "ready" di dalam queued messages. Setelah file consumer.py dinyalakan kembali, consumer tersebut secara otomatis langsung menerima dan memproses ketiga notifikasi pembayaran yang tertunda tadi. Dasbor RabbitMQ kemudian kembali menunjukkan angka 0 pada antrean, yang berarti seluruh pesan telah sukses dikonsumsi.

## Analisis lebih lanjut
- Jalur A: Berdasarkan log pengujian RPC, ketika client.py memanggil fungsi cek_saldo('user1'), sistem mengalami proses blocking/menunggu respons selama kurang lebih 2.0480 detik sebelum akhirnya menerima hasil berupa nominal saldo. Hal ini membuktikan bahwa RPC menahan eksekusi proses selanjutnya di sisi klien sampai instruksi di sisi server selesai dikerjakan.
- Jalur B: Pengujian RabbitMQ yang berjalan di dalam kontainer Docker menunjukkan modul publisher dan consumer beroperasi secara independen/decoupled. Pada uji normal, publisher dapat mengirim event secara instan dan langsung diterima oleh consumer, sehingga grafik antrean RabbitMQ tetap kosong. Keunggulan decoupling ini sangat terlihat pada "uji pesan tidak hilang", di mana publisher tidak perlu tahu apakah consumer sedang hidup atau mati, publisher hanya bertugas menyerahkan pesan ke broker RabbitMQ dan tugasnya selesai.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
