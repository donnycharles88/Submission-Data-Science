# Submission-Data-Science
------

# 📊 Proyek Akhir: Perusahaan Edutech - Jaya Jaya Institut

## 🎯 Business Understanding

Jaya Jaya Institut merupakan institusi pendidikan tinggi yang telah berdiri sejak tahun 2000 dengan reputasi akademik yang baik. Namun, institusi ini menghadapi tantangan serius berupa tingginya angka putus studi (dropout) mahasiswa, mencapai 32.1% dari total 4.424 data mahasiswa. Tingginya angka dropout tidak hanya berdampak pada reputasi institusi, tetapi juga mengindikasikan inefisiensi dalam alokasi sumber daya pendampingan akademik. Jaya Jaya Institut membutuhkan pendekatan berbasis data untuk mendeteksi mahasiswa berisiko sejak dini agar dapat diberikan intervensi yang tepat sebelum memutuskan keluar dari perkuliahan.


### Permasalahan Bisnis

Berdasarkan kondisi tersebut, permasalahan bisnis yang perlu diselesaikan adalah:

1. Apakah tingginya angka dropout mahasiswa mengganggu target kelulusan institusi?
2. Bagaimana cara mendeteksi mahasiswa yang berisiko dropout sejak dini sebelum mereka memutuskan keluar?
3. Faktor-faktor apa saja yang paling berpengaruh terhadap keputusan mahasiswa untuk dropout atau melanjutkan studi?
4. Program studi mana saja yang memiliki tingkat dropout tertinggi dan memerlukan perhatian khusus?
5. Bagaimana cara mengalokasikan sumber daya bimbingan akademik secara efektif kepada mahasiswa yang paling membutuhkan?
6. Apakah performa akademik di semester awal (semester 1 dan 2) dapat menjadi indikator yang reliable untuk memprediksi kelulusan mahasiswa?
7. Bagaimana cara memonitor dan mengevaluasi efektivitas program pencegahan dropout yang telah diterapkan?



### Cakupan Proyek

- Exploratory Data Analysis (EDA) untuk memahami pola akademik, demografi, dan hubungan antar variabel pada data mahasiswa
- Identifikasi faktor dominan yang mempengaruhi status kelulusan (Dropout, Enrolled, Graduate) melalui analisis statistik dan feature importance
- Pembangunan model klasifikasi Machine Learning (Logistic Regression, Random Forest, Gradient Boosting) dengan Random Forest terpilih sebagai model utama
- **Pengembangan prototype aplikasi web (`app.py`) menggunakan Streamlit untuk prediksi status mahasiswa baru secara real-time**
- Pembuatan business dashboard interaktif menggunakan **Metabase** untuk monitoring performa akademik dan tingkat kelulusan per program studi
- Rekomendasi actionable berbasis data untuk strategi intervensi dini dan peningkatan retensi mahasiswa

**Batasan Proyek:**
- Data yang digunakan terbatas pada 4.424 record mahasiswa dari institusi pendidikan tinggi
- Model difokuskan pada prediksi multi-kelas: Dropout, Currently Enrolled, dan Graduate
- Dashboard Metabase dijalankan secara lokal menggunakan Docker, sedangkan prototype ML di-deploy ke Streamlit Community Cloud
- Akurasi model (~75%) masih dapat ditingkatkan dengan penambahan fitur non-akademik (seperti kesehatan mental, keterlibatan organisasi kampus, dll.) yang tidak tersedia dalam dataset saat ini

---

### Persiapan
**Spesifikasi Environment:**
- **Python**: `Python 3.13.7` 
- **Metabase**: `v0.59.6.3` 

**Sumber Data**
- **File**: [data.csv](<data.csv>)
- **Jumlah Record**: 4.424 mahasiswa
- **Jumlah Fitur**: 37 variabel
- **Target Variable**: 'Status' (Dropout / Enrolled / Graduate)
- **Format**: CSV dengan separator ;

**Setup Environment**

```bash
# 1. Ekstraksi Folder Zip
cd Edutech

# 2. Buat virtual environment (direkomendasikan)
python -m venv venv
# Aktifkan environment
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Jalankan Jupyter Notebook
jupyter notebook .
```

