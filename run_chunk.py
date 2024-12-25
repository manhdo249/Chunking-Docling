import os
from docling.document_converter import DocumentConverter
from docling_core.transforms.chunker import HierarchicalChunker

input_path = "/home/ctai-manhdd10-d/Documents/docling-chunking/input/Câu hỏi thường gặp VF8.pdf"

conv_res = DocumentConverter().convert(input_path)
doc = conv_res.document

chunks = list(HierarchicalChunker().chunk(doc))
print(len(chunks))
# print(chunks[0].text)
# print(chunks[0].meta.headings)

base_dir = 'results'
pdf_name = os.path.splitext(os.path.basename(input_path))[0]  
output_dir = os.path.join(base_dir, pdf_name)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

chunks_file_path = os.path.join(output_dir, 'chunks.txt')

with open(chunks_file_path, 'w') as file:
    for i in range(len(chunks)):
        doc_items = chunks[i].meta.doc_items
        ref_text = chunks[i].text
        title = chunks[i].meta.headings
        
        for index, item in enumerate(doc_items):
            file.write(f"-----Ref_text_{i}----- \n -----Chunk_{index + 1}-----\n")  
            file.write(f"Chunk_content: {item.orig}\n")
            file.write(f"Ref_text:\n{ref_text}\n")
            file.write(f"Title: {title}\n")
            file.write("\n")



