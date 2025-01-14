# from fastapi import FastAPI, UploadFile, File
# from docling.document_converter import DocumentConverter
# from docling_core.transforms.chunker import HierarchicalChunker
# from docling.chunking import HybridChunker

# from decouple import config
# import io
# import os
# import time 

# def merge_chunks_by_title(chunk_data, max_length=512):
#     """
#     Gộp các chunk có độ dài nhỏ hơn `max_length` trong cùng một `Title` 
#     và đảm bảo ChunkIndex được đánh số lại.

#     Args:
#         chunk_data (list): Danh sách các chunk dưới dạng dictionary.
#         max_length (int): Độ dài tối đa cho mỗi chunk. Mặc định là 512.

#     Returns:
#         list: Danh sách các chunk đã được gộp và đánh số lại `ChunkIndex`.
#     """
#     merged_data = []
#     temp_chunk = ""
#     temp_group_index = None
#     temp_ref_text = ""
#     temp_title = ""
#     new_chunk_index = 1   

#     for chunk in chunk_data:
#         chunk_content = chunk["Chunk"]
#         group_index = chunk["GroupIndex"]
#         ref_text = chunk["RefText"]
#         title = chunk["Title"]

#         if not temp_chunk or temp_title != title:
#             if temp_chunk:
#                 merged_data.append({
#                     "ChunkIndex": new_chunk_index,  
#                     "Chunk": temp_chunk,
#                     "GroupIndex": temp_group_index,
#                     "RefText": temp_ref_text,
#                     "Title": temp_title,
#                 })
#                 new_chunk_index += 1  

#             temp_chunk = chunk_content
#             temp_group_index = group_index
#             temp_ref_text = ref_text
#             temp_title = title
#         elif len(temp_chunk) + len(chunk_content) < max_length:
#             temp_chunk += " " + chunk_content
#         else:
#             merged_data.append({
#                 "ChunkIndex": new_chunk_index,  
#                 "Chunk": temp_chunk,
#                 "GroupIndex": temp_group_index,
#                 "RefText": temp_ref_text,
#                 "Title": temp_title,
#             })
#             new_chunk_index += 1  
#             temp_chunk = chunk_content
#             temp_group_index = group_index
#             temp_ref_text = ref_text
#             temp_title = title

#     if temp_chunk:
#         merged_data.append({
#             "ChunkIndex": new_chunk_index,  
#             "Chunk": temp_chunk,
#             "GroupIndex": temp_group_index,
#             "RefText": temp_ref_text,
#             "Title": temp_title,
#         })

#     return merged_data

# app = FastAPI()

# @app.post("/upload_pdf/")
# async def upload_pdf(file: UploadFile = File(...)):
#     start_time = time.time()
#     pdf_content = await file.read()
    
#     temp_file_path = "/tmp/temp.pdf"  
#     with open(temp_file_path, 'wb') as f:
#         f.write(pdf_content)
    
#     conv_res = DocumentConverter().convert(temp_file_path)
#     doc = conv_res.document
    
#     chunks = list(HierarchicalChunker().chunk(doc))

#     # chunker = HybridChunker(tokenizer="BAAI/bge-small-en-v1.5")  
#     # chunk_hybrid = list(chunker.chunk(doc))
    
#     title_to_reftexts = {}
#     for chunk in chunks:
#         title = " > ".join(chunk.meta.headings)
#         ref_text = chunk.text
#         if title not in title_to_reftexts:
#             title_to_reftexts[title] = []
#         title_to_reftexts[title].append(ref_text)

#     title_to_combined_reftext = {}
#     for title, reftexts in title_to_reftexts.items():
#         combined_ref_text = " ".join(reftexts)  
#         title_to_combined_reftext[title] = combined_ref_text

#     unique_titles = list(title_to_combined_reftext.keys())
#     title_to_groupindex = {title: idx + 1 for idx, title in enumerate(unique_titles)}

#     chunk_data = []

#     current_doc_item_index = 1  

#     temp_chunk = ""
#     max_length = 512
#     for _, chunk in enumerate(chunks):
#         title = " > ".join(chunk.meta.headings)
#         combined_ref_text = title_to_combined_reftext.get(title, "")
#         group_index = title_to_groupindex.get(title, 0)
#         doc_items = chunk.meta.doc_items
        
#         for item in doc_items:
#             chunk_content = item.text.strip()
            
#             if chunk_content == "" or len(chunk_content) < 10:
#                 continue
            
#             if len(temp_chunk) + len(chunk_content) < max_length:
#                 if temp_chunk:
#                     temp_chunk += " "  
#                 temp_chunk += chunk_content
#             else:
#                 if temp_chunk:
#                     chunk_info = {
#                         "ChunkIndex": current_doc_item_index,
#                         "Chunk": temp_chunk.replace("\n", " "),
#                         "GroupIndex": group_index,
#                         "RefText": combined_ref_text.replace("\n", " "),
#                         "Title": title,
#                     }
#                     chunk_data.append(chunk_info)
#                     current_doc_item_index += 1
#                 temp_chunk = chunk_content  

