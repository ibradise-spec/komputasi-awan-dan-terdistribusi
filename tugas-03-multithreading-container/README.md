analisis

DI program FoodGo setiap pesanan awalnya dianggap diproses menggunakan proses OS baru. Kalau jumlah pesanan nya tambah banyak, proses seperti ini akan perlu resource yang lebih besar karena setiap proses punyai overhead dan ruang memorinya sendiri. Jika banyak pesanan masuk secara bersamaan kondisi tersebut bisa membuat penggunaan resource server menjadi berlebihan.

Karena itu, pada simulasi ini digunakan multithreading. Beberapa pesanan dapat diproses secara bersamaan menggunakan beberapa thread yang berada dalam satu proses. Thread juga dapat menggunakan data yang sama sehingga lebih ringan dibandingkan membuat proses OS baru untuk setiap pesanan. Pada program ini digunakan 10 thread untuk memproses 100 pesanan.

Tapi penggunaan thread yang berbagi data juga menimbulkan masalah berupa race condition. Pada program ini beberapa thread mengakses dan mengubah variabel processed_count yang sama. Jika dua atau lebih thread melakukan perubahan pada waktu yang hampir bersamaan, salah satu perubahan dapat tertimpa oleh perubahan thread lainnya.

Hal ini dibuktikan pada percobaan tanpa Lock. Dari 100 pesanan yang diproses nilai processed_count yang diperoleh hanya 35. Seharusnya nilai nya mencapai 100. Perbedaan hasil ini menunjukkan bahwa terjadi race condition karena beberapa pembaruan pada counter tidak tercatat dengan benar.

Untuk memperbaiki masalah ini maka digunakan threading.Lock(). Lock digunakan untuk membatasi akses ke bagian yang mengubah processed_count, sehingga hanya satu thread yang bisa melakukan perubahan pada satu waktu. Thread lainnya harus menunggu sampai proses tersebut selesai. Setelah menggunakan Lock, hasil processed_count menjadi 100 dari 100 pesanan.

Dari percobaan tersebut dapat dilihat bahwa multithreading lebih sesuai digunakan pada simulasi ini dibandingkan membuat proses OS baru untuk setiap pesanan. Thread dapat bekerja secara bersamaan menggunakan beberapa thread dalam satu proses dan menggunakan data bersama, tetapi data yang dipake bersama harus dilindungi agar tidak terjadi race condition. Penggunaan Lock berhasil membuat hasil perhitungan counter kembali sesuai dengan jumlah pesanan yang diproses.