**Setup Metabase (Dashboard)**
Dashboard telah dikonfigurasi sebelumnya dan database-nya disimpan dalam file `metabase.db.mv.db`. Ikuti langkah berikut untuk menjalankannya:
```bash
# Pull dan jalankan Metabase dengan Docker
docker pull metabase/metabase:latest
docker run -d -p 3000:3000 --name metabase metabase/metabase:v0.59.5.2
```
```
Akses dashboard di: http://localhost:3000
Username: root@mail.com
Password: root123
```
---
## 📊 Business Dashboard (Metabase)

## Screenshots

![App Screenshot](donny_charles_88-dashboard.jpg)


## 🔗 Akses Dashboard
```bash
🌐 URL Lokal: http://localhost:3000
👤 Username:  root@mail.com  
🔑 Password:   root123
```

## 🗂️ Struktur Dashboard
Dashboard bisnis telah dikembangkan menggunakan Metabase untuk memberikan visibilitas menyeluruh terhadap performa mahasiswa. Dashboard ini menampilkan:
### Fitur Utama Dashboard:

| Komponen | Deskripsi | Visualisasi | 
| -------------------|-------------------|-------------------| 
| Total Mahasiswa |Count of Row | Number chart |
| Distribusi Status Akhir Mahasiswa | Count of Row by Status | Pie chart| 
| Hubungan Usia Enrollment dengan Status Kelulusan | Count of Row by Age_at_enrollment (binning) + Status | Stack Bar chart |
| Distribusi Gender per Status Akhir | Count of Row by Gender + Status | Bar chart |
| Tingkat Dropout berdasarkan Prodi | Filter Status = 'Dropout', Count of Row by Course | Row chart |
| Rata-rata SKS Lulus per Semester |Average of Curricular_units_1st_sem_approved + Curricular_units_2nd_sem_approved by Status | Line chart |
| Analisis Mahasiswa dengan Kebutuhan Khusus | Count of Row by Educational_special_needs + Status | Bar chart |
| Rata-rata Nilai Admission per Prodi |Average of Admission_grade by Course | Bar chart |

## 🤖 Model Prediction - Panduan Penggunaan

Script `app.py` digunakan oleh HR untuk memprediksi risiko attrition karyawan baru atau existing.

### Format File Input

Siapkan file CSV dengan nama `new_employee_data.csv` di dalam folder `data/`. 
File harus memiliki **34 kolom berikut** (kolom `Attrition` boleh disertakan atau tidak):

| Kolom | Tipe | Contoh Nilai |
|---|---|---|
| EmployeeId | Integer | 1001 |
| Age | Integer | 32 |
| BusinessTravel | String | `Travel_Rarely` / `Travel_Frequently` / `Non-Travel` |
| DailyRate | Integer | 800 |
| Department | String | `Sales` / `Research & Development` / `Human Resources` |
| DistanceFromHome | Integer | 5 |
| Education | Integer | 1–5 (1=Below College, 5=Doctor) |
| EducationField | String | `Life Sciences` / `Medical` / `Marketing` / `Technical Degree` / `Human Resources` / `Other` |
| EmployeeCount | Integer | 1 (selalu 1) |
| EnvironmentSatisfaction | Integer | 1–4 (1=Low, 4=Very High) |
| Gender | String | `Male` / `Female` |
| HourlyRate | Integer | 65 |
| JobInvolvement | Integer | 1–4 (1=Low, 4=Very High) |
| JobLevel | Integer | 1–5 |
| JobRole | String | `Sales Executive` / `Research Scientist` / `Laboratory Technician` / `Manager` / `Healthcare Representative` / `Manufacturing Director` / `Research Director` / `Sales Representative` / `Human Resources` |
| JobSatisfaction | Integer | 1–4 (1=Low, 4=Very High) |
| MaritalStatus | String | `Single` / `Married` / `Divorced` |
| MonthlyIncome | Integer | 5000 |
| MonthlyRate | Integer | 15000 |
| NumCompaniesWorked | Integer | 3 |
| Over18 | String | `Y` (selalu Y) |
| OverTime | String | `Yes` / `No` |
| PercentSalaryHike | Integer | 12 |
| PerformanceRating | Integer | 3–4 (3=Excellent, 4=Outstanding) |
| RelationshipSatisfaction | Integer | 1–4 (1=Low, 4=Very High) |
| StandardHours | Integer | 80 (selalu 80) |
| StockOptionLevel | Integer | 0–3 |
| TotalWorkingYears | Integer | 10 |
| TrainingTimesLastYear | Integer | 3 |
| WorkLifeBalance | Integer | 1–4 (1=Bad, 4=Best) |
| YearsAtCompany | Integer | 5 |
| YearsInCurrentRole | Integer | 3 |
| YearsSinceLastPromotion | Integer | 1 |
| YearsWithCurrManager | Integer | 2 |


