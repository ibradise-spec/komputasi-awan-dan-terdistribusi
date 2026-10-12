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


|...|...|...|...|

| 11-10-2026 | claude | aku mau membuat modul pembayaran yaitu server.py dan pemesanan client.py RPC memakai xmlrpc python berdasarkan skeleton yang aku dapat. apa itu xmlrpc? tolong jelaskan saja apa yang diminta dari TODO" di skeleton. tolong contoh code nya saja yang bisa dipke
ini skeleton nya: 

client.py: 
    # TODO 1: buat ServerProxy ke http://localhost:8000
    proxy = None  # ganti dengan xmlrpc.client.ServerProxy(...)

    print("Memanggil cek_saldo('user1') ... menunggu respons sinkron")
    start = time.time()
    # TODO 2: panggil proxy.cek_saldo("user1") dan cetak hasilnya + waktu tempuh
    #         (buktikan client BENAR-BENAR menunggu sampai server membalas)

    print("Memanggil proses_pembayaran('user1', 20000) ...")
    # TODO 3: panggil proxy.proses_pembayaran("user1", 20000) dan cetak hasilnya

server.py: 

def cek_saldo(user_id: str) -> float:
    """Kembalikan saldo user_id saat ini."""
    # TODO 1: kembalikan saldo dari dict `saldo_user`.
    # Jika user_id tidak ada, putuskan sendiri perilakunya (mis. return 0 atau raise error)
    # dan jelaskan keputusan ini di README.md.
    pass


def proses_pembayaran(user_id: str, jumlah: float) -> dict:
    """Kurangi saldo user sejumlah `jumlah`. Kembalikan status hasil."""
    # TODO 2: validasi saldo cukup, kurangi saldo_user[user_id], dan kembalikan
    # dict berisi minimal {"status": "sukses"/"gagal", "saldo_akhir": ...}
    pass


def main():
    # TODO 3: buat SimpleXMLRPCServer di localhost port 8000,
    # daftarkan fungsi cek_saldo & proses_pembayaran, lalu serve_forever().
    server = SimpleXMLRPCServer(("localhost", 8000))
    print("RPC server modul Pembayaran berjalan di port 8000...")
    server.serve_forever()|Apa itu XML-RPC?

XML-RPC adalah protokol Remote Procedure Call yang mengirim pemanggilan fungsi lewat HTTP, dengan isi permintaan/respons berformat XML. Client memanggil fungsi yang ada di server seolah-olah fungsi lokal (proxy.cek_saldo("user1")), padahal eksekusinya terjadi di proses/mesin lain.

Karakteristik pentingnya:

Sinkron: client berhenti (blocking) sampai server membalas. Ini yang diminta dibuktikan di TODO 2 client.
Transport: HTTP POST, jadi mudah dipakai dan lintas bahasa.
Pustaka standar Python: xmlrpc.server (server) dan xmlrpc.client (client), tanpa instalasi tambahan.
Tipe data terbatas: int, float, string, bool, list, dict, dll. Karena itu proses_pembayaran mengembalikan dict.
Penjelasan TODO di server.py
TODO	Yang diminta	Penjelasan
TODO 1 cek_saldo	Kembalikan saldo dari dict saldo_user	Ambil saldo_user[user_id]. Kamu harus memutuskan sendiri perilaku jika user_id tidak ada: return 0 (diam-diam) atau raise error (lebih tegas, di XML-RPC akan sampai ke client sebagai Fault). Keputusan ini wajib dijelaskan di README.md.
TODO 2 proses_pembayaran	Validasi, kurangi saldo, kembalikan status	Cek apakah saldo cukup (dan idealnya jumlah > 0 serta user ada). Jika cukup, kurangi saldo_user[user_id] lalu return {"status": "sukses", "saldo_akhir": ...}. Jika tidak, return {"status": "gagal", "saldo_akhir": ...} tanpa mengubah saldo.
TODO 3 main	Buat server, daftarkan fungsi, jalankan	Bagian SimpleXMLRPCServer(("localhost", 8000)) dan serve_forever() sudah ada. Yang kurang: mendaftarkan kedua fungsi dengan server.register_function(cek_saldo) dan server.register_function(proses_pembayaran) sebelum serve_forever(). Tanpa registrasi, client tidak bisa memanggilnya.

