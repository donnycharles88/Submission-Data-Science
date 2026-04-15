import streamlit as st
import pandas as pd
import numpy as np
import joblib

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Prediksi Dropout - Jaya Jaya Institut",
    page_icon="🎓",
    layout="wide"
)

# ── Load Model ────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    model  = joblib.load('model/student_status_model.pkl')
    scaler = joblib.load('model/scaler.pkl')
    return model, scaler

model, scaler = load_model()

FEATURE_COLS = [
    'Marital_status','Application_mode','Application_order','Course',
    'Daytime_evening_attendance','Previous_qualification',
    'Previous_qualification_grade','Nacionality','Mothers_qualification',
    'Fathers_qualification','Mothers_occupation','Fathers_occupation',
    'Admission_grade','Displaced','Educational_special_needs','Debtor',
    'Tuition_fees_up_to_date','Gender','Scholarship_holder',
    'Age_at_enrollment','International',
    'Curricular_units_1st_sem_credited','Curricular_units_1st_sem_enrolled',
    'Curricular_units_1st_sem_evaluations','Curricular_units_1st_sem_approved',
    'Curricular_units_1st_sem_grade','Curricular_units_1st_sem_without_evaluations',
    'Curricular_units_2nd_sem_credited','Curricular_units_2nd_sem_enrolled',
    'Curricular_units_2nd_sem_evaluations','Curricular_units_2nd_sem_approved',
    'Curricular_units_2nd_sem_grade','Curricular_units_2nd_sem_without_evaluations',
    'Unemployment_rate','Inflation_rate','GDP',
    'Approval_Rate_Sem1','Approval_Rate_Sem2','Overall_Grade','Total_Units_Enrolled'
]

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🎓 Jaya Jaya Institut")
st.subheader("Sistem Prediksi Risiko Dropout Mahasiswa")
st.markdown("---")

c1, c2, c3 = st.columns(3)
c1.metric("Total Data Training", "3.630", "Dropout + Graduate")
c2.metric("Akurasi Model",       "90.9%",  "Random Forest")
c3.metric("Jumlah Fitur",        "40",     "36 asli + 4 engineered")
st.markdown("---")

# ── Sidebar Input ─────────────────────────────────────────────────────────────
st.sidebar.header("📝 Input Data Mahasiswa")

st.sidebar.subheader("👤 Data Pribadi")
marital_status = st.sidebar.selectbox(
    "Status Pernikahan", [1,2,3,4,5,6],
    format_func=lambda x:{1:"Single",2:"Married",3:"Widower",
                           4:"Divorced",5:"Facto Union",6:"Legally Separated"}[x])
gender         = st.sidebar.selectbox("Gender",[1,0],
                    format_func=lambda x:"Laki-laki" if x==1 else "Perempuan")
age            = st.sidebar.slider("Usia Saat Enrollment", 17, 70, 20)
nacionality    = st.sidebar.number_input("Kode Kewarganegaraan",1,109,1,
                    help="1=Portugal, 2=German, 6=Spain, dll.")
international  = st.sidebar.selectbox("Mahasiswa Internasional",[0,1],
                    format_func=lambda x:"Tidak" if x==0 else "Ya")
displaced      = st.sidebar.selectbox("Displaced (Pindahan)",[0,1],
                    format_func=lambda x:"Tidak" if x==0 else "Ya")
edu_special    = st.sidebar.selectbox("Kebutuhan Pendidikan Khusus",[0,1],
                    format_func=lambda x:"Tidak" if x==0 else "Ya")

st.sidebar.subheader("📋 Data Pendaftaran")
app_mode       = st.sidebar.number_input("Mode Aplikasi Pendaftaran",1,57,1)
app_order      = st.sidebar.slider("Urutan Pilihan Aplikasi",0,9,1)
course         = st.sidebar.number_input("Kode Program Studi",33,9991,9500,
                    help="9500=Nursing, 9238=Management, 9147=Animation, dll.")
daytime        = st.sidebar.selectbox("Waktu Kuliah",[1,0],
                    format_func=lambda x:"Pagi/Siang" if x==1 else "Malam")
prev_qual      = st.sidebar.number_input("Kode Kualifikasi Sebelumnya",1,43,1)
prev_grade     = st.sidebar.slider("Nilai Kualifikasi Sebelumnya",95.0,190.0,130.0,0.1)
admission_grade= st.sidebar.slider("Nilai Admission",95.0,190.0,130.0,0.1)

st.sidebar.subheader("👨‍👩‍👧 Data Keluarga")
moth_qual      = st.sidebar.number_input("Kualifikasi Ibu (kode)",1,44,19)
fath_qual      = st.sidebar.number_input("Kualifikasi Ayah (kode)",1,44,19)
moth_occ       = st.sidebar.number_input("Pekerjaan Ibu (kode)",0,194,5)
fath_occ       = st.sidebar.number_input("Pekerjaan Ayah (kode)",0,194,5)

