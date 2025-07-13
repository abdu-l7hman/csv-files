import streamlit as st
import pandas as pd
import io

st.title("Excel + Text File Processor")

uploaded_csv = st.file_uploader("Upload Excel/CSV File starting with 'Day'", type=['csv', 'xlsx'])
uploaded_txt = st.file_uploader("Upload Text File (oreginal.txt)", type=['txt'])

if uploaded_csv and uploaded_txt:
    try:
        # Read CSV/Excel
        if uploaded_csv.name.endswith('.csv'):
            df = pd.read_csv(uploaded_csv)
        else:
            df = pd.read_excel(uploaded_csv)

        if 'Username' not in df.columns or 'Total time' not in df.columns:
            st.error("CSV file must contain 'Username' and 'Total time' columns.")
            st.stop()

        email_list = df['Username'].tolist()
        total_time = df['Total time'].tolist()

        original_list = [line.strip() for line in uploaded_txt.readlines()]
        original_list = [line.decode('utf-8') for line in original_list]

        if len(email_list) != len(total_time):
            st.warning("Length mismatch between email list and total time list.")

        combined_dict = dict(zip(email_list, total_time))
        reordered_total_time = [combined_dict.get(username, "00:00:00") for username in original_list]

        df_output = pd.DataFrame({
            'Username': original_list,
            'Reordered Total Time': reordered_total_time
        })

        # Convert to Excel
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_output.to_excel(writer, index=False)
        st.success("File processed successfully!")

        st.download_button(
            label="Download Excel File",
            data=output.getvalue(),
            file_name="output_with_time.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"Error: {str(e)}")