Catatan: saldo_user (dict) harus didefinisikan di level modul, di atas fungsi.

Penjelasan TODO di client.py
TODO	Yang diminta	Penjelasan
TODO 1	Buat ServerProxy	Isi proxy dengan xmlrpc.client.ServerProxy("http://localhost:8000"). Objek ini yang membuat proxy.nama_fungsi(...) diteruskan ke server.
TODO 2	Panggil cek_saldo, cetak hasil dan waktu tempuh	Simpan hasil proxy.cek_saldo("user1"), hitung time.time() - start, lalu cetak keduanya. start sudah disediakan. Untuk membuktikan sinkron, tambahkan time.sleep(...) di server (mis. 2 detik di cek_saldo); waktu tempuh di client akan ≥ 2 detik, artinya client benar-benar menunggu.
TODO 3	Panggil proses_pembayaran	Panggil proxy.proses_pembayaran("user1", 20000) dan cetak dict hasilnya (status dan saldo akhir).
Urutan menjalankan
Jalankan server.py di terminal pertama (biarkan berjalan).
Jalankan client.py di terminal kedua. | # TODO 1: buat ServerProxy ke http://localhost:8000
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000")

    print("Memanggil cek_saldo('user1') ... menunggu respons sinkron")
    start = time.time()

    # TODO 2: panggil proxy.cek_saldo("user1") dan cetak hasilnya + waktu tempuh
    #         (buktikan client BENAR-BENAR menunggu sampai server membalas)
    saldo = proxy.cek_saldo("user1")
    waktu_tempuh = time.time() - start

    print("Saldo user1:", saldo)
    print(f"Waktu respons: {waktu_tempuh:.4f} detik")

    print("Memanggil proses_pembayaran('user1', 20000) ...")

    # TODO 3: panggil proxy.proses_pembayaran("user1", 20000) dan cetak hasilnya
    hasil = proxy.proses_pembayaran("user1", 20000)
    print("Hasil pembayaran:", hasil)

def cek_saldo(user_id: str) -> float:
    """Kembalikan saldo user_id saat ini."""
    # TODO 1: kembalikan saldo dari dict saldo_user.
    # Jika user_id tidak ada, putuskan sendiri perilakunya (mis. return 0 atau raise error)
    # dan jelaskan keputusan ini di README.md.
    return saldo_user.get(user_id, 0)


def proses_pembayaran(user_id: str, jumlah: float) -> dict:
    """Kurangi saldo user sejumlah jumlah. Kembalikan status hasil."""
    # TODO 2: validasi saldo cukup, kurangi saldo_user[user_id], dan kembalikan
    # dict berisi minimal {"status": "sukses"/"gagal", "saldo_akhir": ...}

    if user_id not in saldo_user:
        return {"status": "gagal", "saldo_akhir": 0}

    if jumlah <= 0 or saldo_user[user_id] < jumlah:
        return {
            "status": "gagal",
            "saldo_akhir": saldo_user[user_id]
        }

    saldo_user[user_id] -= jumlah

    return {
        "status": "sukses",
        "saldo_akhir": saldo_user[user_id]
    }


def main():
    # TODO 3: buat SimpleXMLRPCServer di localhost port 8000,
    # daftarkan fungsi cek_saldo & proses_pembayaran, lalu serve_forever().
    server = SimpleXMLRPCServer(("localhost", 8000))
    server.register_function(cek_saldo, "cek_saldo")
    server.register_function(proses_pembayaran, "proses_pembayaran")

    print("RPC server modul Pembayaran berjalan di port 8000...")
    server.serve_forever() |
| 11-10-2026 | Chatgpt | apa itu rabbit mqdan apa sih hubungannya dengan biasanya consumer.py dan publisher.py, kasih contoh sekalian jelaskan hubungannya dong| memberikan penjelasan sekaligus memberikan contoh implementasi  | mengisi todo pada folder mq |
