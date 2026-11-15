# Jurnal Proses — Tugas 7

## Diskusi pemilihan model konsistensi
- Argumen yang dipertimbangkan: Tim mendiskusikan apakah Eventual Consistency sudah memadai untuk sistem e-wallet FoodGo. Argumen awal mencatat bahwa Eventual Consistency sangat efisien untuk latensi jaringan global, namun memiliki kelemahan fatal berupa stale data saat terjadi replication lag antar wilayah (misal server Jakarta dan Bandung). Untuk data finansial seperti saldo, model Strong/Sequential Consistency global dinilai terlalu mahal karena memperlambat performa sistem secara drastis akibat overhead sinkronisasi lintas region.
- Kesimpulan akhir & alasan: Diputuskan untuk menggunakan Client-Centric Consistency (model Read-Your-Writes). Alasannya, model ini adalah titik tengah yang paling optimal. Memberikan jaminan bahwa pelanggan yang baru melakukan top up atau transaksi akan selalu melihat pembaruan saldonya sendiri secara instan di server mana pun ia terhubung, tanpa harus menanggung beban latensi dari sinkronisasi global seluruh basis data replika secara serentak.

## Simulasi (jika dikerjakan)
- Hasil skenario naif vs Read-Your-Writes: ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
