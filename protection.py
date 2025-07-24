import PyPDF2
import os
import getpass
import sys
from pathlib import Path

def validate_file_path(file_path, check_exists=True):
    """Validate file path and check if it exists (for input files)"""
    if not file_path.strip():
        return False, "File path cannot be empty."
    
    path = Path(file_path)
    
    if check_exists:
        if not path.exists():
            return False, f"File '{file_path}' does not exist."
        if not path.is_file():
            return False, f"'{file_path}' is not a file."
        if path.suffix.lower() != '.pdf':
            return False, f"'{file_path}' is not a PDF file."
    else:
        # For output files, check if directory exists
        parent_dir = path.parent
        if not parent_dir.exists():
            return False, f"Directory '{parent_dir}' does not exist."
        
        # Add .pdf extension if not present
        if path.suffix.lower() != '.pdf':
            return False, "Output file must have .pdf extension."
    
    return True, ""

def get_password():
    """Get password with confirmation and strength check"""
    while True:
        password = getpass.getpass("Enter password for PDF encryption: ")
        
        if len(password) < 4:
            print("⚠️  Password should be at least 4 characters long.")
            continue
        
        confirm_password = getpass.getpass("Confirm password: ")
        
        if password != confirm_password:
            print("❌ Passwords don't match. Please try again.")
            continue
        
        # Basic password strength check
        strength = check_password_strength(password)
        print(f"Password strength: {strength}")
        
        if strength == "Weak":
            choice = input("Password is weak. Continue anyway? (y/n): ").lower()
            if choice != 'y':
                continue
        
        return password

def check_password_strength(password):
    """Basic password strength checker"""
    score = 0
    
    if len(password) >= 8:
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        score += 1
    
    if score >= 4:
        return "Strong"
    elif score >= 2:
        return "Medium"
    else:
        return "Weak"

def get_file_info(pdf_path):
    """Get basic information about the PDF"""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)
            is_encrypted = reader.is_encrypted
            
            # Try to get metadata
            metadata = reader.metadata
            title = metadata.get('/Title', 'N/A') if metadata else 'N/A'
            author = metadata.get('/Author', 'N/A') if metadata else 'N/A'
            
            return {
                'pages': num_pages,
                'encrypted': is_encrypted,
                'title': title,
                'author': author,
                'size': os.path.getsize(pdf_path)
            }
    except Exception:
        return None

def format_file_size(size_bytes):
    """Convert bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

def create_password_protected_pdf(input_pdf, output_pdf, password, compression_level=None):
    """Create password-protected PDF with optional compression"""
    try:
        with open(input_pdf, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            # Check if already encrypted
            if pdf_reader.is_encrypted:
                print("⚠️  Input PDF is already encrypted!")
                decrypt_choice = input("Do you want to decrypt it first? You'll need the current password (y/n): ").lower()
                if decrypt_choice == 'y':
                    current_password = getpass.getpass("Enter current password: ")
                    try:
                        pdf_reader.decrypt(current_password)
                        print("✅ PDF successfully decrypted.")
                    except Exception:
                        print("❌ Failed to decrypt PDF. Incorrect password.")
                        return False
                else:
                    print("❌ Cannot proceed with already encrypted PDF.")
                    return False
            
            pdf_writer = PyPDF2.PdfWriter()
            
            # Copy all pages
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                
                # Apply compression if requested
                if compression_level:
                    page.compress_content_streams()
                
                pdf_writer.add_page(page)
            
            # Copy metadata if available
            if pdf_reader.metadata:
                pdf_writer.add_metadata(pdf_reader.metadata)
            
            # Encrypt the PDF
            pdf_writer.encrypt(password)
            
            # Write to output file
            with open(output_pdf, 'wb') as output_file:
                pdf_writer.write(output_file)
            
            return True
        
    except FileNotFoundError:
        print(f"❌ The file '{input_pdf}' was not found.")
        return False
    except PyPDF2.errors.PdfReadError as e:
        print(f"❌ Error reading PDF: {e}")
        return False
    except PermissionError:
        print(f"❌ Permission denied. Cannot write to '{output_pdf}'.")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    print("🔒 PDF Encryption Tool")
    print("=" * 50)
    
    # Get input PDF file
    while True:
        input_pdf = input("Enter input PDF file path: ").strip()
        
        # Remove quotes if present
        input_pdf = input_pdf.strip('"\'')
        
        valid, error_msg = validate_file_path(input_pdf, check_exists=True)
        if valid:
            break
        else:
            print(f"❌ {error_msg}")
    
    # Display file information
    print("\n📄 File Information:")
    file_info = get_file_info(input_pdf)
    if file_info:
        print(f"   Pages: {file_info['pages']}")
        print(f"   Size: {format_file_size(file_info['size'])}")
        print(f"   Already encrypted: {'Yes' if file_info['encrypted'] else 'No'}")
        if file_info['title'] != 'N/A':
            print(f"   Title: {file_info['title']}")
        if file_info['author'] != 'N/A':
            print(f"   Author: {file_info['author']}")
    
    # Get output PDF file
    while True:
        output_pdf = input("\nEnter output PDF file path: ").strip()
        
        # Remove quotes if present
        output_pdf = output_pdf.strip('"\'')
        
        # Auto-add .pdf extension if missing
        if not output_pdf.lower().endswith('.pdf'):
            output_pdf += '.pdf'
        
        valid, error_msg = validate_file_path(output_pdf, check_exists=False)
        if valid:
            # Check if file already exists
            if os.path.exists(output_pdf):
                overwrite = input(f"File '{output_pdf}' already exists. Overwrite? (y/n): ").lower()
                if overwrite != 'y':
                    continue
            break
        else:
            print(f"❌ {error_msg}")
    
    # Get password
    print("\n🔑 Password Setup:")
    password = get_password()
    
    # Ask for compression
    print("\n⚙️  Additional Options:")
    compress = input("Enable compression to reduce file size? (y/n): ").lower() == 'y'
    
    # Create encrypted PDF
    print(f"\n🔄 Encrypting PDF...")
    
    success = create_password_protected_pdf(
        input_pdf, 
        output_pdf, 
        password, 
        compression_level=compress
    )
    
    if success:
        # Show results
        input_size = os.path.getsize(input_pdf)
        output_size = os.path.getsize(output_pdf)
        
        print(f"\n✅ Success! Password-protected PDF created.")
        print(f"📁 Output file: {output_pdf}")
        print(f"📊 Original size: {format_file_size(input_size)}")
        print(f"📊 New size: {format_file_size(output_size)}")
        
        if compress:
            reduction = ((input_size - output_size) / input_size) * 100
            if reduction > 0:
                print(f"📉 Size reduction: {reduction:.1f}%")
            else:
                print(f"📈 Size increase: {abs(reduction):.1f}% (due to encryption overhead)")
        
        print("\n🛡️  Your PDF is now protected with a password!")
    else:
        print("\n❌ Failed to create encrypted PDF.")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Operation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
