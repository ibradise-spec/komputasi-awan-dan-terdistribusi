# Jurnal Proses — Tugas 3

## Percobaan tanpa Lock
- Hasil `processed_count` yang didapat: 35 (Seharusnya 100)
- Kenapa bisa meleset (jelaskan mekanisme race condition dengan kata sendiri): Dikarenakan ada dua threads atau lebih yang selesai dalam waktu bersamaan. Contoh selesai dalam waktu 2 miliseconds tepat bersamaan. kondisi ini membuat dua threads tersebut menambahkan 'processed_count' pada waktu yang sama sehingga tidak menyadari adanya penambahan yang dilakukan oleh threads lainnya yang menyebabkan terjadinya satu hitungan tertimpa atau hilang.

## Percobaan dengan Lock
- Hasil `processed_count` setelah perbaikan: 100

## Kendala Docker
- Error yang ditemui saat `docker build`/`docker run` dan cara memperbaikinya:
- Error "Code language not supported": Terjadi karena mencoba menjalankan Dockerfile menggunakan tombol eksekusi ekstensi Code Runner. Diperbaiki dengan menjalankan perintah docker build langsung di terminal.
- Error "failed to connect to the docker API": Terjadi karena aplikasi Docker (daemon) belum berjalan. Diperbaiki dengan membuka dan memastikan aplikasi Docker Desktop berjalan ("Engine running") sebelum mengeksekusi perintah.
- Error "open Dockerfile: no such file or directory": Terjadi karena salah penamaan file dengan huruf F kapital (DockerFile) dan kurangnya file requirements.txt. Diperbaiki dengan melakukan rename menjadi Dockerfile (f kecil) dan membuat file requirements.txt kosong.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
| :--- | :--- | :--- | :--- | :--- |
| 4 Okt 2026 | Gemini | Meminta penjelasan beda multiprocessing dan multithreading untuk tugas ini. | Memberikan analogi dapur dan koki untuk membedakan alokasi memori (fork vs shared memory). | Saya menggunakan pemahaman konsep shared memory ini untuk menyusun kalimat analisis penyebab race condition di jurnal dengan bahasa saya sendiri. |
| 4 Okt 2026 | Gemini | Meminta cara memicu race condition dan setup threading.Lock() di kode Python. | Memberikan teknik pembagian langkah (baca, time.sleep, tulis) agar OS melakukan context switch saat thread bekerja. | Mengadaptasikan logika time.sleep tersebut untuk melengkapi bagian TODO 1 dan TODO 2 di file src/order_simulator.py. |
| 4 Okt 2026 | Gemini | Meminta bantuan memperbaiki error Docker build API not connect dan file not found. | Menyarankan untuk menyalakan Docker Desktop daemon, memperbaiki penamaan file menjadi Dockerfile (case-sensitive), dan menyiapkan requirements.txt. | Menjalankan aplikasi Docker, melakukan rename file, membuat file requirements, dan berhasil menjalankan kontainer Docker. |
