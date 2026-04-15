import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import joblib
import warnings
warnings.filterwarnings('ignore')

# Konfigurasi Halaman
st.set_page_config(page_title="Prediksi Status Mahasiswa", page_icon="🎓", layout="wide")

# 1. Load Data (Menggunakan data.csv asli)
@st.cache_data
def load_data():
    try:
        # Menggunakan separator ';' sesuai data asli
        df = pd.read_csv('data.csv', sep=';')
        return df
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        return None

# 2. Load Model
@st.cache_resource
def load_model():
    try:
        model = joblib.load('model/student_status_model.pkl')
        scaler = joblib.load('model/scaler.pkl')
        label_encoder = joblib.load('model/label_encoder.pkl')
        return model, scaler, label_encoder
    except Exception as e:
        st.error(f"Gagal memuat model: {e}")
        return None, None, None

df = load_data()
model, scaler, label_encoder = load_model()

# Definisi Feature Cols HARUS SAMA PERSIS dengan notebook.ipynb
feature_cols = [
    'Marital_status', 'Application_mode', 'Application_order', 'Course',
    'Daytime_evening_attendance', 'Previous_qualification',
    'Previous_qualification_grade', 'Nacionality', 'Mothers_qualification',
    'Fathers_qualification', 'Mothers_occupation', 'Fathers_occupation',
    'Admission_grade', 'Displaced', 'Educational_special_needs', 'Debtor',
    'Tuition_fees_up_to_date', 'Gender', 'Scholarship_holder',
    'Age_at_enrollment', 'International',
    'Curricular_units_1st_sem_credited', 'Curricular_units_1st_sem_enrolled',
    'Curricular_units_1st_sem_evaluations', 'Curricular_units_1st_sem_approved',
    'Curricular_units_1st_sem_grade', 'Curricular_units_1st_sem_without_evaluations',
    'Curricular_units_2nd_sem_credited', 'Curricular_units_2nd_sem_enrolled',
    'Curricular_units_2nd_sem_evaluations', 'Curricular_units_2nd_sem_approved',
    'Curricular_units_2nd_sem_grade', 'Curricular_units_2nd_sem_without_evaluations',
    'Unemployment_rate', 'Inflation_rate', 'GDP',
    'Approval_Rate_Sem1', 'Approval_Rate_Sem2', 'Overall_Grade', 'Total_Units_Enrolled'
]

# Sidebar
st.sidebar.title("🎓 Jaya Jaya Institut")
menu = st.sidebar.radio("Menu", ["📊 Dashboard", "🔮 Prediksi Mahasiswa"])

# --- HALAMAN DASHBOARD ---
if menu == "📊 Dashboard":
    st.title("Dashboard Performa Mahasiswa")
    if df is not None:
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Mahasiswa", len(df))
        col2.metric("Lulus", (df['Status'] == 'Graduate').sum())
        col3.metric("Dropout", (df['Status'] == 'Dropout').sum())
        
        st.subheader("Distribusi Status")
        st.bar_chart(df['Status'].value_counts())
        
        st.subheader("Rata-rata Nilai Admission per Course (Top 10)")
        course_avg = df.groupby('Course')['Admission_grade'].mean().sort_values(ascending=False).head(10)
        st.bar_chart(course_avg)