st.sidebar.subheader("💳 Status Finansial")
tuition        = st.sidebar.selectbox("Tuition Fees Up to Date",[1,0],
                    format_func=lambda x:"✅ Lunas" if x==1 else "❌ Menunggak")
scholarship    = st.sidebar.selectbox("Penerima Beasiswa",[0,1],
                    format_func=lambda x:"Tidak" if x==0 else "Ya")
debtor         = st.sidebar.selectbox("Status Debitur",[0,1],
                    format_func=lambda x:"Tidak" if x==0 else "Ya")

st.sidebar.subheader("📚 Akademik Semester 1")
cu1_credited   = st.sidebar.slider("SKS Diakui Sem.1",    0, 20, 0)
cu1_enrolled   = st.sidebar.slider("SKS Diambil Sem.1",   0, 26, 6)
cu1_eval       = st.sidebar.slider("Evaluasi Sem.1",      0, 45, 8)
cu1_approved   = st.sidebar.slider("SKS Lulus Sem.1",     0, 26, 5)
cu1_grade      = st.sidebar.slider("Nilai Rata-rata Sem.1",0.0,20.0,12.0,0.1)
cu1_no_eval    = st.sidebar.slider("SKS Tanpa Eval Sem.1", 0, 12, 0)

st.sidebar.subheader("📚 Akademik Semester 2")
cu2_credited   = st.sidebar.slider("SKS Diakui Sem.2",    0, 20, 0)
cu2_enrolled   = st.sidebar.slider("SKS Diambil Sem.2",   0, 23, 6)
cu2_eval       = st.sidebar.slider("Evaluasi Sem.2",      0, 33, 8)
cu2_approved   = st.sidebar.slider("SKS Lulus Sem.2",     0, 20, 5)
cu2_grade      = st.sidebar.slider("Nilai Rata-rata Sem.2",0.0,20.0,12.0,0.1)
cu2_no_eval    = st.sidebar.slider("SKS Tanpa Eval Sem.2", 0, 12, 0)

st.sidebar.subheader("🌐 Kondisi Ekonomi")
unemp_rate     = st.sidebar.slider("Tingkat Pengangguran (%)",7.6,16.2,11.1,0.1)
inflation_rate = st.sidebar.slider("Tingkat Inflasi (%)",-0.8,3.7,0.6,0.1)
gdp            = st.sidebar.slider("GDP",-4.06,3.51,2.02,0.01)

# ── Hitung Fitur Engineered Otomatis ─────────────────────────────────────────
apr_sem1         = cu1_approved / max(cu1_enrolled, 1)
apr_sem2         = cu2_approved / max(cu2_enrolled, 1)
overall_grade    = (cu1_grade + cu2_grade) / 2
total_enrolled   = cu1_enrolled + cu2_enrolled

# ── Tampilkan summary engineered features ────────────────────────────────────
st.subheader("📊 Ringkasan Fitur Akademik (Auto-calculated)")
e1, e2, e3, e4 = st.columns(4)
e1.metric("Approval Rate Sem.1", f"{apr_sem1:.1%}",
          "⚠️ Risiko" if apr_sem1 < 0.5 else "✅ Baik")
e2.metric("Approval Rate Sem.2", f"{apr_sem2:.1%}",
          "⚠️ Risiko" if apr_sem2 < 0.5 else "✅ Baik")
e3.metric("Overall Grade",       f"{overall_grade:.1f}/20",
          "⚠️ Rendah" if overall_grade < 10 else "✅ Cukup")
e4.metric("Total SKS Diambil",   str(total_enrolled), "Sem.1 + Sem.2")

# ── Prediksi ──────────────────────────────────────────────────────────────────
st.sidebar.markdown("---")
predict_btn = st.sidebar.button("🔍 Prediksi Sekarang", type="primary", use_container_width=True)

