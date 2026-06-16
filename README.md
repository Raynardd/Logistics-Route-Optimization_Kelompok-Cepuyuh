# Logistics Route Optimization: Heuristic vs Exact Algorithm Simulation

Repositori ini berisi simulasi komparasi arsitektur algoritma pencarian rute (*Last-Mile Delivery*) untuk menentukan keputusan bisnis terkait infrastruktur teknologi perusahaan ekspedisi. Kami membandingkan algoritma **Greedy (Heuristik)** dan **Dynamic Programming Held-Karp (Eksak)** berdasarkan *Total Cost of Ownership* (TCO) yang mencakup biaya komputasi server awan dan biaya operasional bahan bakar minyak (BBM) dinamis.

---

## Tim Pengembang
* **Sammy Farrel Zebua (140810240016)** — *Data & Integration Engineer* (Pemodelan Matriks & Ekstraksi Data Gmaps)
* **Tristan Bonardo Silalahi (140810240058)** — *Logic & Heuristic Engineer* (Implementasi Greedy & Fungsi Biaya Dinamis)
* **Laudzan Ananda Syawaliandi (140810240050)** — *Optimization Engineer* (Implementasi DP Held-Karp & Integrasi CLI)
* **Vincentius Raynard Thedy (140810240028)** — *QA, Analyst & Git Manager* (Analisis Kompleksitas, Metrik Finansial, & Dokumentasi)

---

## 1. Timeline Pengerjaan Proyek

Berikut adalah alur waktu pengerjaan proyek oleh tim kami:

| Tanggal | Target Pekerjaan |
| :--- | :--- |
| **Selasa, 16 Juni 2026** | <ul><li>`README.md` (Pemilihan Algoritma)</li></ul> |
| **Rabu, 17 Juni 2026** | <ul><li>Pemodelan data (Format CSV terpisah untuk matriks jarak dan beban paket)</li><li>Implementasi Algoritma Heuristik dan Eksak</li></ul> |
| **Kamis, 18 Juni 2026** | <ul><li>Menggabungkan semua pekerjaan (Algoritma Heuristik dan Eksak)</li><li>*Finishing* `README.md`</li></ul> |

---

## 2. Cara Menjalankan Program

Pastikan sistem Anda menggunakan minimal **Python 3.8**. Dataset (*nodes*, beban paket, dan matriks jarak) akan dibaca secara otomatis dari direktori `data/` dalam format `.csv`.

Untuk menjalankan simulasi, gunakan *Command Line Interface* (CLI) berikut di terminal:

**Menjalankan Skenario Subsidi (Harga BBM Rp 5.000/liter):**
> `python src/main.py --scenario subsidi`

**Menjalankan Skenario Krisis (Harga BBM Rp 20.000/liter):**
> `python src/main.py --scenario krisis`

*(Catatan: Anda juga bisa menggunakan argumen `--scenario all` untuk menjalankan dan membandingkan kedua skenario sekaligus secara berdampingan).*

---

## 3. Pemilihan Algoritma & Trade-Off

Dalam simulasi ini, kami memilih dua pendekatan algoritma yang bertolak belakang untuk memperlihatkan *trade-off* antara kecepatan eksekusi komputasi dan optimalitas jarak rute:

### A. Algoritma Heuristik (Greedy)
Kami mengimplementasikan algoritma **Greedy** murni. Pada setiap *node*, kurir akan selalu memilih lokasi pelanggan terdekat berikutnya yang belum dikunjungi tanpa memikirkan konsekuensi jarak rute setelahnya.
*   **Kelebihan:** Sangat ringan dan secepat kilat. Biaya *Cloud Server* (berbasis eksekusi per milidetik) hampir mendekati angka nol.
*   **Trade-off:** Sering terjebak dalam *local optimum*. Hasil rute akhir biasanya sub-optimal dan zigzag. Hal ini menyebabkan jarak tempuh total memanjang dan konsumsi BBM menjadi sangat boros, terutama pada awal rute saat beban paket masih penuh.

