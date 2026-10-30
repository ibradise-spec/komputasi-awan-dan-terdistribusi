"""
Tugas 6 - Simulasi Chord DHT (single-process, tanpa jaringan sungguhan)
 
Fungsi hashing & struktur data ring sudah disediakan.
Lengkapi TODO untuk lookup(), join(), dan leave().
"""
 
import hashlib
 
M_BITS = 8               # ruang identifier 0..255 (disederhanakan dari Chord asli yang pakai 160-bit)
RING_SIZE = 2 ** M_BITS
 
 
def hash_id(key: str) -> int:
    """Hash string (ID node atau ID kurir) ke ruang identifier 0..RING_SIZE-1."""
    digest = hashlib.sha1(key.encode()).digest()
    return int.from_bytes(digest, "big") % RING_SIZE
 
 
class ChordRing:
    def __init__(self):
        # node_id (hasil hash) -> alamat IP node tersebut
        self.nodes: dict[int, str] = {}
        # key kurir (hasil hash) -> IP kurir yang disimpan node yang bertanggung jawab
        self.data: dict[int, tuple[str, str]] = {}  # hash -> (kurir_id, ip_kurir)
        # (tambahan) key (hash) -> node_id yang saat ini bertanggung jawab.
        # Dipakai supaya perpindahan tanggung jawab benar-benar tercatat & bisa dibuktikan.
        self.owner: dict[int, int] = {}
        # (tambahan) node_id -> nama node, untuk log yang mudah dibaca
        self.names: dict[int, str] = {}
 
    # ------------------------------------------------------------------
    # Helper tampilan
    # ------------------------------------------------------------------
    def _label(self, node_id: int) -> str:
        return f"{self.names.get(node_id, '?')}(id={node_id})"
 
    def print_ring(self, title: str = "Kondisi ring"):
        """Cetak node berurutan melingkar beserta key yang dipegang tiap node."""
        print(f"\n[{title}]")
        for nid in sorted(self.nodes):
            keys = sorted(k for k, o in self.owner.items() if o == nid)
            isi = ", ".join(f"{self.data[k][0]}(h={k})" for k in keys) or "-"
            print(f"  {self._label(nid):<28} ip={self.nodes[nid]:<10} menyimpan: {isi}")
 
    # ------------------------------------------------------------------
    # Operasi inti
    # ------------------------------------------------------------------
    def join(self, node_name: str, node_ip: str):
        """Tambahkan node baru ke ring. Pindahkan data yang seharusnya
        menjadi tanggung jawab node baru ini dari successor lamanya."""
        node_id = hash_id(node_name)
 
        if node_id in self.nodes:
            print(f"[JOIN] GAGAL: hash '{node_name}' (id={node_id}) bentrok dengan "
                  f"{self._label(node_id)}. Gunakan nama node lain.")
            return
 
        # TODO 2: successor LAMA dicari SEBELUM node baru dimasukkan ke self.nodes
        # (otomatis "node_id ini dikecualikan").
        old_succ = self.find_successor(node_id) if self.nodes else None
 
        # TODO 1: tambahkan node_id -> node_ip ke self.nodes.
        self.nodes[node_id] = node_ip
        self.names[node_id] = node_name
        print(f"[JOIN] Node '{node_name}' (id={node_id}) bergabung, alamat {node_ip}")
 
        # TODO 3: pindahkan key yang sekarang jatuh ke node baru dari successor lama.
        # Dicek ulang dengan find_successor() supaya kasus wrap-around ikut benar.
        if old_succ is None:
            print("       Ring tadinya kosong, belum ada key yang dipindah.")
            return
 
        moved = False
        for key_hash in sorted(self.owner):
            if self.owner[key_hash] == old_succ and self.find_successor(key_hash) == node_id:
                self.owner[key_hash] = node_id
                print(f"       Key {self.data[key_hash][0]} (h={key_hash}) pindah: "
                      f"{self._label(old_succ)} -> {self._label(node_id)}")
                moved = True
        if not moved:
            print(f"       Tidak ada key yang berpindah (successor lama: {self._label(old_succ)}).")
 
    def leave(self, node_name: str):
        """Keluarkan sebuah node dari ring. Data yang dipegangnya harus
        berpindah ke successor-nya."""
        node_id = hash_id(node_name)
 
        if node_id not in self.nodes:
            print(f"[LEAVE] GAGAL: node '{node_name}' (id={node_id}) tidak ada di ring.")
            return
 
        print(f"[LEAVE] Node '{node_name}' (id={node_id}) keluar dari ring")
 
        # TODO 4: hapus node_id dari self.nodes.
        del self.nodes[node_id]
        leaving_label = f"{node_name}(id={node_id})"
        self.names.pop(node_id, None)
 
        # TODO 5: cari successor BARU untuk tiap key milik node ini, lalu pindahkan.
        keys = sorted(k for k, o in self.owner.items() if o == node_id)
        if not keys:
            print("        Node tidak memegang key apa pun.")
            return
 
        if not self.nodes:
            print("        Ring kosong: semua key hilang (tidak ada successor).")
            for k in keys:
                del self.owner[k]
                del self.data[k]
            return
 
        for key_hash in keys:
            new_owner = self.find_successor(key_hash)
            self.owner[key_hash] = new_owner
            print(f"        Key {self.data[key_hash][0]} (h={key_hash}) pindah: "
                  f"{leaving_label} -> {self._label(new_owner)}")
 
    def find_successor(self, key_hash: int) -> int:
        """Cari node_id dengan nilai hash TERKECIL yang >= key_hash
        (successor menurut aturan Chord). Jika tidak ada, wrap-around
        ke node dengan hash terkecil di ring (karena ring melingkar)."""
        # TODO 6
        if not self.nodes:
            raise RuntimeError("Ring kosong: tidak ada node.")
        ids = sorted(self.nodes.keys())
        for nid in ids:
            if nid >= key_hash:
                return nid
        return ids[0]  # wrap-around
 
    def register_kurir(self, kurir_id: str, ip_kurir: str):
        """Simpan mapping ID Kurir -> IP di node yang bertanggung jawab."""
        key_hash = hash_id(kurir_id)
        # TODO 7
        node_id = self.find_successor(key_hash)
        self.data[key_hash] = (kurir_id, ip_kurir)
        self.owner[key_hash] = node_id
        print(f"[REGISTER] {kurir_id} (h={key_hash}) -> {ip_kurir}, "
              f"disimpan di {self._label(node_id)}")
 
    def lookup(self, kurir_id: str) -> str | None:
        """Cari alamat IP terkini untuk sebuah ID Kurir."""
        key_hash = hash_id(kurir_id)
        # TODO 8
        if not self.nodes:
            return None
        node_id = self.find_successor(key_hash)
        # Data hanya valid jika node penanggung jawab memang memegangnya.
        if self.owner.get(key_hash) == node_id and key_hash in self.data:
            return self.data[key_hash][1]
        return None
 
    def lookup_verbose(self, kurir_id: str):
        """Lookup + cetak node penanggung jawab (untuk bukti di bukti/)."""
        key_hash = hash_id(kurir_id)
        node_id = self.find_successor(key_hash)
        ip = self.lookup(kurir_id)
        print(f"  {kurir_id} (h={key_hash}) -> {self._label(node_id)} -> {ip}")
 
 
