#!/usr/bin/env python3
"""
OCR Document Processing Script for Tax FY24-25

Extracts dates from tax documents (PDFs, images) and renames files to YYMMdd format.
Documents that cannot be processed are moved to NEEDS MANUAL PROCESSING/ folder.

Usage:
    python scripts/ocr_processor.py --dry-run          # Preview changes
    python scripts/ocr_processor.py --execute          # Apply changes
    python scripts/ocr_processor.py --folder "1. Income/Thomas"  # Process specific folder
"""

import os
import re
import sys
import json
import shutil
import subprocess
import argparse
from pathlib import Path
from datetime import datetime, date
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Tuple
from enum import Enum
import time

# OCR dependencies
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io


class ProcessingStatus(Enum):
    SUCCESS = "success"
    NO_DATE = "no_date"
    AMBIGUOUS_DATE = "ambiguous_date"
    OCR_FAILED = "ocr_failed"
    UNSUPPORTED_TYPE = "unsupported_type"
    OUTSIDE_FY = "outside_fy"
    ALREADY_NAMED = "already_named"
    SKIPPED = "skipped"


@dataclass
class ProcessingResult:
    """Result of processing a single document."""
    original_path: str
    status: ProcessingStatus
    extracted_date: Optional[date] = None
    suggested_name: Optional[str] = None
    confidence: float = 0.0
    extracted_text_preview: str = ""
    error_message: str = ""
    dates_found: List[str] = field(default_factory=list)


# FY24-25 date range
FY_START = date(2024, 7, 1)
FY_END = date(2025, 6, 30)

# File extensions to process
SUPPORTED_EXTENSIONS = {'.pdf', '.png', '.jpg', '.jpeg', '.gif', '.tiff', '.tif', '.PNG', '.PDF', '.JPG', '.JPEG'}

# Folders to skip
SKIP_FOLDERS = {'.git', '.github', '.venv', '.beads', 'scripts', 'NEEDS MANUAL PROCESSING'}

# Pattern for files already named in YYMMdd format
ALREADY_NAMED_PATTERN = re.compile(r'^\d{6}\s*-\s*.+')

# Date patterns to search for (in order of preference)
DATE_PATTERNS = [
    # ISO format: 2024-08-15
    (r'(\d{4})-(\d{1,2})-(\d{1,2})', 'ymd'),
    # Australian format: 15/08/2024 or 15-08-2024 or 15.08.2024
    (r'(\d{1,2})[/\-.](\d{1,2})[/\-.](\d{4})', 'dmy'),
    # Written: 15 August 2024, August 15, 2024
    (r'(\d{1,2})\s+(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+(\d{4})', 'dMy'),
    (r'(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+(\d{1,2}),?\s+(\d{4})', 'Mdy'),
    # Short format: 15/08/24 or 15.08.24
    (r'(\d{1,2})[/\-.](\d{1,2})[/\-.](\d{2})\b', 'dmy_short'),
    # YYYYMMDD format: 20241230
    (r'\b(20[234]\d)(\d{2})(\d{2})\b', 'yyyymmdd'),
    # YYMMDD in filename: 241230
    (r'\b(2[45])(\d{2})(\d{2})\b', 'yymmdd'),
    # Spaced date: 2024 08 30 or 10 August 2024
    (r'(\d{4})\s+(\d{2})\s+(\d{2})', 'ymd_spaced'),
    (r'(\d{1,2})\s+(\d{2})\s+(\d{4})', 'dmy_spaced'),
]

MONTH_MAP = {
    'jan': 1, 'january': 1,
    'feb': 2, 'february': 2,
    'mar': 3, 'march': 3,
    'apr': 4, 'april': 4,
    'may': 5,
    'jun': 6, 'june': 6,
    'jul': 7, 'july': 7,
    'aug': 8, 'august': 8,
    'sep': 9, 'september': 9,
    'oct': 10, 'october': 10,
    'nov': 11, 'november': 11,
    'dec': 12, 'december': 12,
}


