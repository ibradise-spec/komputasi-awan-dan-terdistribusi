# Jurnal Proses — Tugas 6

## Implementasi find_successor
- Kesalahan pertama yang ditemui (mis. lupa wrap-around di ring): Perlu memperhatikan kondisi ketika nilai hash key lebih besar daripada seluruh ID node dalam ring.
- Cara memperbaikinya: Menambahkan mekanisme wrap-around dengan mengembalikan ID node terkecil apabila tidak ditemukan successor yang memenuhi kondisi.

## Skenario join/leave
- Hasil sebelum & sesudah node baru bergabung: Pada kondisi awal terdapat empat node, yaitu Jakarta-1, Jakarta-2, Bandung, dan Surabaya. Setelah node Makassar bergabung, mapping kurir-001 berpindah dari node Jakarta-2 ke node Makassar karena node baru memiliki hash yang menjadi successor dari key tersebut.
- Hasil sebelum & sesudah node keluar: Ketika node Surabaya keluar dari ring, mapping kurir-003 yang sebelumnya disimpan pada node Surabaya dialihkan ke node Jakarta-1 sebagai successor berikutnya.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