### Cara Penggunaan Step-by-Step

**Langkah 1** — Pastikan model sudah ada di foler model: *student_status_model.pkl*, *scaler.pkl*, dan *label_encoder.pkl*
```bash
ls model/
```

**Langkah 2** — Jalankan aplikasi Streamlit
```bash
streamlit run app.py
```

# 3. Akses di browser
#    Buka: http://localhost:8501

**🌐 Akses Prototype Cloud:**
Link Streamlit Community Cloud: 

**📝 Cara Menggunakan Prototype:**
1. Pilih menu "🔮 Prediksi Mahasiswa" di sidebar
2. Isi data akademik mahasiswa:
- Nilai Admission (0-200)
- Rata-rata Nilai Semester 1 & 2 (0-20)
- Jumlah SKS Diambil & Lulus per semester
- Usia enrollment dan status debtor
4. Klik tombol "🔮 Prediksi Status"
5. Lihat hasil prediksi beserta probabilitas dan rekomendasi intervensi
---
## 📈 Conclusion

Berdasarkan analisis data terhadap 1.470 karyawan, dapat disimpulkan bahwa tingkat employee attrition di perusahaan tidak terjadi secara acak, melainkan dipengaruhi oleh pola sistematis yang melibatkan faktor kompensasi, beban kerja, kepuasan karir, dan keseimbangan hidup.

**Temuan Kunci**

1. **Performa akademik awal:** (Grade Semester 1, Approval Rate, Admission Grade) merupakan prediktor terkuat status kelulusan mahasiswa.
2. **Faktor finansial (status Debtor)** memiliki korelasi signifikan dengan risiko dropout
3. **Program studi tertentu (Management, Nursing, Animation & Multimedia)** menunjukkan tingkat dropout yang lebih tinggi dan memerlukan intervensi khusus  
4. Mahasiswa dengan Approval Rate < 70% di semester 1 memiliki risiko dropout 3x lebih tinggi

**Performa Model**

| Metric | value | Interpretasi |
|---|---|---|
| Accuracy | 0.776271 | Model dapat memprediksi dengan cukup baik |
| F1-Score (Weighted) | 0.7860 |Performa seimbang untuk semua kelas |
| Precision  | 0.7595 | Akurat memprediksi mahasiswa yang lulus |
| Recall  | 0.84 | Cukup baik mendeteksi mahasiswa berisiko |

Tabel di atas menunjukkan performa model Random Forest yang telah di-tuning dalam memprediksi status mahasiswa (Dropout, Enrolled, Graduate). Model mencapai akurasi sebesar 77.6% yang mengindikasikan bahwa model mampu memprediksi dengan cukup baik pada data testing. F1-Score Weighted sebesar 0.786 menunjukkan performa yang seimbang untuk ketiga kelas prediksi, dengan mempertimbangkan ketidakseimbangan jumlah data antar kelas. Precision sebesar 0.7595 menunjukkan bahwa ketika model memprediksi suatu kelas, tingkat keakuratannya cukup tinggi. Sementara itu, Recall sebesar 0.84 mengindikasikan bahwa model mampu mendeteksi dengan baik sebagian besar mahasiswa yang berisiko dropout, yang merupakan aspek kritis dalam sistem early warning. Secara keseluruhan, model ini layak digunakan sebagai alat bantu untuk mengidentifikasi mahasiswa yang memerlukan intervensi akademik lebih lanjut.