def parse_date_match(match: re.Match, format_type: str) -> Optional[date]:
    """Parse a regex match into a date object."""
    try:
        groups = match.groups()
        
        if format_type == 'ymd':
            year, month, day = int(groups[0]), int(groups[1]), int(groups[2])
        elif format_type == 'ymd_spaced':
            year, month, day = int(groups[0]), int(groups[1]), int(groups[2])
        elif format_type == 'dmy':
            day, month, year = int(groups[0]), int(groups[1]), int(groups[2])
        elif format_type == 'dmy_spaced':
            day, month, year = int(groups[0]), int(groups[1]), int(groups[2])
        elif format_type == 'dmy_short':
            day, month, year = int(groups[0]), int(groups[1]), int(groups[2])
            year = 2000 + year if year < 50 else 1900 + year
        elif format_type == 'dMy':
            day = int(groups[0])
            month = MONTH_MAP.get(groups[1].lower()[:3], 0)
            year = int(groups[2])
        elif format_type == 'Mdy':
            month = MONTH_MAP.get(groups[0].lower()[:3], 0)
            day = int(groups[1])
            year = int(groups[2])
        elif format_type == 'yymmdd':
            year = 2000 + int(groups[0])
            month = int(groups[1])
            day = int(groups[2])
        elif format_type == 'yyyymmdd':
            year = int(groups[0])
            month = int(groups[1])
            day = int(groups[2])
        else:
            return None
        
        if 1 <= month <= 12 and 1 <= day <= 31:
            return date(year, month, day)
    except (ValueError, IndexError):
        pass
    return None


def extract_text_from_pdf(pdf_path: Path) -> Tuple[str, bool]:
    """
    Extract text from PDF. Returns (text, is_ocr_needed).
    First tries direct text extraction, then falls back to OCR.
    """
    try:
        doc = fitz.open(pdf_path)
        text = ""
        
        # Try direct text extraction first
        for page in doc:
            text += page.get_text()
        
        # If we got meaningful text, return it
        if len(text.strip()) > 50:
            doc.close()
            return text, False
        
        # Fall back to OCR for scanned PDFs
        ocr_text = ""
        for page_num in range(len(doc)):
            page = doc[page_num]
            # Render page to image
            mat = fitz.Matrix(2, 2)  # 2x zoom for better OCR
            pix = page.get_pixmap(matrix=mat)
            img_data = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_data))
            
            # OCR the image
            page_text = pytesseract.image_to_string(img)
            ocr_text += page_text + "\n"
        
        doc.close()
        return ocr_text, True
        
    except Exception as e:
        return f"Error: {str(e)}", True


def extract_text_from_image(image_path: Path) -> str:
    """Extract text from image using OCR."""
    try:
        img = Image.open(image_path)
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        return f"Error: {str(e)}"


def extract_dates_from_text(text: str, filename: str = "") -> List[Tuple[date, float, str]]:
    """
    Extract all dates from text and filename.
    Returns list of (date, confidence, source) tuples.
    """
    dates_found = []
    
    # Also check the filename
    combined_text = f"{filename}\n{text}"
    
    for pattern, format_type in DATE_PATTERNS:
        for match in re.finditer(pattern, combined_text, re.IGNORECASE):
            parsed_date = parse_date_match(match, format_type)
            if parsed_date:
                # Higher confidence for dates in FY range
                confidence = 0.8
                if FY_START <= parsed_date <= FY_END:
                    confidence = 1.0
                elif parsed_date.year in (2024, 2025):
                    confidence = 0.9
                
                # Higher confidence for certain patterns
                if format_type in ('ymd', 'dmy'):
                    confidence *= 1.0
                elif format_type == 'yymmdd':
                    confidence *= 0.7  # Filename dates are less reliable
                
                dates_found.append((parsed_date, confidence, match.group()))
    
    # Remove duplicates, keeping highest confidence
    unique_dates = {}
    for d, conf, source in dates_found:
        if d not in unique_dates or conf > unique_dates[d][0]:
            unique_dates[d] = (conf, source)
    
    return [(d, conf, src) for d, (conf, src) in unique_dates.items()]


def select_best_date(dates: List[Tuple[date, float, str]]) -> Tuple[Optional[date], float, List[str]]:
    """
    Select the best date from candidates.
    Prefers dates within FY24-25, then most recent, then highest confidence.
    """
    if not dates:
        return None, 0.0, []
    
    # Filter to FY dates first
    fy_dates = [(d, c, s) for d, c, s in dates if FY_START <= d <= FY_END]
    
    if fy_dates:
        # Sort by confidence, then by date (most recent first)
        fy_dates.sort(key=lambda x: (x[1], x[0]), reverse=True)
        best = fy_dates[0]
        return best[0], best[1], [s for _, _, s in dates]
    
    # No FY dates - check if there are dates close to FY
    close_dates = [(d, c, s) for d, c, s in dates if d.year in (2024, 2025)]
    if close_dates:
        close_dates.sort(key=lambda x: (x[1], x[0]), reverse=True)
        best = close_dates[0]
        return best[0], best[1] * 0.5, [s for _, _, s in dates]  # Lower confidence for out-of-FY
    
    return None, 0.0, [s for _, _, s in dates]


