"""
Template Manager Module
Handles LaTeX template compilation to PDF based on role
"""
import subprocess
from pathlib import Path
from typing import Optional
import shutil


# Mapping of roles to template filenames
ROLE_TEMPLATE_MAP = {
    "Software Engineer": "yashwanth_resume_software_engineer.tex",
    "AI/ML Developer": "yashwanth_resume_AI_ML_engineer.tex",
    "Salesforce Developer": "yashwanth_resume_salesforce_developer.tex",
    "Salesforce Administrator": "yashwanth_resume_salesforce_administrator.tex"
}


def get_template_for_role(role: str) -> Optional[str]:
    """
    Get the template filename for a given role.
    
    Args:
        role: The job role selected by the user
        
    Returns:
        Template filename or None if role not found
    """
    return ROLE_TEMPLATE_MAP.get(role)


def compile_template_to_pdf(role: str, destination_folder: Path) -> bool:
    """
    Compile the appropriate LaTeX template to PDF and save in the destination folder.
    
    Args:
        role: The job role selected by the user
        destination_folder: Path object pointing to the resume folder
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Get the template filename for the role
        template_filename = get_template_for_role(role)
        
        if not template_filename:
            print(f"Error: No template found for role: {role}")
            return False
        
        # Get the templates directory
        backend_dir = Path(__file__).parent
        templates_dir = backend_dir.parent / "templates"
        
        # Source template path
        template_source = templates_dir / template_filename
        
        # Check if template exists
        if not template_source.exists():
            print(f"Error: Template file not found: {template_source}")
            return False
        
        # Get base name without extension
        base_name = template_filename.rsplit('.', 1)[0]
        
        # Output PDF filename
        pdf_filename = f"{base_name}.pdf"
        
        print(f"Compiling LaTeX template: {template_filename}")
        print(f"Template location: {template_source}")
        print(f"Output directory: {destination_folder}")
        
        # Run xelatex twice for references and formatting (better font support, required for fontspec package)
        # Using -output-directory to specify where to save the PDF
        # Using -interaction=nonstopmode to avoid stopping on errors
        print("Running xelatex (first pass)...")
        result1 = subprocess.run(
            [
                'xelatex',
                '-output-directory', str(destination_folder),
                '-interaction=nonstopmode',
                str(template_source)
            ],
            capture_output=True,
            text=True,
            timeout=30  # 30 second timeout
        )
        
        # Second pass for references
        print("Running xelatex (second pass)...")
        result = subprocess.run(
            [
                'xelatex',
                '-output-directory', str(destination_folder),
                '-interaction=nonstopmode',
                str(template_source)
            ],
            capture_output=True,
            text=True,
            timeout=30  # 30 second timeout
        )
        
        # Check if compilation was successful
        output_pdf = destination_folder / pdf_filename
        
        if result.returncode == 0 and output_pdf.exists():
            print(f"Successfully compiled PDF: {pdf_filename}")
            print(f"PDF saved to: {output_pdf}")
            
            # Clean up auxiliary files created by xelatex
            cleanup_aux_files(destination_folder, base_name)
            
            # Also save a copy directly in the resumes directory
            resumes_dir = destination_folder.parent  # Get the parent resumes directory
            resumes_pdf = resumes_dir / pdf_filename
            
            try:
                shutil.copy2(output_pdf, resumes_pdf)
                print(f"PDF also saved to: {resumes_pdf}")
            except Exception as e:
                print(f"Warning: Could not copy PDF to resumes directory: {e}")
            
            return True
        else:
            print(f"Error compiling LaTeX template")
            print(f"Return code: {result.returncode}")
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
            return False
        
    except subprocess.TimeoutExpired:
        print(f"Error: LaTeX compilation timed out")
        return False
    except FileNotFoundError:
        print(f"Error: xelatex not found. Please install LaTeX (e.g., texlive or mactex)")
        print(f"On macOS: brew install --cask mactex")
        print(f"After installation, restart your terminal or run: eval \"$(/usr/libexec/path_helper)\"")
        return False
    except Exception as e:
        print(f"Error compiling template: {str(e)}")
        return False


def cleanup_aux_files(folder: Path, base_name: str):
    """
    Clean up auxiliary files created by pdflatex.
    
    Args:
        folder: Directory containing the auxiliary files
        base_name: Base name of the LaTeX file (without extension)
    """
    aux_extensions = ['.aux', '.log', '.out', '.toc', '.lof', '.lot']
    
    for ext in aux_extensions:
        aux_file = folder / f"{base_name}{ext}"
        if aux_file.exists():
            try:
                aux_file.unlink()
                print(f"Cleaned up: {aux_file.name}")
            except Exception as e:
                print(f"Could not delete {aux_file.name}: {e}")


def get_available_templates() -> dict:
    """
    Get all available templates and their roles.
    
    Returns:
        Dictionary mapping roles to template filenames
    """
    return ROLE_TEMPLATE_MAP.copy()
