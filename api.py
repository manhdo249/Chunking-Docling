# # from fastapi import FastAPI, UploadFile, File
# # from docling.document_converter import DocumentConverter
# # from docling_core.transforms.chunker import HierarchicalChunker
# # from docling.chunking import HybridChunker

# # from decouple import config
# # import io
# # import os
# # import time 

# # def merge_chunks_by_title(chunk_data, max_length=512):
# #     """
# #     Gộp các chunk có độ dài nhỏ hơn `max_length` trong cùng một `Title` 
# #     và đảm bảo ChunkIndex được đánh số lại.

# #     Args:
# #         chunk_data (list): Danh sách các chunk dưới dạng dictionary.
# #         max_length (int): Độ dài tối đa cho mỗi chunk. Mặc định là 512.

# #     Returns:
# #         list: Danh sách các chunk đã được gộp và đánh số lại `ChunkIndex`.
# #     """
# #     merged_data = []
# #     temp_chunk = ""
# #     temp_group_index = None
# #     temp_ref_text = ""
# #     temp_title = ""
# #     new_chunk_index = 1   

# #     for chunk in chunk_data:
# #         chunk_content = chunk["Chunk"]
# #         group_index = chunk["GroupIndex"]
# #         ref_text = chunk["RefText"]
# #         title = chunk["Title"]

# #         if not temp_chunk or temp_title != title:
# #             if temp_chunk:
# #                 merged_data.append({
# #                     "ChunkIndex": new_chunk_index,  
# #                     "Chunk": temp_chunk,
# #                     "GroupIndex": temp_group_index,
# #                     "RefText": temp_ref_text,
# #                     "Title": temp_title,
# #                 })
# #                 new_chunk_index += 1  

# #             temp_chunk = chunk_content
# #             temp_group_index = group_index
# #             temp_ref_text = ref_text
# #             temp_title = title
# #         elif len(temp_chunk) + len(chunk_content) < max_length:
# #             temp_chunk += " " + chunk_content
# #         else:
# #             merged_data.append({
# #                 "ChunkIndex": new_chunk_index,  
# #                 "Chunk": temp_chunk,
# #                 "GroupIndex": temp_group_index,
# #                 "RefText": temp_ref_text,
# #                 "Title": temp_title,
# #             })
# #             new_chunk_index += 1  
# #             temp_chunk = chunk_content
# #             temp_group_index = group_index
# #             temp_ref_text = ref_text
# #             temp_title = title

# #     if temp_chunk:
# #         merged_data.append({
# #             "ChunkIndex": new_chunk_index,  
# #             "Chunk": temp_chunk,
# #             "GroupIndex": temp_group_index,
# #             "RefText": temp_ref_text,
# #             "Title": temp_title,
# #         })

# #     return merged_data

# # app = FastAPI()

# # @app.post("/upload_pdf/")
# # async def upload_pdf(file: UploadFile = File(...)):
# #     start_time = time.time()
# #     pdf_content = await file.read()
    
# #     temp_file_path = "/tmp/temp.pdf"  
# #     with open(temp_file_path, 'wb') as f:
# #         f.write(pdf_content)
    
# #     conv_res = DocumentConverter().convert(temp_file_path)
# #     doc = conv_res.document
    
# #     chunks = list(HierarchicalChunker().chunk(doc))

# #     # chunker = HybridChunker(tokenizer="BAAI/bge-small-en-v1.5")  
# #     # chunk_hybrid = list(chunker.chunk(doc))
    
# #     title_to_reftexts = {}
# #     for chunk in chunks:
# #         title = " > ".join(chunk.meta.headings)
# #         ref_text = chunk.text
# #         if title not in title_to_reftexts:
# #             title_to_reftexts[title] = []
# #         title_to_reftexts[title].append(ref_text)

# #     title_to_combined_reftext = {}
# #     for title, reftexts in title_to_reftexts.items():
# #         combined_ref_text = " ".join(reftexts)  
# #         title_to_combined_reftext[title] = combined_ref_text

# #     unique_titles = list(title_to_combined_reftext.keys())
# #     title_to_groupindex = {title: idx + 1 for idx, title in enumerate(unique_titles)}

# #     chunk_data = []

# #     current_doc_item_index = 1  

# #     temp_chunk = ""
# #     max_length = 512
# #     for _, chunk in enumerate(chunks):
# #         title = " > ".join(chunk.meta.headings)
# #         combined_ref_text = title_to_combined_reftext.get(title, "")
# #         group_index = title_to_groupindex.get(title, 0)
# #         doc_items = chunk.meta.doc_items
        
# #         for item in doc_items:
# #             chunk_content = item.text.strip()
            
# #             if chunk_content == "" or len(chunk_content) < 10:
# #                 continue
            