def generate_new_filename(original_path: Path, extracted_date: date) -> str:
    """Generate new filename in YYMMdd - Description.ext format."""
    date_prefix = extracted_date.strftime('%y%m%d')
    
    # Clean up the original filename for description
    stem = original_path.stem
    
    # Remove existing date prefixes
    stem = re.sub(r'^\d{6}\s*-\s*', '', stem)
    stem = re.sub(r'^\d{4}[-_]\d{2}[-_]\d{2}\s*', '', stem)
    stem = re.sub(r'^\d{2}[-_/.]\d{2}[-_/.]\d{2,4}\s*', '', stem)
    stem = re.sub(r'^\d{8}\s*', '', stem)  # YYYYMMDD
    
    # Clean up common patterns
    stem = stem.strip(' -_')
    
    # Capitalize first letter if all lowercase
    if stem and stem[0].islower():
        stem = stem[0].upper() + stem[1:]
    
    # Preserve original extension
    ext = original_path.suffix
    
    return f"{date_prefix} - {stem}{ext}"


def process_document(file_path: Path) -> ProcessingResult:
    """Process a single document and return the result."""
    result = ProcessingResult(original_path=str(file_path), status=ProcessingStatus.SKIPPED)
    
    # Check if already named correctly
    if ALREADY_NAMED_PATTERN.match(file_path.name):
        result.status = ProcessingStatus.ALREADY_NAMED
        return result
    
    # Check file extension
    if file_path.suffix.lower() not in {s.lower() for s in SUPPORTED_EXTENSIONS}:
        result.status = ProcessingStatus.UNSUPPORTED_TYPE
        result.error_message = f"Unsupported file type: {file_path.suffix}"
        return result
    
    # Extract text based on file type
    try:
        if file_path.suffix.lower() == '.pdf':
            text, used_ocr = extract_text_from_pdf(file_path)
        else:
            text = extract_text_from_image(file_path)
            used_ocr = True
        
        if text.startswith("Error:"):
            result.status = ProcessingStatus.OCR_FAILED
            result.error_message = text
            return result
        
        result.extracted_text_preview = text[:500] if text else ""
        
    except Exception as e:
        result.status = ProcessingStatus.OCR_FAILED
        result.error_message = str(e)
        return result
    
    # Extract dates
    dates = extract_dates_from_text(text, file_path.name)
    best_date, confidence, all_dates = select_best_date(dates)
    
    result.dates_found = all_dates
    result.confidence = confidence
    
    if not best_date:
        # Try file metadata as fallback
        try:
            stat = file_path.stat()
            mtime = datetime.fromtimestamp(stat.st_mtime).date()
            if FY_START <= mtime <= FY_END:
                best_date = mtime
                confidence = 0.3
                result.dates_found.append(f"file_mtime:{mtime}")
        except:
            pass
    
    if not best_date:
        result.status = ProcessingStatus.NO_DATE
        result.error_message = "No date could be extracted from document"
        return result
    
    # Check if date is in FY range
    if not (FY_START <= best_date <= FY_END):
        # Allow dates just outside if they might be valid (e.g., statement dated Jul 2025 covering Jun)
        if best_date.year in (2024, 2025):
            result.status = ProcessingStatus.OUTSIDE_FY
            result.error_message = f"Date {best_date} is outside FY24-25 (Jul 2024 - Jun 2025)"
        else:
            result.status = ProcessingStatus.OUTSIDE_FY
            result.error_message = f"Date {best_date} is well outside FY24-25"
            return result
    
    result.extracted_date = best_date
    result.suggested_name = generate_new_filename(file_path, best_date)
    result.status = ProcessingStatus.SUCCESS
    
    return result


def find_documents(root_path: Path, specific_folder: Optional[str] = None) -> List[Path]:
    """Find all documents to process."""
    documents = []
    
    if specific_folder:
        search_path = root_path / specific_folder
        if not search_path.exists():
            print(f"Warning: Folder not found: {specific_folder}")
            return documents
    else:
        search_path = root_path
    
    for file_path in search_path.rglob('*'):
        if file_path.is_file():
            # Skip files in excluded folders
            if any(skip in file_path.parts for skip in SKIP_FOLDERS):
                continue
            
            # Skip hidden files and temp files
            if file_path.name.startswith('.') or file_path.name.startswith('~'):
                continue
            
            # Skip markdown and other non-document files
            if file_path.suffix.lower() in {'.md', '.csv', '.xlsx', '.json', '.py', '.txt'}:
                continue
            
            # Only process supported extensions
            if file_path.suffix.lower() in {s.lower() for s in SUPPORTED_EXTENSIONS}:
                documents.append(file_path)
    
    return sorted(documents)


