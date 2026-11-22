# Jurnal Proses — Tugas 9

## Diskusi deployment model
- Opsi yang dipertimbangkan dan kenapa akhirnya memilih salah satu: Kami mempertimbangkan tiga opsi utama: Private Cloud murni, Public Cloud murni, dan Hybrid Cloud. Opsi Public Cloud murni langsung ditolak karena melanggar kepatuhan UU PDP dan kedaulatan data (risiko yurisdiksi asing dan multi-tenancy pada data biometrik yang dampaknya permanen jika bocor). Di sisi lain, opsi Private Cloud murni ditolak karena tidak memiliki rapid elasticity yang efisien—pengadaan perangkat keras untuk kapasitas puncak hanya akan memboroskan anggaran saat trafik normal. Kami akhirnya sepakat memilih Hybrid Cloud karena berhasil menyeimbangkan dua kebutuhan utama: keamanan absolut data sensitif (database inti tetap berada di private cloud pemerintah) dan elastisitas tinggi untuk lapisan stateless (API gateway dan portal publik) yang dapat melakukan scale-out ke public cloud saat terjadi lonjakan akses musiman seperti pemilu atau PPDB.

## Diskusi service model per komponen
- Pembagian tanggung jawab layanan per komponen: Kami menyepakati pendekatan multi-service model agar beban pengelolaan tepat sasaran:
1. IaaS di Private Cloud: Dikhususkan untuk Database Inti Kependudukan, Mesin Biometrik, dan HSM. Pemerintah memegang kendali penuh hingga level OS, kernel, dan enkripsi perangkat keras fisik untuk audit menyeluruh.
2. PaaS di Lapisan Hybrid: Dipilih untuk API Gateway verifikasi mitra dan microservices. Model ini membebaskan pengembang dari konfigurasi server fisik dan memfasilitasi orkestrasi kontainer serta auto-scaling otomatis saat cloud bursting.
3. SaaS di Lapisan Klien: Digunakan untuk Portal Cek KTP publik dan Dasbor Petugas Dukcapil Daerah. Menghilangkan kerumitan instalasi maupun maintenance di perangkat daerah, cukup diakses via peramban web dengan otentikasi ketat RBAC dan MFA.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 22 Nov 2026 | Gemini | Bagaimana memetakan service model cloud (IaaS, PaaS, SaaS) yang paling tepat untuk masing-masing komponen sistem data kependudukan (database biometrik, API gateway, dan portal daerah)? | AI menyarankan pendekatan multi-service model: IaaS untuk database inti dan biometrik karena butuh kontrol penuh pada OS/enkripsi hardware di private cloud; PaaS untuk API gateway/microservices agar mudah auto-scaling saat lonjakan akses; dan SaaS untuk portal web warga/petugas daerah agar instansi daerah tidak perlu instalasi lokal. | Saya menggunakan kerangka pembagian tiga model layanan tersebut sebagai landasan konseptual  (Rekomendasi Service Model) di README.md. |
| ... | ... | ... | ... | ... |
