import base64

def get_pdf_download_link(pdf_path, file_label):
    """Generate a link to download the pdf at `pdf_path`."""
    with open(pdf_path, 'rb') as f:
        pdf_data = f.read()
    b64 = base64.b64encode(pdf_data).decode()
    download_link = f'<a href="data:application/octet-stream;base64,{b64}" download="{file_label}.pdf">Download PDF تحميل الملف</a>'
    return download_link
