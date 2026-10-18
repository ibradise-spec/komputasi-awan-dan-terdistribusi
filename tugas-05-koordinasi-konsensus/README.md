# Tugas 5 (Pekan 5) — Koordinasi & Konsensus

**Materi terkait:** Physical/Logical Clock, Election Algorithm (Bully/Raft).

## Pemilihan bully algorithm vs raft
Dalam kasus ini, sistem membutuhkan satu node leader tunggal sebagai single source of truth untuk mengurutkan pesanan pusat (centralized order sequencing) agar tidak terjadi race condition atau pemroresan pesanan ganda akibat clock drift atau jam fisik antar server tidak sinkron.
Oleh karena itu, dengan adanya bully algorithm, terdapat algoritma yang sangat ringan yang diimplementasikan pada klaster kecil dengan topologi 5 node statis. Pemilihannya deterministik, node dengan ID tertinggi yang hidup pasti menang. Dalam konteks ini, dapat ditetapkan ID tertinggi pada server dengan spesifikasi hardware paling kuat untuk menjadi koordinator antrean.
Selain itu, tanpa perlu mekanisme randomized election timer atau voting quorum yang kompleks, node dengan ID tertinggi dapat langsung mendeklarasikan dirinya sebagai coordinator begitu mendeteksi ketiadaan node di atasnya.

## Trade off Bully algorithm vs Raft
Lonjakan jumlah pesan jaringan memiliki komplesiktas komputasi yang tinggi ketika node dengan ID terendah menjadi pihak pertama yang mendeteksi matinya node tertinggi, node terendah akan mengirimkan pesan ELECTION ke node atasnya hingga node tertinggi. Hal ini memicu efek berantai di mana node yang berada di atas node terendah akan memulai sesi election mereka sendiri secara bersamaan. Akibatnya, jaringan dibanjiri oleh pesan election dan ok yang saling tumpang tindih dengan kompleksitas mencapai O(N^2) pesan. Sebaliknya, Raft jauh lebih hemat bandwidth dengan kompleksitas O(N) karena menggunakan randomized election timeout, sehingga umumnya hanya satu kandidat yang aktif lebih dulu dan meminta voting ke node lain tanpa terjadinya pesan serentak.

Dalam jeda Single Point of Failure selama masa transisi leader dari leader lama hingga terpilihnya leader baru, Sistem akan mengalami kekosongan pemimpin. Berdasarkan code yang telah dibuat, jeda ini memakan waktu sekitar 5 deetik, akumulasi dari monitor_leader(3 detik) ditambah elction_timeout(2 detik) sebelum node selanjutnya maju menjadi COORDINATOR. Selama 5 detik ini, tidak adanya koordinator yang bisa mengurutkan pesanan masuk membuat layanan antrean FoodGo tetap mengalami downtime sementara atau penumpukan request.

Karena bully algorithm memenangkan ID tertinggi tanpa melihat riwayat kestabilan node, jika node tertinggi mengalami gangguan perangkat keras yang membuatnya hidup mati secara berulang, setiap kali node 5 menyala kembali ia akan langsung merebut posisi leader dari node 4. Perebutan kepemimpinan yang terus menerus ini akan mengacaukan pemroresan antrean pesan FoodGo. Pada algoritma Raft, node yang baru hidup kembali tidak bisa seenaknya merebut posisi leader selama leader saat ini masih rutin mengirimkan sinyal.

Bully algorithm hanya memilih pemimpin melalui ID tanpa memvalidasi kelengkapan data. Jika terjadi partisi jaringan yang membelah klaster FoodGO menjadi dua kubu terisolasi. Misal {node 1, node2} terputus dari {node 3, node 4}, maka node 2 dan 4 akan sama sama mengira node di atasnya mati dan mendeklarasikan diri sebagai leader di kubunya masing masing. Hal ini memicu munculnya dua leader aktif yang mencatatat urutan pesanan berbeda. Sebaliknya, Raft mencegah split brain dengan mewajibkan persetujuan kuorum mayoritas serta menjamin node yang terpilih sebagai leader adalah node yang memiliki catatan log pesanan paling update.

