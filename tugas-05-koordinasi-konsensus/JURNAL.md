# Jurnal Proses — Tugas 5

## Pemilihan bully algorithm vs raft
Dalam kasus ini, sistem membutuhkan satu node leader tunggal sebagai single source of truth untuk mengurutkan pesanan pusat (centralized order sequencing) agar tidak terjadi race condition atau pemroresan pesanan ganda akibat clock drift atau jam fisik antar server tidak sinkron.
Oleh karena itu, dengan adanya bully algorithm, terdapat algoritma yang sangat ringan yang diimplementasikan pada klaster kecil dengan topologi 5 node statis. Pemilihannya deterministik, node dengan ID tertinggi yang hidup pasti menang. Dalam konteks ini, dapat ditetapkan ID tertinggi pada server dengan spesifikasi hardware paling kuat untuk menjadi koordinator antrean.
Selain itu, tanpa perlu mekanisme randomized election timer atau voting quorum yang kompleks, node dengan ID tertinggi dapat langsung mendeklarasikan dirinya sebagai coordinator begitu mendeteksi ketiadaan node di atasnya.

## Implementasi Bully
- Kendala saat mengisi TODO 1-4: ...

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
| ... | ... | ... | ... | ... |
