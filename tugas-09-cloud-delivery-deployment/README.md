# Tugas 9 (Pekan 9) — Cloud Delivery & Deployment Model

**Materi terkait:** Karakteristik esensial cloud computing (NIST SP 800-145), Deployment Model (Public/Private/Hybrid/Community), Service Model (IaaS/PaaS/SaaS).

> Bagian 2 mata kuliah ini murni **analisis & desain di atas kertas** — tidak ada biaya cloud sama sekali, karena tugas berhenti di tahap rekomendasi, bukan implementasi nyata (implementasi baru mulai Tugas 11).

## Studi Kasus

Pemerintah ingin membangun **Sistem Data Kependudukan** (nama, NIK, alamat, data biometrik) yang:
- Sangat **rahasia** (data pribadi warga negara, diatur UU Perlindungan Data Pribadi).
- Diakses oleh **ribuan instansi** (dukcapil daerah, kepolisian, bank untuk verifikasi KYC) dengan pola akses yang **tidak rata** (lonjakan saat musim pemilu/pendaftaran sekolah).
- Butuh **skalabilitas** agar tidak downtime saat lonjakan akses, tapi **tidak boleh** datanya berada di infrastruktur yang tidak terkendali penuh oleh negara.

## Tugas Kelompok

1. **Rekomendasikan Deployment Model** (Public / Private / Hybrid / Community Cloud) yang paling tepat untuk sistem ini. Jelaskan alasannya berdasarkan **karakteristik NIST** (on-demand self-service, broad network access, resource pooling, rapid elasticity, measured service) dikaitkan dengan kebutuhan kerahasiaan vs skalabilitas.
2. **Rekomendasikan Service Model** (IaaS / PaaS / SaaS) yang tepat untuk komponen-komponen berbeda dari sistem ini (boleh berbeda service model untuk komponen berbeda, mis. database inti vs portal publik untuk pengecekan status).
3. Jelaskan **minimal 2 risiko spesifik** dari pilihan kalian dan mitigasinya (mis. jika Hybrid Cloud dipilih: risiko sinkronisasi data antara private & public segment).
4. Bandingkan singkat dengan **satu alternatif yang kalian tolak** — kenapa alternatif itu kurang tepat (mis. kenapa Public Cloud murni ditolak, atau kenapa Private Cloud murni dianggap kurang skalabel).

## 1. Rekomendasi Deployment Model

Kami merekomendasikan Hybrid Cloud. Data inti (database kependudukan, biometrik, dan manajemen kunci enkripsi) tetap di private cloud milik pemerintah. Lapisan yang bersifat stateless dan tidak menyimpan data pribadi mentah (portal cek status, API gateway di sisi depan, cache non-sensitif) dapat melakukan scale-out ke public cloud saat terjadi lonjakan akses.

### Berdasrakan prinsip NIST

On-demand self-service. Tim pengelola dan instansi dapat melakukan provisioning environment, API key, dan kuota secara mandiri tanpa tiket manual. Saat menjelang pemilu, tim pusat dapat menambah kapasitas di public cloud tanpa proses pengadaan hardware baru.

Broad network access. Ribuan instansi dengan jenis klien berbeda (sistem dukcapil daerah, sistem kepolisian, core system bank) mengakses lewat mekanisme standar, yaitu API berbasis HTTPS dengan mutual TLS melalui API gateway. Jangkauan luas ini dicapai tanpa membuka database langsung ke jaringan luar.

Resource pooling. Private cloud melayani banyak instansi dari satu pool sumber daya dengan isolasi per tenant (RBAC dan kebijakan akses per instansi). Public cloud menambahkan pool kapasitas untuk beban non sensitif. Karena pool di public cloud hanya berisi komponen stateless, risiko multi tenancy terhadap data sensitif dapat dihindari.

Rapid elasticity. Saat terjadi lonjakan, request yang tidak membutuhkan akses PII mentah dialihkan ke kapasitas di public cloud (cloud bursting), sedangkan database inti tidak ikut keluar. Dengan cara ini sistem tetap responsif saat beban memuncak, risiko downtime berkurang, dan kerahasiaan data tetap terjaga. Ketika beban turun, kapasitas tambahan dilepas kembali.

Measured service. Pemakaian tiap instansi diukur lewat rate limiting, kuota, dan audit log akses. Ini memudahkan deteksi akses anomali dan memungkinkan alokasi biaya kapasitas burst ke instansi pengguna.

## 2. Rekomendasikan Service Model
Kami merekomendasikan pendekatan multi-service model yang membagi model layanan sesuai kebutuhan spesifik tiap komponen sistem kependudukan:

