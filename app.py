import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Student Time Reordering", layout="centered")

st.title("📊 Student Time Reordering App")

st.markdown("""
Welcome, Teacher! 👩‍🏫👨‍🏫  
This app helps you reorder students' total time data based on your original email list.

### 📥 What to upload:
1. **Excel or CSV file**: This file is the file generated after every day

2. **Text file (.txt)**: A list of student emails (one per line), in the order you'd like to display them.
example

ahmad@gmail.com 
ali@gmail.com
... and so on

Once uploaded, you'll get a downloadable Excel file with the reordered time data.
""")

uploaded_excel = st.file_uploader("Step 1: Upload Excel or CSV File", type=['csv', 'xlsx'])
uploaded_txt = st.file_uploader("Step 2: Upload Text File with Original Email Order", type=['txt'])

if uploaded_excel and uploaded_txt:
    try:
        # Read Excel or CSV file
        if uploaded_excel.name.endswith('.csv'):
            df = pd.read_csv(uploaded_excel)
        else:
            df = pd.read_excel(uploaded_excel)

        if 'Username' not in df.columns or 'Total time' not in df.columns:
            st.error("The uploaded file must contain 'Username' and 'Total time' columns.")
            st.stop()

        email_list = df['Username'].tolist()
        total_time = df['Total time'].tolist()

        # Read original email list
        original_list = [line.strip().decode('utf-8') for line in uploaded_txt.readlines()]

        if len(email_list) != len(total_time):
            st.warning("⚠️ Note: The number of emails and total time entries do not match.")

        combined_dict = dict(zip(email_list, total_time))
        reordered_total_time = [combined_dict.get(username, "00:00:00") for username in original_list]

        df_output = pd.DataFrame({
            'Username': original_list,
            'Reordered Total Time': reordered_total_time
        })

        # Convert to downloadable Excel
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_output.to_excel(writer, index=False)
        output.seek(0)

        st.success("✅ File processed successfully! Click below to download:")

        st.download_button(
            label="⬇️ Download Reordered Excel File",
            data=output.getvalue(),
            file_name="output_with_time.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