def print_results_table(results: List[ProcessingResult]):
    """Print a formatted table of processing results."""
    print("\n" + "=" * 100)
    print("DOCUMENT PROCESSING RESULTS")
    print("=" * 100)
    
    # Group by status
    success = [r for r in results if r.status == ProcessingStatus.SUCCESS]
    already_named = [r for r in results if r.status == ProcessingStatus.ALREADY_NAMED]
    needs_review = [r for r in results if r.status in (
        ProcessingStatus.NO_DATE, ProcessingStatus.AMBIGUOUS_DATE,
        ProcessingStatus.OCR_FAILED, ProcessingStatus.UNSUPPORTED_TYPE,
        ProcessingStatus.OUTSIDE_FY
    )]
    
    if success:
        print(f"\n✅ READY TO RENAME ({len(success)} files)")
        print("-" * 100)
        print(f"{'Current Name':<50} {'Date':<12} {'New Name':<35} {'Conf'}")
        print("-" * 100)
        for r in success:
            current = Path(r.original_path).name[:48]
            new_name = r.suggested_name[:33] if r.suggested_name else "N/A"
            date_str = r.extracted_date.strftime('%Y-%m-%d') if r.extracted_date else "N/A"
            conf = f"{r.confidence:.0%}"
            print(f"{current:<50} {date_str:<12} {new_name:<35} {conf}")
    
    if already_named:
        print(f"\n⏭️  ALREADY NAMED ({len(already_named)} files)")
        print("-" * 100)
        for r in already_named:
            print(f"  {Path(r.original_path).name}")
    
    if needs_review:
        print(f"\n⚠️  NEEDS MANUAL REVIEW ({len(needs_review)} files)")
        print("-" * 100)
        print(f"{'File':<50} {'Status':<20} {'Reason'}")
        print("-" * 100)
        for r in needs_review:
            name = Path(r.original_path).name[:48]
            status = r.status.value
            reason = r.error_message[:40] if r.error_message else "Unknown"
            print(f"{name:<50} {status:<20} {reason}")
    
    print("\n" + "=" * 100)
    print(f"SUMMARY: {len(success)} ready | {len(already_named)} already named | {len(needs_review)} need review")
    print("=" * 100)


def move_to_manual_processing(root_path: Path, results: List[ProcessingResult]) -> List[str]:
    """Move failed documents to NEEDS MANUAL PROCESSING folder."""
    manual_folder = root_path / "NEEDS MANUAL PROCESSING"
    manual_folder.mkdir(exist_ok=True)
    
    moved = []
    needs_review = [r for r in results if r.status in (
        ProcessingStatus.NO_DATE, ProcessingStatus.AMBIGUOUS_DATE,
        ProcessingStatus.OCR_FAILED
    )]
    
    for r in needs_review:
        src = Path(r.original_path)
        if src.exists():
            # Create a unique destination name if needed
            dest = manual_folder / src.name
            if dest.exists():
                stem = src.stem
                suffix = src.suffix
                counter = 1
                while dest.exists():
                    dest = manual_folder / f"{stem}_{counter}{suffix}"
                    counter += 1
            
            try:
                shutil.move(str(src), str(dest))
                moved.append(f"{src.name} -> NEEDS MANUAL PROCESSING/")
            except Exception as e:
                print(f"Error moving {src.name}: {e}")
    
    # Create a summary file
    if moved:
        summary_path = manual_folder / "PROCESSING_FAILED.md"
        with open(summary_path, 'w') as f:
            f.write("# Documents Requiring Manual Processing\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("These documents could not be automatically processed.\n")
            f.write("Please review and rename manually using format: `YYMMdd - Description.ext`\n\n")
            
            for r in needs_review:
                f.write(f"## {Path(r.original_path).name}\n")
                f.write(f"- **Status:** {r.status.value}\n")
                f.write(f"- **Reason:** {r.error_message}\n")
                if r.dates_found:
                    f.write(f"- **Dates found:** {', '.join(r.dates_found)}\n")
                f.write("\n")
    
    return moved


def execute_renames(root_path: Path, results: List[ProcessingResult], use_git: bool = True) -> List[str]:
    """Execute the file renames."""
    renamed = []
    success_results = [r for r in results if r.status == ProcessingStatus.SUCCESS and r.suggested_name]
    
    for r in success_results:
        src = Path(r.original_path)
        if not src.exists():
            continue
        
        dest = src.parent / r.suggested_name
        
        # Skip if destination already exists
        if dest.exists():
            print(f"⚠️  Skipping {src.name} - destination exists")
            continue
        
        try:
            if use_git:
                # Use git mv for tracking
                result = subprocess.run(
                    ['git', 'mv', str(src), str(dest)],
                    cwd=str(root_path),
                    capture_output=True,
                    text=True
                )
                if result.returncode != 0:
                    # Fall back to regular move if git mv fails
                    shutil.move(str(src), str(dest))
            else:
                shutil.move(str(src), str(dest))
            
            renamed.append(f"{src.name} -> {r.suggested_name}")
            
        except Exception as e:
            print(f"❌ Error renaming {src.name}: {e}")
    
    return renamed


def save_manifest(root_path: Path, results: List[ProcessingResult]):
    """Save processing results to a manifest file."""
    manifest_path = root_path / "document_manifest.json"
    
    manifest = {
        "generated": datetime.now().isoformat(),
        "fy_range": f"{FY_START} to {FY_END}",
        "total_processed": len(results),
        "results": []
    }
    
    for r in results:
        entry = {
            "original_path": r.original_path,
            "status": r.status.value,
            "extracted_date": r.extracted_date.isoformat() if r.extracted_date else None,
            "suggested_name": r.suggested_name,
            "confidence": r.confidence,
            "dates_found": r.dates_found,
            "error_message": r.error_message
        }
        manifest["results"].append(entry)
    
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"\n📄 Manifest saved to: {manifest_path}")