def main():
    ring = ChordRing()
 
    # Skenario awal: 4 node bergabung
    ring.join("node-jakarta-1", "10.0.0.1")
    ring.join("node-jakarta-2", "10.0.0.2")
    ring.join("node-bandung-1", "10.0.0.3")
    ring.join("node-surabaya-1", "10.0.0.4")
 
    # Daftarkan beberapa kurir
    print()
    ring.register_kurir("kurir-001", "192.168.1.10")
    ring.register_kurir("kurir-002", "192.168.1.11")
    ring.register_kurir("kurir-003", "192.168.1.12")
    ring.register_kurir("kurir-006", "192.168.1.15")  # h=217 > semua node -> wrap-around
 
    ring.print_ring("Ring awal (4 node)")
 
    print("\n--- Lookup sebelum perubahan topologi ---")
    ring.lookup_verbose("kurir-001")
    ring.lookup_verbose("kurir-002")
    ring.lookup_verbose("kurir-003")
    ring.lookup_verbose("kurir-006")  # uji wrap-around
 
    print("\n--- Node baru bergabung ---")
    ring.join("node-makassar-1", "10.0.0.5")
    ring.print_ring("Ring setelah join node-makassar-1")
    ring.lookup_verbose("kurir-001")
    ring.lookup_verbose("kurir-003")
 
    print("\n--- Sebuah node keluar ---")
    ring.leave("node-surabaya-1")
    ring.print_ring("Ring setelah leave node-surabaya-1")
    ring.lookup_verbose("kurir-001")
    ring.lookup_verbose("kurir-002")
    ring.lookup_verbose("kurir-003")
    ring.lookup_verbose("kurir-006")
 
    print("\n--- IP kurir berubah (update mapping) ---")
    ring.register_kurir("kurir-001", "172.16.5.77")
    ring.lookup_verbose("kurir-001")
 
 
if __name__ == "__main__":
    main()
 