# #             if len(temp_chunk) + len(chunk_content) < max_length:
# #                 if temp_chunk:
# #                     temp_chunk += " "  
# #                 temp_chunk += chunk_content
# #             else:
# #                 if temp_chunk:
# #                     chunk_info = {
# #                         "ChunkIndex": current_doc_item_index,
# #                         "Chunk": temp_chunk.replace("\n", " "),
# #                         "GroupIndex": group_index,
# #                         "RefText": combined_ref_text.replace("\n", " "),
# #                         "Title": title,
# #                     }
# #                     chunk_data.append(chunk_info)
# #                     current_doc_item_index += 1
# #                 temp_chunk = chunk_content  

# #         if temp_chunk:
# #             chunk_info = {
# #                 "ChunkIndex": current_doc_item_index,
# #                 "Chunk": temp_chunk.replace("\n", " "),
# #                 "GroupIndex": group_index,
# #                 "RefText": combined_ref_text.replace("\n", " "),
# #                 "Title": title,
# #             }
# #             chunk_data.append(chunk_info)
# #             current_doc_item_index += 1
# #             temp_chunk = ""  

# #     merged_chunk_data = merge_chunks_by_title(chunk_data, max_length=512)

# #     end_time = time.time()
# #     latency = end_time - start_time
    
# #     return {"List_Chunks": merged_chunk_data, "Latency(s)": latency}

# # if __name__ == "__main__":
# #     import uvicorn
    
# #     uvicorn.run(
# #         "api:app",  
# #         host=config("HOST", default="0.0.0.0"),  # Global
# #         port=config("PORT", default=8074, cast=int),  # Port
# #         reload=config('DEBUG', default=False, cast=bool)  # Reload 
# #     )

# # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# # Using for chunking Table
# import re 
# from fastapi import FastAPI, UploadFile, File
# from docling.document_converter import DocumentConverter
# from docling_core.transforms.chunker import HierarchicalChunker
# from docling.chunking import HybridChunker

# from decouple import config
# import io
# import os
# import time 

# app = FastAPI()

# from langchain.text_splitter import RecursiveCharacterTextSplitter

# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size=512,  # Max_length
#     chunk_overlap=10,  # Character
#     separators=["\n"]  # Order of priority breakdown
# )

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

#     chunk_data = []
#     current_doc_item_index = 1  
#     group_index_map = {}  # Lưu trữ GroupIndex cho mỗi Title
#     current_group_index = 1  # Khởi tạo GroupIndex từ 1
#     combine_ref_text_map = {}  # Lưu trữ các ref_text đã gộp theo Title

#     # Gộp ref_text theo Title
#     for chunk in chunks:
#         if chunk.meta.headings is None:
#             continue  # Đặt giá trị mặc định nếu không có heading
#         else:
#             title = tuple(chunk.meta.headings)
#         ref_text = chunk.text.replace(". ", ".\n")
        
#         # Thêm ref_text vào combine_ref_text_map theo Title
#         if title not in combine_ref_text_map:
#             combine_ref_text_map[title] = []
#         combine_ref_text_map[title].append(ref_text)

#     # Xử lý từng Title và phân tách thành minichunks
#     for title, ref_texts in combine_ref_text_map.items():
#         # Kết hợp tất cả ref_text thành một chuỗi duy nhất
#         combine_ref_text = "\n".join(ref_texts)
        
#         # Gán GroupIndex cho Title nếu chưa có
#         if title not in group_index_map:
#             group_index_map[title] = current_group_index
#             current_group_index += 1
        
#         group_index = group_index_map[title]  # Lấy GroupIndex cho Title hiện tại
        
#         # Phân tách combine_ref_text thành các minichunks
#         minichunks = text_splitter.split_text(combine_ref_text)
        
#         for minichunk in minichunks:
#             # if len(minichunk) < 15:  # Bỏ qua các minichunk quá ngắn
#             #     continue
#             chunk_info = {
#                 "ChunkIndex": current_doc_item_index,
#                 "Chunk": minichunk,
#                 "GroupIndex": group_index,  # Đảm bảo cùng GroupIndex
#                 "RefText": combine_ref_text,  # Dùng combine_ref_text
#                 "Title": title             
#             }
#             chunk_data.append(chunk_info)
#             current_doc_item_index += 1


#     end_time = time.time()
#     latency = end_time - start_time
    
#     return {"List_Chunks": chunk_data, "Latency(s)": latency}

# if __name__ == "__main__":
#     import uvicorn
    
#     uvicorn.run(
#         "api:app",  
#         host=config("HOST", default="0.0.0.0"),  # Global
#         port=config("PORT", default=8095, cast=int),  # Port
#         reload=config('DEBUG', default=False, cast=bool)  # Reload 
#     )

import re 
from fastapi import FastAPI, UploadFile, File
from docling.document_converter import DocumentConverter
from docling_core.transforms.chunker import HierarchicalChunker
from docling.chunking import HybridChunker

from decouple import config
import io
import os
import time 
import fitz  # PyMuPDF

app = FastAPI()

from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,  # Max_length
    chunk_overlap=10,  # Character
    separators=["\n"]  # Order of priority breakdown
)