## 2 Skenario
# Skenario 1: Start Normal (Node 1–5 Dinyalakan)
Berdasarkan hasil pengujian terminal, terdapat dua pola menarik tergantung kecepatan eksekusi antar terminal:

Pola Konvergensi Bertahap (Sequential Start - Gambar Terminal Biru):

Saat node dinyalakan berurutan dari Node 1 hingga Node 5 dengan jeda waktu di atas ELECTION_TIMEOUT (2 detik), Node 1 yang belum melihat peer di atasnya sempat melakukan Broadcast COORDINATOR.
Begitu Node 2 menyala, ia mengambil alih kepemimpinan (Leader baru adalah Node 2), diikuti oleh Node 3, Node 4, dan akhirnya ketika Node 5 menyala, ia memeriksa higher_peers: {} (kosong) dan langsung melakukan Broadcast COORDINATOR. Seluruh Node (1–4) menerima pesan tersebut dan kompak mencatat: Leader baru adalah Node 5.

Pola Konvergensi Serentak (Concurrent Start - Gambar PowerShell Hitam):

Saat semua node aktif hampir bersamaan, Node 1, 2, 3, dan 4 mengirim pesan ELECTION ke ID yang lebih tinggi.
Node 2, 3, 4, dan 5 membalas OK ke pengirim di bawahnya (memicu ok_event.set()), sehingga Node 1–4 mencetak Menerima OK, menunggu COORDINATOR dan mengurungkan niat menjadi leader.
Node 5 tidak memiliki peer yang lebih tinggi ({}), sehingga langsung mendeklarasikan diri sebagai leader. Hasil akhir konsisten: Node 5 terpilih sebagai Leader.

# Skenario 2: Leader Mati & Re-Election (Node 5 Dimatikan dengan Ctrl+C)

Deteksi Kegagalan (Failure Detection):

Proses pada Node 5 dihentikan paksa (KeyboardInterrupt).
Thread monitor_leader() pada Node 1, 2, 3, dan 4 yang berjalan setiap time.sleep(3) detik mencoba mengirim pesan "PING" ke port 5005 milik Node 5.
Karena socket port 5005 sudah tertutup, send_message() mengembalikan False (ConnectionRefusedError), sehingga Node 1–4 mencetak: Leader Node 5 mati, election ulang.

Proses Pemilihan Ulang (Re-Election):

Node 1 mengirim ELECTION ke {2, 3, 4, 5}, Node 2 mengirim ke {3, 4, 5}, Node 3 mengirim ke {4, 5}, dan Node 4 mengirim ke {5}.   Node 1, 2, dan 3 menerima balasan OK dari node di atasnya yang masih hidup (Node 2, 3, dan 4), sehingga mereka berhenti dan menunggu pesan COORDINATOR.
Node 4 hanya mengirim ELECTION ke {5: 5005}. Karena Node 5 sudah mati, Node 4 tidak menerima balasan OK hingga batas ELECTION_TIMEOUT (2.0 detik) habis.

Hasil Akhir:

Setelah timeout terlewati, Node 4 memanggil declare_leader(), mencetak node 4 Broadcast COORDINATOR, saya jadi leader, dan mengirimkan pesan tersebut ke seluruh peer.
Node 1, 2, dan 3 menerima pesan tersebut dan memperbarui status mereka menjadi: Leader baru adalah Node 4. Sistem FoodGo berhasil pulih secara otomatis (self-healing coordination).

## Studi Kasus

Terjadi konflik urutan waktu pada pesanan FoodGo (dua server mencatat urutan pesanan berbeda karena jam tidak sinkron), dan sistem membutuhkan satu **"Node Leader"** untuk mengelola antrean pesanan pusat agar tidak terjadi konflik pemrosesan ganda.

## Tugas Kelompok

