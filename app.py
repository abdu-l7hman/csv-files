import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Student Time Reordering", layout="centered")

st.title("📊 Student Time Reordering App")

st.markdown("""
Welcome, Teacher! 👩‍🏫👨‍🏫  
This app helps you reorder students' total time based on your original email list.

### 📥 Upload Instructions:
1. **CSV file** (daily time report):  
   Skip the first 2 rows (header + teacher row), extract from `Username` and `Total time` columns.
2. **Excel file (.xlsx)**:  
   Contains the original email list in **column B** (second column).

⬇️ You'll get a downloadable Excel file with the time reordered based on your original list.
""")

# File uploads
uploaded_daily_csv = st.file_uploader("Step 1: Upload Daily CSV File (with Time Data)", type=["csv"])
uploaded_original_excel = st.file_uploader("Step 2: Upload Original Email List Excel File (.xlsx)", type=["xlsx"])

if uploaded_daily_csv and uploaded_original_excel:
    try:
        # Read the CSV and skip first two rows (header + teacher)
        df_daily = pd.read_csv(uploaded_daily_csv, skiprows=2)

        # Check necessary columns
        if 'Username' not in df_daily.columns or 'Total time' not in df_daily.columns:
            st.error("CSV file must contain 'Username' and 'Total time' columns after skipping first 2 rows.")
            st.stop()

        # Read the Excel with original email list
        df_original = pd.read_excel(uploaded_original_excel)

        if df_original.shape[1] < 2:
            st.error("Excel file must have at least 2 columns. Emails must be in column B.")
            st.stop()

        # Get emails from column B
        original_emails = df_original.iloc[:, 1].dropna().astype(str).str.strip().tolist()

        # Prepare username: time mapping from daily file
        usernames = df_daily['Username'].astype(str).str.strip().tolist()
        total_times = df_daily['Total time'].astype(str).tolist()
        time_dict = dict(zip(usernames, total_times))

        # Reorder times based on original email list
        reordered_times = [time_dict.get(email, "00:00:00") for email in original_emails]

        # Create output DataFrame
        df_output = pd.DataFrame({
            'Username': original_emails,
            'Reordered Total Time': reordered_times
        })

        # Convert to Excel for download
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_output.to_excel(writer, index=False)
        output.seek(0)

        # Show download button
        st.success("✅ Processing complete! Download your reordered file below.")
        st.download_button(
            label="⬇️ Download Reordered Excel File",
            data=output.getvalue(),
            file_name="reordered_time_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"❌ An error occurred: {e}")