# def crop_pdf_pymupdf(input_path, output_path, top_crop_percent=10, bottom_crop_percent=5):
#     """
#     Cắt 10% từ phía trên và 5% từ phía dưới của mỗi trang trong file PDF.

#     :param input_path: Đường dẫn tới file PDF nguồn.
#     :param output_path: Đường dẫn tới file PDF đích sau khi cắt.
#     :param top_crop_percent: Tỷ lệ phần trăm cần cắt từ phía trên (mặc định là 10%).
#     :param bottom_crop_percent: Tỷ lệ phần trăm cần cắt từ phía dưới (mặc định là 5%).
#     """
#     # Mở file PDF nguồn
#     doc = fitz.open(input_path)
    
#     for page_number, page in enumerate(doc, start=1):
#         rect = page.rect
#         width = rect.width
#         height = rect.height
        
#         # Tính toán số điểm cần cắt từ trên và dưới
#         top_crop_amount = height * top_crop_percent / 100
#         bottom_crop_amount = height * bottom_crop_percent / 100
        
#         # Thiết lập vùng cắt mới
#         new_rect = fitz.Rect(
#             rect.x0, 
#             rect.y0 + top_crop_amount, 
#             rect.x1, 
#             rect.y1 - bottom_crop_amount
#         )
#         page.set_cropbox(new_rect)
        
#         print(f"Trang {page_number}: Cắt {top_crop_percent}% từ trên và {bottom_crop_percent}% từ dưới.")
    
#     # Lưu file PDF đã cắt
#     doc.save(output_path)
#     doc.close()
#     print(f"Đã cắt {input_path} và lưu kết quả vào {output_path}")

@app.post("/upload_pdf/")
async def upload_pdf(
    file: UploadFile = File(...),
    # top_crop_percent: float = 10.0  # Giá trị mặc định là 10% nếu người dùng không cung cấp
):
    """
    API endpoint để tải lên file PDF, cắt theo tỷ lệ được cung cấp và trả về các chunks đã xử lý.
    
    :param file: File PDF được tải lên.
    :param top_crop_percent: Tỷ lệ phần trăm cần cắt từ phía trên. (Nhập số thực)
    """
    start_time = time.time()
    pdf_content = await file.read()
    
    # Đường dẫn tạm thời cho file gốc
    temp_file_path = "/tmp/temp.pdf"
    with open(temp_file_path, 'wb') as f:
        f.write(pdf_content)
    
    # # Đường dẫn tạm thời cho file đã cắt
    # cropped_file_path = "/tmp/temp_cropped.pdf"
    
    # # Thực hiện cắt PDF
    # crop_pdf_pymupdf(
    #     input_path=temp_file_path,
    #     output_path=cropped_file_path,
    #     top_crop_percent=top_crop_percent,
    #     bottom_crop_percent=0  # Mặc định không cắt phía dưới
    # )
    
    # Sử dụng file PDF đã cắt để chuyển đổi
    conv_res = DocumentConverter().convert(temp_file_path)
    doc = conv_res.document
    
    # # Xóa các file tạm sau khi sử dụng
    # try:
    #     os.remove(temp_file_path)
    #     os.remove(cropped_file_path)
    # except Exception as e:
    #     print(f"Lỗi khi xóa file tạm: {e}")

    # Xử lý lỗi Role trong Docling
    page_header_texts = set()
    for item in doc.texts:
        if item.label == "page_header":
            page_header_texts.add(item.text)
        elif item.text in page_header_texts:
            item.label = "page_header"
    
    # Xóa header-footer
    new_doc = []
    for minidoc in doc.texts:
        if minidoc.label != "page_header" and minidoc.label != "page_footer":
            new_doc.append(minidoc)
    doc.texts = new_doc

    
    chunks = []
    try:
        for chunk in HierarchicalChunker().chunk(doc):
            chunks.append(chunk)
    except IndexError as e:
        pass

    chunk_data = []
    current_doc_item_index = 1  
    group_index_map = {}  # Lưu trữ GroupIndex cho mỗi Title
    current_group_index = 1  # Khởi tạo GroupIndex từ 1
    combine_ref_text_map = {}  # Lưu trữ các ref_text đã gộp theo Title
    unique_labels = set() 

    for chunk in chunks:
        skip_chunk = False
        for doc_item in chunk.meta.doc_items:
            unique_labels.add(doc_item.label)
            if doc_item.label == "page_footer":
                skip_chunk = True
                break 
        
        if skip_chunk:
            continue  # Bỏ qua chunk này
        

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
            # Nếu cần bỏ qua các minichunk quá ngắn, kích hoạt đoạn mã dưới
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
    
    return {"List_Chunks": chunk_data, "Latency(s)": latency}

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "api:app",  
        host=config("HOST", default="0.0.0.0"),  # Global
        port=config("PORT", default=2409, cast=int),  # Port
        reload=config('DEBUG', default=False, cast=bool)  # Reload 
    )









