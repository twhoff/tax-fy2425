#!/bin/bash
# Batch OCR script - adds searchable text layer to all PDFs
# Uses ocrmypdf with --skip-text to skip already-OCR'd files

WORKSPACE="/Users/twhoffmann/Library/CloudStorage/GoogleDrive-hoffmatw@gmail.com/My Drive/Filing Cabinet/Australia/Tax/Tax 2024-2025"
cd "$WORKSPACE"
source .venv/bin/activate

TOTAL=$(find "$WORKSPACE" -name "*.pdf" -type f | wc -l | tr -d ' ')
COUNT=0
SUCCESS=0
SKIPPED=0
FAILED=0

echo "========================================"
echo "PDF OCR Batch Processing"
echo "========================================"
echo "Total PDFs to process: $TOTAL"
echo ""

find "$WORKSPACE" -name "*.pdf" -type f | while read -r pdf; do
    COUNT=$((COUNT + 1))
    filename=$(basename "$pdf")
    
    echo "[$COUNT/$TOTAL] Processing: $filename"
    
    # Create temp file for output
    temp_pdf="${pdf}.tmp"
    
    # Run ocrmypdf with --skip-text (skips pages that already have text)
    output=$(ocrmypdf --skip-text --optimize 1 "$pdf" "$temp_pdf" 2>&1)
    exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        # Replace original with OCR'd version
        mv "$temp_pdf" "$pdf"
        echo "         ✓ Done (OCR added)"
        SUCCESS=$((SUCCESS + 1))
    elif [ $exit_code -eq 6 ]; then
        # Exit code 6 = already has text layer, nothing to do
        rm -f "$temp_pdf" 2>/dev/null
        echo "         ⏭ Skipped (already has text)"
        SKIPPED=$((SKIPPED + 1))
    else
        rm -f "$temp_pdf" 2>/dev/null
        echo "         ✗ Failed: $output"
        FAILED=$((FAILED + 1))
    fi
done

echo ""
echo "========================================"
echo "COMPLETE"
echo "========================================"
echo "OCR Added: $SUCCESS"
echo "Skipped:   $SKIPPED"
echo "Failed:    $FAILED"