**Fitur Paling Berpengaruh (berdasarkan Random Forest Feature Importance):**

| Ranking | Fitur | Importance Score |
|---|---|---|
| 1 | Approval_Rate_Sem2 | 0.0977 |
| 2 | Curricular_units_2nd_sem_approved | 0.0818 |
| 3 | Overall_Grade (engineered) | 0.0622 |
| 4 | Approval_Rate_Sem1 (engineered) | 0.0566 |
| 5 | Curricular_units_2nd_sem_grade | 0.0562 |
| 6 | Curricular_units_1st_sem_grade | 0.0521 |
| 7 | Admission_grade | 0.0489 |
| 8 | Age_at_enrollment | 0.0412 |
| 9 | Debtor | 0.0387 |
| 10 | Previous_qualification_grade | 0.0354 |


### 🎯 Rekomendasi Action Items

1. **Intervensi Akademik Dini Berdasarkan Approval Rate**
   Berdasarkan hasil analisis, `Approval_Rate_Sem2` adalah faktor paling berpengaruh (importance: 0.098). Mahasiswa dengan rasio kelulusan SKS < 70% di semester awal memiliki probabilitas dropout 3x lebih tinggi. Rekomendasi:
   * Setup alert otomatis untuk mahasiswa dengan Approval Rate < 70% di minggu ke-8 semester.
   * Wajibkan konseling akademik untuk mahasiswa dengan Grade Semester 1 < 10.0.
   * Berikan program tutoring intensif untuk mata kuliah dengan tingkat kegagalan tertinggi.

2. **Penguatan Sistem Pendukung Finansial**
   Fitur `Debtor` (status tunggakan) berkontribusi signifikan terhadap risiko dropout (importance: 0.039). Mahasiswa dengan tunggakan pembayaran cenderung mengalami stres akademik dan sosial. Rekomendasi:
   * Identifikasi mahasiswa dengan status `Debtor = Yes` dari dashboard Metabase.
   * Tawarkan skema cicilan fleksibel atau beasiswa darurat berbasis performa akademik.
   * Kolaborasi dengan lembaga keuangan untuk program pinjaman pendidikan bunga rendah.

3. **Program Retensi Fase Kritis (Semester 1–2)**
   Mahasiswa di semester awal adalah kelompok paling rentan dropout. Rekomendasi:
   * Rancang program orientasi akademik 30 hari yang terstruktur untuk mahasiswa baru.
   * Pasangkan sistem peer-mentoring: mahasiswa tingkat akhir membimbing mahasiswa baru.
   * Lakukan monitoring progress bulanan melalui dashboard dengan KPI: Grade, Approval Rate, Attendance.

4. **Implementasi Early Warning System dengan `app.py`**
   Jalankan prototype `app.py` secara berkala untuk mengidentifikasi mahasiswa dengan prediksi Dropout (probabilitas > 60%). Dari 4.424 data mahasiswa, model mengidentifikasi pola risiko yang dapat diantisipasi. Rekomendasi:
   * Integrasi model ke sistem akademik untuk screening otomatis setiap akhir semester.
   * Prioritaskan intervensi berdasarkan kombinasi: probabilitas dropout tertinggi + Approval Rate terendah.
   * Track efektivitas intervensi melalui dashboard: bandingkan dropout rate sebelum & sesudah program.

5. **Optimalisasi Proses Seleksi & Penempatan**
   `Admission_grade` (importance: 0.049) dan `Previous_qualification_grade` menunjukkan bahwa kualitas input mahasiswa berpengaruh terhadap kelulusan. Rekomendasi:
   * Review kriteria seleksi penerimaan mahasiswa baru berdasarkan data historis kelulusan.
   * Berikan placement test untuk penjurusan yang lebih sesuai dengan kompetensi awal mahasiswa.
   * Siapkan program bridging course untuk mahasiswa dengan latar belakang akademik berbeda.