Implementasikan simulasi **Bully Algorithm** untuk memilih leader di antara **5 node virtual** yang berjalan sebagai 5 proses Python terpisah di laptop yang sama (tiap node = satu proses di port berbeda, komunikasi lewat TCP socket di `localhost`).

Skeleton yang disediakan (`src/node.py`) sudah menangani bagian **infrastruktur jaringan** (membuka socket, menerima & mengirim pesan antar node) — bagian **algoritma Bully sendiri sengaja dikosongkan** (`# TODO`), karena itu inti pembelajaran tugas ini.

### Aturan Bully Algorithm yang harus diimplementasikan

1. Node yang mendeteksi leader tidak merespons (atau saat start pertama kali) mengirim pesan `ELECTION` ke semua node dengan ID **lebih besar** darinya.
2. Jika ada node ber-ID lebih besar yang merespons `OK`, node yang memulai election **berhenti mencalonkan diri** dan menunggu pesan `COORDINATOR`.
3. Jika **tidak ada** node ber-ID lebih besar yang merespons dalam batas waktu tertentu, node tersebut menjadi leader dan mem-broadcast `COORDINATOR` ke semua node lain.
4. Semua node mencatat siapa leader saat ini.

### Cara Menjalankan

Buka 5 terminal terpisah (satu per node):
```bash
python3 src/node.py --id 1 --port 5001 --peers 5002,5003,5004,5005
python3 src/node.py --id 2 --port 5002 --peers 5001,5003,5004,5005
python3 src/node.py --id 3 --port 5003 --peers 5001,5002,5004,5005
python3 src/node.py --id 4 --port 5004 --peers 5001,5002,5003,5005
python3 src/node.py --id 5 --port 5005 --peers 5001,5002,5003,5004
```

### Skenario Wajib Diuji & Dicatat

1. **Start normal**: nyalakan node 1–5 hampir bersamaan, catat siapa yang terpilih jadi leader (harusnya node ber-ID tertinggi, yaitu node 5).
2. **Leader mati**: matikan (Ctrl+C) proses node leader (node 5), amati node lain mendeteksi leader hilang dan memicu election baru. Catat leader baru yang terpilih (harusnya node 4).
3. Simpan log terminal (screenshot atau `> log_nodeX.txt` redirect) dari kedua skenario ke folder `bukti/`.

## Struktur Submission

```
tugas-05-koordinasi-konsensus/
├── README.md      # Analisis: kenapa perlu leader, kenapa Bully (vs Raft), hasil 2 skenario
├── JURNAL.md
├── src/
│   └── node.py
└── bukti/          # Log/screenshot skenario start normal & leader mati
```

## Rubrik Penilaian (Tugas 5)

| Komponen | Bobot | Kriteria |
|---|---|---|
| Implementasi Bully Algorithm benar | 35% | Election, OK, COORDINATOR message bekerja sesuai aturan algoritma |
| Bukti skenario leader mati → re-election | 30% | Log jelas menunjukkan leader baru terpilih otomatis |
| Analisis (kenapa perlu leader, trade-off Bully vs Raft) | 20% | Dikaitkan ke masalah urutan pesanan di skenario FoodGo |
| Proses & kontribusi kelompok | 15% | `JURNAL.md`, commit history |

## Batasan Penggunaan AI (Level 2)

Kebijakan **Level 2 (AI Assisted Idea Generation & Structuring)** berlaku — lihat [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Boleh bertanya ke AI tentang gambaran umum algoritma election; **tidak boleh** meminta AI menuliskan isi `# TODO` di `src/node.py` (logika `on_message`, `start_election`, `declare_leader`, `monitor_leader`). Catat pemakaian AI di "Log Penggunaan AI" pada `JURNAL.md`.

- `README.md` wajib menjelaskan kenapa Bully Algorithm selalu memilih node ber-ID tertinggi yang masih hidup, dan apa kelemahannya dibanding algoritma lain (mis. jumlah pesan yang dikirim saat election, single point of failure sebelum leader baru terpilih) — bukan sekadar definisi generik.
