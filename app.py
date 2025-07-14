import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Student Time Reordering", layout="centered")

st.title("📊 Student Time Reordering App")

st.markdown("""
Welcome, Teacher! 👩‍🏫👨‍🏫  
This app helps you reorder students' total time data based on your original email list.

### 📥 What to upload:
1. **CSV file**: The file generated after each day, with `Username` and `Total time` columns.  
2. **Excel file (.xlsx)**: Contains the original list of student emails in **column B**.

Once uploaded, you'll get a downloadable Excel file with the reordered time data.
""")

uploaded_daily_csv = st.file_uploader("Step 1: Upload Daily Time CSV File", type=['csv'])
uploaded_original_xlsx = st.file_uploader("Step 2: Upload Original Email List Excel File (.xlsx, Emails in Column B)", type=['xlsx'])

if uploaded_daily_csv and uploaded_original_xlsx:
    try:
        # Read the daily CSV file
        df_daily = pd.read_csv(uploaded_daily_csv)

        # Validate required columns
        if 'Username' not in df_daily.columns or 'Total time' not in df_daily.columns:
            st.error("The first CSV file must contain 'Username' and 'Total time' columns.")
            st.stop()

        # Read the original email Excel file
        df_original = pd.read_excel(uploaded_original_xlsx)

        # Check that at least 2 columns exist (to access column B)
        if df_original.shape[1] < 2:
            st.error("The original Excel file must have emails in column B (second column).")
            st.stop()

        # Extract emails from column B
        original_email_list = df_original.iloc[:, 1].dropna().astype(str).str.strip().tolist()

        # Clean up data from daily report
        usernames = df_daily['Username'].astype(str).str.strip().tolist()
        total_times = df_daily['Total time'].tolist()

        # Build dictionary for fast lookup
        time_lookup = dict(zip(usernames, total_times))

        # Reorder time data
        reordered_times = [time_lookup.get(email, "00:00:00") for email in original_email_list]

        # Build the output DataFrame
        df_output = pd.DataFrame({
            'Username': original_email_list,
            'Reordered Total Time': reordered_times
        })

        # Write to Excel
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_output.to_excel(writer, index=False)
        output.seek(0)

        # Show download button
        st.success("✅ File processed successfully! Click below to download:")
        st.download_button(
            label="⬇️ Download Reordered Excel File",
            data=output.getvalue(),
            file_name="reordered_time_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