def main():
    parser = argparse.ArgumentParser(description='OCR Document Processor for Tax FY24-25')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without applying')
    parser.add_argument('--execute', action='store_true', help='Apply changes')
    parser.add_argument('--folder', type=str, help='Process specific folder only')
    parser.add_argument('--no-git', action='store_true', help='Do not use git mv for renames')
    parser.add_argument('--move-failed', action='store_true', help='Move failed documents to NEEDS MANUAL PROCESSING')
    
    args = parser.parse_args()
    
    # Determine root path
    root_path = Path(__file__).parent.parent
    print(f"📁 Working directory: {root_path}")
    
    # Find documents
    print(f"\n🔍 Scanning for documents...")
    documents = find_documents(root_path, args.folder)
    print(f"   Found {len(documents)} documents to process")
    
    if not documents:
        print("No documents found to process.")
        return
    
    # Process each document
    print(f"\n⚙️  Processing documents...")
    results = []
    for i, doc_path in enumerate(documents, 1):
        print(f"   [{i}/{len(documents)}] {doc_path.name[:50]}...", end=" ", flush=True)
        result = process_document(doc_path)
        results.append(result)
        
        status_emoji = {
            ProcessingStatus.SUCCESS: "✅",
            ProcessingStatus.ALREADY_NAMED: "⏭️",
            ProcessingStatus.NO_DATE: "❓",
            ProcessingStatus.OCR_FAILED: "❌",
            ProcessingStatus.OUTSIDE_FY: "📅",
            ProcessingStatus.UNSUPPORTED_TYPE: "⚠️",
        }.get(result.status, "❔")
        print(status_emoji)
    
    # Print results table
    print_results_table(results)
    
    # Save manifest
    save_manifest(root_path, results)
    
    # Handle execution
    if args.dry_run:
        print("\n🔍 DRY RUN - No changes made")
        print("   Run with --execute to apply changes")
        
    elif args.execute:
        # Confirm before executing
        success_count = len([r for r in results if r.status == ProcessingStatus.SUCCESS])
        if success_count == 0:
            print("\n❌ No files ready to rename")
            return
        
        print(f"\n⚠️  About to rename {success_count} files")
        response = input("   Continue? [y/N]: ").strip().lower()
        
        if response == 'y':
            renamed = execute_renames(root_path, results, use_git=not args.no_git)
            print(f"\n✅ Renamed {len(renamed)} files:")
            for r in renamed:
                print(f"   {r}")
            
            if args.move_failed:
                moved = move_to_manual_processing(root_path, results)
                if moved:
                    print(f"\n📁 Moved {len(moved)} files to NEEDS MANUAL PROCESSING/")
        else:
            print("   Cancelled")
    
    else:
        print("\n💡 Run with --dry-run to preview or --execute to apply changes")


if __name__ == "__main__":
    main()
