import os
import base64
import re
from PyPDF2 import PdfReader, PdfWriter

def check_metadata(pdf_path):
    # Baca metadata PDF
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        metadata = pdf_reader.metadata
        for key, value in metadata.items():
            print(f"{key}: {value}")

def encode_pdf(pdf_path, logo_path):
    output_path_encoded = os.path.join(os.path.dirname(pdf_path), 'encoded_' + os.path.basename(pdf_path))
    output_path_original = os.path.join(os.path.dirname(pdf_path), 'original_' + os.path.basename(pdf_path))

    # Baca PDF asli
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        
        # Salin metadata asli
        metadata = pdf_reader.metadata
        
        # Salin halaman-halaman asli
        original_writer = PdfWriter()
        for page in pdf_reader.pages:
            original_writer.add_page(page)
        
        # Salin halaman-halaman dengan tambahan logo di awal
        encoded_writer = PdfWriter()
        logo_page = PdfReader(open(logo_path, 'rb')).pages[0]
        encoded_writer.add_page(logo_page)
        for page in pdf_reader.pages:
            encoded_writer.add_page(page)

        # Simpan PDF yang telah dimodifikasi dengan tambahan logo di awal
        with open(output_path_encoded, 'wb') as output_file_encoded:
            encoded_writer.write(output_file_encoded)

        # Simpan PDF asli
        with open(output_path_original, 'wb') as output_file_original:
            original_writer.write(output_file_original)
            
    print("Encoded PDF saved at:", output_path_encoded)
    print("Original PDF saved at:", output_path_original)
    return output_path_encoded, output_path_original

def decode_pdf(pdf_path):
    output_path = os.path.join(os.path.dirname(pdf_path), 'decoded_' + os.path.basename(pdf_path))
    # Baca PDF yang telah diencode
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        pdf_writer = PdfWriter()

        # Sembunyikan metadata dengan base64_encode dan aturan string replacement
        for page_num in range(len(pdf_reader.pages) - 1):  # Hindari halaman terakhir (metadata tersembunyi)
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            encoded_text = base64.b64encode(text.encode('utf-8')).decode('utf-8')
            decoded_text = re.sub(r'O=S', '', encoded_text)
            decoded_text = base64.b64decode(decoded_text).decode('utf-8')
            pdf_writer.add_page(PdfReader(decoded_text.encode('utf-8')).pages[0])

        # Simpan PDF yang telah didecode
        with open(output_path, 'wb') as output_file:
            pdf_writer.write(output_file)
    print("Decoded PDF saved at:", output_path)
    return output_path

# Contoh penggunaan:
# 1. Check metadata
check_metadata('tugaspdf.pdf')

# 2. Encode PDF
encoded_pdf_path, original_pdf_path = encode_pdf('tugaspdf.pdf', 'logo.pdf')

# 3. Decode PDF
decoded_pdf_path = decode_pdf(encoded_pdf_path)
