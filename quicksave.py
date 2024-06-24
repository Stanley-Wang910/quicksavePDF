import os
import argparse
from docx2pdf import convert

def convert_docx_to_pdf(docx_path):
    # Check if file exists, and is .docx
    if not os.path.isfile(docx_path) or not docx_path.endswith('.docx'): 
        raise ValueError('Invalid file path/type')

    # Generate the PDF file path
    pdf_path = docx_path.replace('.docx', '.pdf')

    # Convert the docx file to PDF
    convert(docx_path, pdf_path)

    print(f'Converted {docx_path} to {pdf_path}')
    return pdf_path

def replace_existing_pdf(pdf_path):
    if os.path.isfile(pdf_path):
        os.remove(pdf_path)
        print(f'Removed existing {pdf_path}')   
    
def main():
    parser = argparse.ArgumentParser(description='Convert a .docx file to a .pdf file')
    parser.add_argument('docx_path', type=str, help='Path to the .docx file')

    args = parser.parse_args()
    docx_path = args.docx_path
    pdf_path = docx_path.replace('.docx', '.pdf')

    replace_existing_pdf(pdf_path)

    convert_docx_to_pdf(docx_path)

if __name__ == "__main__":
    main()

