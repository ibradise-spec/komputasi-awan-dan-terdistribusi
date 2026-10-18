# Jurnal Proses — Tugas 5

## Implementasi Bully
* Kendala saat mengisi TODO 1-4: ...
1. **TODO 1 (Menangani Pesan):** Kesulitan dalam mengatur respons setiap pesan 'ELECTION', 'ΟΚ', dan 'COORDINATOR' agar node dapat berkomunikasi sesuai aturan Bully Algorithm
2. **TODO 2 (Memulai Election):** Kesulitan menentukan kapan node harus menunggu balasan 'OK' dan kapan boleh menyatakan dirinya sebagai leader, terutama saat beberapa node melakukan election secara bersamaan|
3. **TODO 3 (Menentukan Leader):** Perlu memastikan pesan 'COORDINATOR' dikirim ke semua node dan setiap node mencatat ID leader yang sama
4. **TODO 4 (Mendeteksi Leader Mati):** Kesulitan mengatur pengecekan leader secara berkala agar saat Node 5 dimatikan, node lain dapat mendeteksinya dan otomatis melakukan election ulang untuk memilih Node 4

## Skenario 1: Start normal
- Leader yang terpilih: Node 5 (Port 5005).
- Log/observasi: Saat dinyalakan bertahap, kepemimpinan sempat naik berjenjang 1 -> 2 -> 3 -> 4 -> 5 sebelum akhirnya stabil di node 5. Saat seluruh node aktif bersamaan, Node 1–4 menerima balasan OK dari node di atasnya dan menunggu, sementara Node 5 langsung mem-broadcast COORDINATOR karena higher_peers miliknya kosong.

## Skenario 2: Leader dimatikan
- Leader baru yang terpilih: Node 4 (Port 5004)
- Berapa lama waktu sampai leader baru terdeteksi: Sekitar 5 hingga 6 detik totalnya. Dengan rincian maksimal 3 detik interval pengecekan time.sleep(3) pada monitor_leader() untuk mendeteksi PING ke node 5 gagal + 2 detik (ELECTION_TIMEOUT = 2.0) waktu tunggu Node 4 memastikan Node 5 tidak membalas pesan OK sebelum akhirnya mendeklarasikan diri sebagai leader baru.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 18/10/2026 | Chatgpt | apa sih itu bully algohritm dan fungsi,gunanya, dan bagaimana alur bully algorthm bekerja?| Menjelaskan tetang bully algorithm | - |
| 18/10/2026 | Chatgpt | contoh implementasi menangani pesan ELECTION, OK, dan COORDINATOR sesuai aturan Bully Algorithm, proses election dengan mengirim pesan ke node yang memiliki ID lebih tinggi. Jika menerima OK, tunggu COORDINATOR. Jika tidak menerima OK dalam waktu 2 detik, node dapat menjadi leader, ungsi untuk menetapkan node sebagai leader dan mengirim pesan COORDINATOR ke semua node lainnya, dan Buat pengecekan leader secara berkala menggunakan PING. Jika leader mati, jalankan election ulang secara otomatis. | di kasih contoh code bully yang sesuai | menjadi todo 1-4 |