# --- HALAMAN PREDIKSI ---
elif menu == "🔮 Prediksi Mahasiswa":
    st.title("Prediksi Status Mahasiswa")
    if model is None:
        st.error("Model tidak ditemukan di folder 'model/'.")
    else:
        st.write("Masukkan data mahasiswa untuk prediksi:")
        
        # Input Fitur Utama
        admission_grade = st.number_input("Admission Grade", min_value=0.0, max_value=200.0, value=120.0)
        sem1_grade = st.number_input("Rata-rata Nilai Semester 1", min_value=0.0, max_value=20.0, value=12.0)
        sem1_enrolled = st.number_input("SKS Diambil Semester 1", min_value=1, max_value=30, value=6)
        sem1_approved = st.number_input("SKS Lulus Semester 1", min_value=0, max_value=30, value=5)
        
        sem2_grade = st.number_input("Rata-rata Nilai Semester 2", min_value=0.0, max_value=20.0, value=12.0)
        sem2_enrolled = st.number_input("SKS Diambil Semester 2", min_value=1, max_value=30, value=6)
        sem2_approved = st.number_input("SKS Lulus Semester 2", min_value=0, max_value=30, value=5)
        
        age = st.number_input("Usia Enrollment", min_value=17, max_value=60, value=20)
        debtor = st.selectbox("Status Debtor (Tunggakan)", [0, 1])
        
        # Feature Engineering (SAMA PERSIS dengan notebook)
        approval_1 = sem1_approved / sem1_enrolled if sem1_enrolled > 0 else 0
        approval_2 = sem2_approved / sem2_enrolled if sem2_enrolled > 0 else 0
        overall_grade = (sem1_grade + sem2_grade) / 2
        total_units = sem1_enrolled + sem2_enrolled
        
        # Konstruksi Input DataFrame
        # Inisialisasi semua kolom dengan nilai default 0 agar tidak ada kolom yang hilang
        input_dict = {col: [0] for col in feature_cols}
        
        # Isi dengan nilai default yang masuk akal (sesuai dataset asli)
        input_dict['Marital_status'] = [1]
        input_dict['Application_mode'] = [1]
        input_dict['Application_order'] = [1]
        input_dict['Course'] = [9500] # Default Nursing
        input_dict['Daytime_evening_attendance'] = [1]
        input_dict['Previous_qualification'] = [1]
        input_dict['Previous_qualification_grade'] = [130.0]
        input_dict['Nacionality'] = [1]
        input_dict['Mothers_qualification'] = [19]
        input_dict['Fathers_qualification'] = [19]
        input_dict['Mothers_occupation'] = [5]
        input_dict['Fathers_occupation'] = [5]
        
        # Isi dengan Input User
        input_dict['Admission_grade'] = [admission_grade]
        input_dict['Displaced'] = [0]
        input_dict['Educational_special_needs'] = [0]
        input_dict['Debtor'] = [debtor]
        input_dict['Tuition_fees_up_to_date'] = [1]
        input_dict['Gender'] = [1]
        input_dict['Scholarship_holder'] = [0]
        input_dict['Age_at_enrollment'] = [age]
        input_dict['International'] = [0]
        
        input_dict['Curricular_units_1st_sem_credited'] = [0]
        input_dict['Curricular_units_1st_sem_enrolled'] = [sem1_enrolled]
        input_dict['Curricular_units_1st_sem_evaluations'] = [sem1_enrolled] # Asumsi evaluasi = enrolled
        input_dict['Curricular_units_1st_sem_approved'] = [sem1_approved]
        input_dict['Curricular_units_1st_sem_grade'] = [sem1_grade]
        input_dict['Curricular_units_1st_sem_without_evaluations'] = [0]
        
        input_dict['Curricular_units_2nd_sem_credited'] = [0]
        input_dict['Curricular_units_2nd_sem_enrolled'] = [sem2_enrolled]
        input_dict['Curricular_units_2nd_sem_evaluations'] = [sem2_enrolled]
        input_dict['Curricular_units_2nd_sem_approved'] = [sem2_approved]
        input_dict['Curricular_units_2nd_sem_grade'] = [sem2_grade]
        input_dict['Curricular_units_2nd_sem_without_evaluations'] = [0]
        
        input_dict['Unemployment_rate'] = [10.8]
        input_dict['Inflation_rate'] = [1.4]
        input_dict['GDP'] = [1.74]
        
        # Isi Engineered Features
        input_dict['Approval_Rate_Sem1'] = [approval_1]
        input_dict['Approval_Rate_Sem2'] = [approval_2]
        input_dict['Overall_Grade'] = [overall_grade]
        input_dict['Total_Units_Enrolled'] = [total_units]
        
        if st.button("🔮 Prediksi Status", type="primary"):
            try:
                df_input = pd.DataFrame(input_dict)
                
                # PENTING: Urutkan kolom agar sama persis dengan feature_cols model
                df_input = df_input[feature_cols]
                
                # Transform dengan Scaler
                input_scaled = scaler.transform(df_input)
                
                # Prediksi
                prediction = model.predict(input_scaled)
                probability = model.predict_proba(input_scaled)
                result_label = label_encoder.inverse_transform(prediction)[0]
                
                # Tampilkan Hasil
                st.success(f"Hasil Prediksi: **{result_label}**")
                
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.metric("Probabilitas Tertinggi", f"{max(probability[0])*100:.1f}%")
                with col2:
                    prob_df = pd.DataFrame({'Status': label_encoder.classes_, 'Prob': probability[0]})
                    st.bar_chart(prob_df.set_index('Status'))
                    
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")