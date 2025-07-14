import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Student Time Reordering", layout="centered")

st.title("📊 Student Time Reordering App")

st.markdown("""
Welcome, Teacher! 👩‍🏫👨‍🏫  
This app helps you reorder students' total time based on your original email list.

### 📥 Upload Instructions:
1. **CSV file** (daily report):  
   Must contain `Username` and `Total time` columns.  
   ✅ Keep the header  
   ❌ Skip the **second row only** (teacher name)

2. **Excel file (.xlsx)**:  
   Contains the original email list in **column B**.  
   All columns and rows will be preserved in the final output.

⬇️ You’ll get a downloadable Excel file with a new `Reordered Total Time` column.
""")

# Uploads
uploaded_daily_csv = st.file_uploader("Step 1: Upload Daily CSV File", type=["csv"])
uploaded_original_excel = st.file_uploader("Step 2: Upload Original Email List Excel File (.xlsx)", type=["xlsx"])

if uploaded_daily_csv and uploaded_original_excel:
    try:
        # Read CSV and skip only the second row (row index 1)
        all_lines = uploaded_daily_csv.read().decode("utf-8").splitlines()
        cleaned_lines = [line for idx, line in enumerate(all_lines) if idx != 1]
        df_daily = pd.read_csv(io.StringIO("\n".join(cleaned_lines)))

        # Check for required columns
        if 'Username' not in df_daily.columns or 'Total time' not in df_daily.columns:
            st.error("CSV file must contain 'Username' and 'Total time' columns.")
            st.stop()

        # Read Excel file
        df_original = pd.read_excel(uploaded_original_excel)

        # Extract emails from column B (index 1)
        if df_original.shape[1] < 2:
            st.error("Excel file must have at least two columns. Emails must be in column B.")
            st.stop()

        original_emails = df_original.iloc[:, 1].astype(str).str.strip().tolist()
        usernames = df_daily['Username'].astype(str).str.strip().tolist()
        total_times = df_daily['Total time'].astype(str).tolist()

        # Build mapping of username to time
        time_map = dict(zip(usernames, total_times))

        # Add 'Reordered Total Time' column to original DataFrame
        df_original['Reordered Total Time'] = [time_map.get(email, "00:00:00") for email in original_emails]

        # Export to Excel
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_original.to_excel(writer, index=False)
        output.seek(0)

        # Provide download button
        st.success("✅ File ready! Download below:")
        st.download_button(
            label="⬇️ Download Reordered Excel File",
            data=output.getvalue(),
            file_name="reordered_time_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"❌ An error occurred: {e}")