if predict_btn:
    input_data = {
        'Marital_status': marital_status, 'Application_mode': app_mode,
        'Application_order': app_order, 'Course': course,
        'Daytime_evening_attendance': daytime, 'Previous_qualification': prev_qual,
        'Previous_qualification_grade': prev_grade, 'Nacionality': nacionality,
        'Mothers_qualification': moth_qual, 'Fathers_qualification': fath_qual,
        'Mothers_occupation': moth_occ, 'Fathers_occupation': fath_occ,
        'Admission_grade': admission_grade, 'Displaced': displaced,
        'Educational_special_needs': edu_special, 'Debtor': debtor,
        'Tuition_fees_up_to_date': tuition, 'Gender': gender,
        'Scholarship_holder': scholarship, 'Age_at_enrollment': age,
        'International': international,
        'Curricular_units_1st_sem_credited': cu1_credited,
        'Curricular_units_1st_sem_enrolled': cu1_enrolled,
        'Curricular_units_1st_sem_evaluations': cu1_eval,
        'Curricular_units_1st_sem_approved': cu1_approved,
        'Curricular_units_1st_sem_grade': cu1_grade,
        'Curricular_units_1st_sem_without_evaluations': cu1_no_eval,
        'Curricular_units_2nd_sem_credited': cu2_credited,
        'Curricular_units_2nd_sem_enrolled': cu2_enrolled,
        'Curricular_units_2nd_sem_evaluations': cu2_eval,
        'Curricular_units_2nd_sem_approved': cu2_approved,
        'Curricular_units_2nd_sem_grade': cu2_grade,
        'Curricular_units_2nd_sem_without_evaluations': cu2_no_eval,
        'Unemployment_rate': unemp_rate, 'Inflation_rate': inflation_rate, 'GDP': gdp,
        'Approval_Rate_Sem1': apr_sem1, 'Approval_Rate_Sem2': apr_sem2,
        'Overall_Grade': overall_grade, 'Total_Units_Enrolled': total_enrolled,
    }

    input_df     = pd.DataFrame([input_data])[FEATURE_COLS]
    input_scaled = scaler.transform(input_df)

    prediction = model.predict(input_scaled)[0]
    proba      = model.predict_proba(input_scaled)[0]

    st.markdown("---")
    st.subheader("🎯 Hasil Prediksi")

    r1, r2, r3 = st.columns([2,1,1])
    with r1:
        if prediction == 0:
            st.error("## ⚠️ BERISIKO DROPOUT\n"
                     "Mahasiswa ini diprediksi **berpotensi dropout**.\n"
                     "Segera berikan bimbingan akademik dan dukungan finansial.")
        else:
            st.success("## ✅ DIPREDIKSI GRADUATE\n"
                       "Mahasiswa ini diprediksi akan **menyelesaikan studinya**.\n"
                       "Tetap pantau dan pertahankan performa akademiknya.")
    r2.metric("Probabilitas Dropout",  f"{proba[0]:.1%}")
    r3.metric("Probabilitas Graduate", f"{proba[1]:.1%}")

    st.markdown("**Tingkat Risiko Dropout:**")
    st.progress(float(proba[0]))

    # Analisis faktor risiko otomatis
    st.markdown("---")
    st.subheader("🔍 Analisis Faktor Risiko")
    risks, positives = [], []

    if apr_sem2   < 0.5 : risks.append(f"📉 Approval Rate Sem.2 rendah: {apr_sem2:.1%}")
    else                : positives.append(f"📈 Approval Rate Sem.2 baik: {apr_sem2:.1%}")
    if apr_sem1   < 0.5 : risks.append(f"📉 Approval Rate Sem.1 rendah: {apr_sem1:.1%}")
    else                : positives.append(f"📈 Approval Rate Sem.1 baik: {apr_sem1:.1%}")
    if overall_grade<10 : risks.append(f"📉 Overall Grade rendah: {overall_grade:.1f}/20")
    else                : positives.append(f"📈 Overall Grade cukup: {overall_grade:.1f}/20")
    if tuition    == 0  : risks.append("💸 Tuition fees menunggak")
    else                : positives.append("💳 Tuition fees lunas")
    if debtor     == 1  : risks.append("🔴 Berstatus debitur")
    if scholarship== 1  : positives.append("🏅 Menerima beasiswa")
    if age        > 30  : risks.append(f"👤 Usia enrollment >30 tahun ({age} tahun)")

    fa, fb = st.columns(2)
    with fa:
        st.markdown("**⚠️ Faktor Risiko:**")
        for r in risks:     st.warning(r)
        if not risks:       st.success("Tidak ada faktor risiko.")
    with fb:
        st.markdown("**✅ Faktor Positif:**")
        for p in positives: st.info(p)

    with st.expander("📋 Lihat Seluruh 40 Fitur Input"):
        st.dataframe(input_df.T.rename(columns={0:"Nilai"}), use_container_width=True)

else:
    st.info("👈 Lengkapi data di sidebar, lalu klik **Prediksi Sekarang**")
    st.markdown("""
    ### Petunjuk Penggunaan
    1. Lengkapi seluruh data mahasiswa di sidebar kiri
    2. 4 fitur akademik engineered dihitung **otomatis** dari input
    3. Klik tombol **Prediksi Sekarang**
    4. Sistem menampilkan prediksi + analisis faktor risiko
    """)
