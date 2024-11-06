import streamlit as st
import os
import shutil
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import process_invoice  # Now it should work
# from backend.app import process_invoice  # Import the backend logic

# Setup the output folder path
output_folder = "./outputs"

# Streamlit interface
st.title("Invoice Processor")

st.write(
    "Upload your invoice (PDF format), and we'll return the corresponding XLS files."
)

# Invoice file upload
uploaded_file = st.file_uploader("Choose an invoice PDF", type=["pdf"])

if uploaded_file is not None:
    # Save the uploaded file temporarily
    if not os.path.exists('temp'):
        os.makedirs('temp')
    temp_invoice_path = os.path.join("temp", uploaded_file.name)
    with open(temp_invoice_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Process the invoice using the backend code
    st.write("Processing your invoice...")

    # Call the backend function to process the invoice
    result = process_invoice(temp_invoice_path)

    # Provide download link for the processed XLS files
    if result:
        st.write("Processing complete! Download your files below:")

        # List the files in the output folder
        for file in os.listdir(output_folder):
            file_path = os.path.join(output_folder, file)
            if os.path.isfile(file_path):
                st.download_button(
                    label=f"Download {file}",
                    data=open(file_path, "rb").read(),
                    file_name=file,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )

        # Cleanup the temporary invoice file
        os.remove(temp_invoice_path)

else:
    st.write("Please upload an invoice PDF file.")