### B. Algoritma Eksak (Dynamic Programming - Held-Karp)
Sebagai algoritma penentu rute absolut, kami mengimplementasikan **DP Held-Karp** dengan *Memoization*. Algoritma ini memecah graf menjadi sub-masalah dengan mengingat rute terpendek untuk sebuah *subset node* yang sudah dikunjungi.
*   **Kelebihan:** Dijamin 100% menghasilkan rute paling efisien secara matematis dan menekan pengeluaran BBM semaksimal mungkin.
*   **Trade-off:** Sangat boros *resource* komputasi. Waktu eksekusinya bertumbuh secara eksponensial seiring bertambahnya *node* pelanggan, yang akan memicu lonjakan tagihan *Cloud Server Pay-as-you-go*. Metode ini juga memakan memori (RAM) tinggi karena harus menyimpan berbagai status/percabangan di dalam *tabel memori* DP.

---

## 4. Analisis Kompleksitas (Big-O)

Berdasarkan penelusuran struktur rekursif dan iterasi *loop* pada *source code* utama kami, berikut adalah analisis teoritis untuk metrik ruang dan waktu:

*   **Greedy Algorithm (Heuristik)**
    *   **Kompleksitas Waktu:** $O(n^2)$
        Pada graf dengan $n$ titik lokasi, algoritma harus melakukan iterasi dari titik saat ini ke maksimal $(n-1)$ *node* tetangga untuk mencari titik terdekat. Proses seleksi ini diulang sebanyak $n$ kali sampai seluruh *node* pelanggan dikunjungi.
    *   **Kompleksitas Ruang (Memori):** $O(n)$
        Algoritma ini beroperasi secara *in-place* dan hanya membutuhkan ruang memori ekstra minimum untuk menyimpan struktur data *array* (sebagai penanda *node* mana saja yang sudah dilewati).

*   **DP Held-Karp (Eksak)**
    *   **Kompleksitas Waktu:** $O(n^2 \cdot 2^n)$
        Algoritma mengevaluasi $2^n$ kemungkinan *subset node*. Untuk setiap kombinasi *subset*, program akan melakukan iterasi pada $n$ *node* terakhir yang dikunjungi dan mencari *node* perantara sebelumnya. Meskipun jauh lebih optimal daripada $O(n!)$ milik algoritma *Backtracking* murni, waktu eksekusinya tetap berada di ranah eksponensial.
    *   **Kompleksitas Ruang (Memori):** $O(n \cdot 2^n)$
        Penggunaan ruang sangat masif karena program bergantung pada *memoization table*. Tabel ini diwajibkan menyimpan nilai jarak minimum untuk setiap kemungkinan status kombinasi (*subset node* yang dikunjungi, *node* terakhir yang disinggahi).

---

## 5. Summary & Keputusan Bisnis

Berdasarkan hasil eksekusi simulasi kami pada dua kondisi ekonomi yang berbeda, arsitektur algoritma logistik harus diputuskan secara dinamis mengikuti fluktuasi harga bahan bakar:

1.  **Skenario Subsidi (Rp 5.000/liter):** Algoritma **Greedy** adalah pilihan paling logis. Penghematan bensin dari rute optimal DP Held-Karp tidak mampu menutupi mahalnya biaya tagihan *Cloud Server* yang meroket hingga mencapai **[Rp blablablabla]**.
2.  **Skenario Krisis (Rp 20.000/liter):** Algoritma **Eksak (DP Held-Karp)** terbukti berbalik menguntungkan. Kerugian akibat melonjaknya biaya komputasi server sebesar **[Rp blablablabla]** berhasil dikompensasi dengan sukses oleh penghematan BBM signifikan yang mencapai **[Rp blablablabla]**.

**Titik Break-Even (BEP):** Dari analisis perhitungan *Total Cost of Ownership* (TCO), implementasi algoritma DP Held-Karp baru masuk akal secara finansial dan menguntungkan untuk di-*deploy* di server produksi ketika harga BBM telah menyentuh batas **[Rp blablablabla] per liter**. Selama harga BBM masih berada di bawah nominal tersebut, manajemen disarankan untuk tetap menggunakan algoritma Heuristik.