#         if temp_chunk:
#             chunk_info = {
#                 "ChunkIndex": current_doc_item_index,
#                 "Chunk": temp_chunk.replace("\n", " "),
#                 "GroupIndex": group_index,
#                 "RefText": combined_ref_text.replace("\n", " "),
#                 "Title": title,
#             }
#             chunk_data.append(chunk_info)
#             current_doc_item_index += 1
#             temp_chunk = ""  

#     merged_chunk_data = merge_chunks_by_title(chunk_data, max_length=512)

#     end_time = time.time()
#     latency = end_time - start_time
    
#     return {"List_Chunks": merged_chunk_data, "Latency(s)": latency}

# if __name__ == "__main__":
#     import uvicorn
    
#     uvicorn.run(
#         "api:app",  
#         host=config("HOST", default="0.0.0.0"),  # Global
#         port=config("PORT", default=8074, cast=int),  # Port
#         reload=config('DEBUG', default=False, cast=bool)  # Reload 
#     )

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Using for chunking Table
import re 
from fastapi import FastAPI, UploadFile, File
from docling.document_converter import DocumentConverter
from docling_core.transforms.chunker import HierarchicalChunker
from docling.chunking import HybridChunker

from decouple import config
import io
import os
import time 
import PyPDF2  # Thêm thư viện PyPDF2

app = FastAPI()

from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,  # Max_length
    chunk_overlap=10,  # Character
    separators=["\n"]  # Order of priority breakdown
)

def crop_pdf(input_pdf_path, output_pdf_path, crop_percentage=0.05):
    reader = PyPDF2.PdfReader(input_pdf_path)
    writer = PyPDF2.PdfWriter()

    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        media_box = page.mediabox

        width = float(media_box.width)
        height = float(media_box.height)

        # Tính toán khoảng cách cắt bỏ từ trên và dưới
        crop_margin = height * crop_percentage

        # Định nghĩa lại mediabox sau khi cắt
        new_media_box = PyPDF2.generic.RectangleObject([
            media_box.lower_left[0],
            media_box.lower_left[1] + crop_margin,
            media_box.upper_right[0],
            media_box.upper_right[1] - crop_margin
        ])

        page.mediabox = new_media_box
        writer.add_page(page)

    with open(output_pdf_path, 'wb') as out_file:
        writer.write(out_file)

@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    start_time = time.time()
    pdf_content = await file.read()
    
    # Lưu file PDF gốc tạm thời
    temp_input_path = "/tmp/temp_input.pdf"  
    with open(temp_input_path, 'wb') as f:
        f.write(pdf_content)
    
    # Đường dẫn để lưu PDF đã cắt
    temp_cropped_path = "/tmp/temp_cropped.pdf"
    
    # Cắt bỏ header và footer
    crop_pdf(temp_input_path, temp_cropped_path, crop_percentage=0.05)
    
    # Chuyển tiếp file PDF đã cắt cho Docling
    conv_res = DocumentConverter().convert(temp_cropped_path)
    doc = conv_res.document
    
    chunks = list(HierarchicalChunker().chunk(doc))

    chunk_data = []
    current_doc_item_index = 1  
    group_index_map = {}  # Lưu trữ GroupIndex cho mỗi Title
    current_group_index = 1  # Khởi tạo GroupIndex từ 1
    combine_ref_text_map = {}  # Lưu trữ các ref_text đã gộp theo Title

    # Gộp ref_text theo Title
    for chunk in chunks:
        if chunk.meta.headings is None:
            continue  # Bỏ qua nếu không có heading
        else:
            title = tuple(chunk.meta.headings)
        ref_text = chunk.text.replace(". ", ".\n")
        
        # Thêm ref_text vào combine_ref_text_map theo Title
        if title not in combine_ref_text_map:
            combine_ref_text_map[title] = []
        combine_ref_text_map[title].append(ref_text)

    # Xử lý từng Title và phân tách thành minichunks
    for title, ref_texts in combine_ref_text_map.items():
        # Kết hợp tất cả ref_text thành một chuỗi duy nhất
        combine_ref_text = "\n".join(ref_texts)
        
        # Gán GroupIndex cho Title nếu chưa có
        if title not in group_index_map:
            group_index_map[title] = current_group_index
            current_group_index += 1
        
        group_index = group_index_map[title]  # Lấy GroupIndex cho Title hiện tại
        
        # Phân tách combine_ref_text thành các minichunks
        minichunks = text_splitter.split_text(combine_ref_text)
        
        for minichunk in minichunks:
            # if len(minichunk) < 15:  # Bỏ qua các minichunk quá ngắn
            #     continue
            chunk_info = {
                "ChunkIndex": current_doc_item_index,
                "Chunk": minichunk,
                "GroupIndex": group_index,  # Đảm bảo cùng GroupIndex
                "RefText": combine_ref_text,  # Dùng combine_ref_text
                "Title": title             
            }
            chunk_data.append(chunk_info)
            current_doc_item_index += 1

    end_time = time.time()
    latency = end_time - start_time
    
    os.remove(temp_input_path)
    os.remove(temp_cropped_path)
    
    return {"List_Chunks": chunk_data, "Latency(s)": latency}

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "api:app",  
        host=config("HOST", default="0.0.0.0"),  # Global
        port=config("PORT", default=8095, cast=int),  # Port
        reload=config('DEBUG', default=False, cast=bool)  # Reload 
    )
