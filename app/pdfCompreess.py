import PyPDF2
import os
import io
def compress_pdf(input_path, output_path, target_size_kb):
    # Open the input PDF file
    with open(input_path, 'rb') as input_file:
        pdf_reader = PyPDF2.PdfReader(input_file)
        pdf_writer = PyPDF2.PdfWriter()

        # Iterate through each page of the PDF
        for page_num in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page_num])

        # Create a BytesIO object to write the compressed PDF
        output_buffer = io.BytesIO()
        pdf_writer.write(output_buffer)

        # Get the size of the compressed PDF
        output_size_kb = len(output_buffer.getvalue()) / 1024

        # If the output size is already smaller than the target size, just write the original PDF
        if output_size_kb <= target_size_kb:
            with open(output_path, 'wb') as output_file:
                output_buffer.seek(0)
                output_file.write(output_buffer.read())
            print("Compression not needed. Output size:", output_size_kb, "KB")
            return

        # Calculate the compression ratio required
        compression_ratio = target_size_kb / output_size_kb

        # Create a new PDF writer with the required compression
        pdf_writer = PyPDF2.PdfWriter()
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            page.compress_content_streams()
            pdf_writer.add_page(page)

        # Write the compressed PDF to the output file
        with open(output_path, 'wb') as output_file:
            pdf_writer.write(output_file)

        print("PDF compressed successfully. Original size:", output_size_kb, "KB. Target size:", target_size_kb, "KB")

# Example usage
input_pdf_path = 'aot.pdf'  # Replace with the path to your input PDF file
output_pdf_path = 'compressed_output.pdf'  # Replace with the desired output path
target_size_kb = 500  # Replace with the target size in KB

compress_pdf(input_pdf_path, output_pdf_path, target_size_kb)
