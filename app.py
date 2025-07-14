import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Student Time Reordering", layout="centered")

st.title("📊 Student Time Reordering App")

st.markdown("""
Welcome, Teacher! 👩‍🏫👨‍🏫  
This app helps you reorder students' total time data based on your original email list.

### 📥 What to upload:
1. **Excel or CSV file**: The file generated after each day, with `Username` and `Total time` columns.
2. **Excel file (.xlsx)**: Contains the original list of student emails in **column B**.

Once uploaded, you'll get a downloadable Excel file with the reordered time data.
""")

uploaded_excel = st.file_uploader("Step 1: Upload Excel or CSV File", type=['csv', 'xlsx'])
uploaded_original_excel = st.file_uploader("Step 2: Upload Excel File with Original Email List (Emails in Column B)", type=['xlsx'])

if uploaded_excel and uploaded_original_excel:
    try:
        # Read the main daily report
        if uploaded_excel.name.endswith('.csv'):
            df = pd.read_csv(uploaded_excel)
        else:
            df = pd.read_excel(uploaded_excel)

        # Validate required columns
        if 'Username' not in df.columns or 'Total time' not in df.columns:
            st.error("The uploaded file must contain 'Username' and 'Total time' columns.")
            st.stop()

        # Read the original Excel file
        df_original = pd.read_excel(uploaded_original_excel)

        # Check for at least two columns (to ensure column B exists)
        if df_original.shape[1] < 2:
            st.error("The uploaded Excel file must have emails in column B.")
            st.stop()

        # Extract emails from column B (index 1)
        original_list = df_original.iloc[:, 1].dropna().astype(str).str.strip().tolist()

        # Extract username and time from daily file
        email_list = df['Username'].astype(str).str.strip().tolist()
        total_time = df['Total time'].tolist()

        # Create dictionary of username: time
        combined_dict = dict(zip(email_list, total_time))

        # Reorder total time based on original email list
        reordered_total_time = [combined_dict.get(email, "00:00:00") for email in original_list]

        # Build output DataFrame
        df_output = pd.DataFrame({
            'Username': original_list,
            'Reordered Total Time': reordered_total_time
        })

        # Save to Excel
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_output.to_excel(writer, index=False)
        output.seek(0)

        # Download button
        st.success("✅ File processed successfully! Click below to download:")

        st.download_button(
            label="⬇️ Download Reordered Excel File",
            data=output.getvalue(),
            file_name="output_with_time.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
