#!/bin/bash

PDF_FILE="/home/ctai-manhdd10-d/Documents/docling-chunking/input/THUYỀN KAYAK.pdf"

if [ ! -f "$PDF_FILE" ]; then
    echo "File không tồn tại: $PDF_FILE"
    exit 1
fi

curl -X 'POST' \
  'http://0.0.0.0:8074/upload_pdf/' \
  -F "file=@${PDF_FILE}" \
  -o "output.json"

echo "Kết quả đã được lưu vào file Output.json"