Untuk database inti kependudukan, mesin biometrik, dan modul enkripsi (HSM), kami memilih Infrastructure as a Service (IaaS) di lingkungan private cloud. Komponen vital ini menyimpan data warga yang sangat rahasia, sehingga pemerintah wajib memegang kendali penuh hingga tingkat sistem operasi, konfigurasi kernel, dan isolasi fisik penyimpanan tanpa campur tangan lapisan abstraksi pihak ketiga.

Untuk lapisan microservices, API gateway verifikasi mitra, dan sistem antrean data, kami merekomendasikan Platform as a Service (PaaS). Model ini mempermudah tim pengembang dalam mengelola kontainer, load balancing, dan auto-scaling tanpa repot mengurus perangkat keras. Melalui PaaS, lapisan stateless ini dapat melakukan ekspansi kapasitas (cloud bursting) secara instan ke public cloud saat terjadi lonjakan akses pemilu atau pendaftaran sekolah.

Pada lapisan antarmuka pengguna, kami menerapkan Software as a Service (SaaS) untuk portal cek status KTP oleh warga serta dasbor kerja petugas Dukcapil daerah. Dengan model SaaS, ribuan instansi dan staf daerah cukup mengakses aplikasi siap pakai melalui peramban web yang diamankan dengan RBAC dan MFA, tanpa perlu melakukan instalasi, konfigurasi, maupun pemeliharaan perangkat lunak di perangkat lokal.

## 4. Alternatif yang ditolak
Public cloud murni unggul di rapid elasticity dan on-demand self-service, dan kami mengakui bahwa kebutuhan skalabilitas sistem ini terpenuhi dengan baik. Namun alternatif ini kurang tepat karena beberapa alasan;

Kedaulatan data dan yurisdiksi. Data yang disimpan di provider publik, terutama provider asing, dapat berada di bawah yurisdiksi hukum negara lain dan berpotensi berbenturan dengan aturan lokalisasi data bagi penyelenggara sistem elektronik lingkup publik. Pemerintah tidak dapat menjamin sepenuhnya bahwa data warga hanya tunduk pada hukum Indonesia.

Kendali infrastruktur terbatas. Dalam shared responsibility model, provider memegang lapisan fisik, hypervisor, dan operasional infrastrukturnya. Pemerintah tidak mengontrol siapa yang mengelola lapisan tersebut maupun bagaimana prosesnya diaudit.

Multi-tenancy pada data paling sensitif. Resource pooling di public cloud berarti sumber daya fisik dipakai bersama banyak pelanggan. Untuk data biasa risiko ini dapat diterima, tetapi untuk data kependudukan dan biometrik, risiko isolasi menjadi tidak baik dimiliki.

Dampak kebocoran yang permanen. Data biometrik tidak dapat diganti seperti password. Sekali bocor, dampaknya melekat pada warga seumur hidup.

Enkripsi tidak menyelesaikan semuanya. Enkripsi dan customer managed key memang memperkecil risiko, tetapi tidak menghilangkan masalah yurisdiksi dan keterbatasan kendali atas infrastruktur.

## Struktur Submission

```
tugas-09-cloud-delivery-deployment/
├── README.md      # Analisis lengkap (isi dengan poin 1-4 di atas)
├── JURNAL.md
└── bukti/          # (opsional) diagram pendukung
```

## Rubrik Penilaian (Tugas 9)

| Komponen | Bobot | Kriteria |
|---|---|---|
| Ketepatan rekomendasi deployment model | 30% | Argumen berbasis karakteristik NIST, bukan sekadar "private cloud lebih aman" tanpa detail |
| Ketepatan rekomendasi service model | 25% | Pemetaan komponen sistem ke IaaS/PaaS/SaaS masuk akal |
| Analisis risiko & mitigasi | 25% | Risiko spesifik ke konteks data kependudukan (bukan risiko generik) |
| Perbandingan dengan alternatif yang ditolak | 20% | Argumen penolakan jelas dan berdasar |

## Batasan Penggunaan AI (Level 2)

Kebijakan **Level 2 (AI Assisted Idea Generation & Structuring)** berlaku — lihat [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Boleh bertanya ke AI gambaran umum karakteristik NIST/deployment model untuk brainstorming; **tidak boleh** meminta AI menuliskan rekomendasi/analisis akhir yang tinggal ditempel ke `README.md`. Catat pemakaian AI di "Log Penggunaan AI" pada `JURNAL.md`.

- Jawaban yang terasa seperti "template" (bisa dipakai untuk sistem cloud apa saja tanpa menyebut spesifik kependudukan/data pribadi/regulasi) akan dinilai rendah pada komponen ketepatan rekomendasi.
- `README.md` wajib membahas minimal satu skenario tandingan yang kalian buat sendiri (mis. "bagaimana jika instansi daerah tidak punya infrastruktur private cloud sendiri?") beserta jawabannya.
