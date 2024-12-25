from fastapi import FastAPI, UploadFile, File
from docling.document_converter import DocumentConverter
from docling_core.transforms.chunker import HierarchicalChunker
from docling.chunking import HybridChunker

from decouple import config
import io
import os
import time 

def merge_chunks_by_title(chunk_data, max_length=512):
    """
    Gộp các chunk có độ dài nhỏ hơn `max_length` trong cùng một `Title` 
    và đảm bảo ChunkIndex được đánh số lại.

    Args:
        chunk_data (list): Danh sách các chunk dưới dạng dictionary.
        max_length (int): Độ dài tối đa cho mỗi chunk. Mặc định là 512.

    Returns:
        list: Danh sách các chunk đã được gộp và đánh số lại `ChunkIndex`.
    """
    merged_data = []
    temp_chunk = ""
    temp_group_index = None
    temp_ref_text = ""
    temp_title = ""
    new_chunk_index = 1   

    for chunk in chunk_data:
        chunk_content = chunk["Chunk"]
        group_index = chunk["GroupIndex"]
        ref_text = chunk["RefText"]
        title = chunk["Title"]

        if not temp_chunk or temp_title != title:
            if temp_chunk:
                merged_data.append({
                    "ChunkIndex": new_chunk_index,  
                    "Chunk": temp_chunk,
                    "GroupIndex": temp_group_index,
                    "RefText": temp_ref_text,
                    "Title": temp_title,
                })
                new_chunk_index += 1  

            temp_chunk = chunk_content
            temp_group_index = group_index
            temp_ref_text = ref_text
            temp_title = title
        elif len(temp_chunk) + len(chunk_content) < max_length:
            temp_chunk += " " + chunk_content
        else:
            merged_data.append({
                "ChunkIndex": new_chunk_index,  
                "Chunk": temp_chunk,
                "GroupIndex": temp_group_index,
                "RefText": temp_ref_text,
                "Title": temp_title,
            })
            new_chunk_index += 1  
            temp_chunk = chunk_content
            temp_group_index = group_index
            temp_ref_text = ref_text
            temp_title = title

    if temp_chunk:
        merged_data.append({
            "ChunkIndex": new_chunk_index,  
            "Chunk": temp_chunk,
            "GroupIndex": temp_group_index,
            "RefText": temp_ref_text,
            "Title": temp_title,
        })

    return merged_data

app = FastAPI()

@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    start_time = time.time()
    pdf_content = await file.read()
    
    temp_file_path = "/tmp/temp.pdf"  
    with open(temp_file_path, 'wb') as f:
        f.write(pdf_content)
    
    conv_res = DocumentConverter().convert(temp_file_path)
    doc = conv_res.document
    
    chunks = list(HierarchicalChunker().chunk(doc))

    # chunker = HybridChunker(tokenizer="BAAI/bge-small-en-v1.5")  
    # chunk_hybrid = list(chunker.chunk(doc))
    
    title_to_reftexts = {}
    for chunk in chunks:
        title = " > ".join(chunk.meta.headings)
        ref_text = chunk.text
        if title not in title_to_reftexts:
            title_to_reftexts[title] = []
        title_to_reftexts[title].append(ref_text)

    title_to_combined_reftext = {}
    for title, reftexts in title_to_reftexts.items():
        combined_ref_text = " ".join(reftexts)  
        title_to_combined_reftext[title] = combined_ref_text

    unique_titles = list(title_to_combined_reftext.keys())
    title_to_groupindex = {title: idx + 1 for idx, title in enumerate(unique_titles)}

    chunk_data = []

    current_doc_item_index = 1  

    temp_chunk = ""
    max_length = 512
    for _, chunk in enumerate(chunks):
        title = " > ".join(chunk.meta.headings)
        combined_ref_text = title_to_combined_reftext.get(title, "")
        group_index = title_to_groupindex.get(title, 0)
        doc_items = chunk.meta.doc_items
        
        for item in doc_items:
            chunk_content = item.text.strip()
            
            if chunk_content == "" or len(chunk_content) < 5:
                continue
            
            if len(temp_chunk) + len(chunk_content) < max_length:
                if temp_chunk:
                    temp_chunk += " "  
                temp_chunk += chunk_content
            else:
                if temp_chunk:
                    chunk_info = {
                        "ChunkIndex": current_doc_item_index,
                        "Chunk": temp_chunk.replace("\n", " "),
                        "GroupIndex": group_index,
                        "RefText": combined_ref_text.replace("\n", " "),
                        "Title": title,
                    }
                    chunk_data.append(chunk_info)
                    current_doc_item_index += 1
                temp_chunk = chunk_content  

        if temp_chunk:
            chunk_info = {
                "ChunkIndex": current_doc_item_index,
                "Chunk": temp_chunk.replace("\n", " "),
                "GroupIndex": group_index,
                "RefText": combined_ref_text.replace("\n", " "),
                "Title": title,
            }
            chunk_data.append(chunk_info)
            current_doc_item_index += 1
            temp_chunk = ""  

    merged_chunk_data = merge_chunks_by_title(chunk_data, max_length=512)

    end_time = time.time()
    latency = end_time - start_time
    
    return {"List_Chunks": merged_chunk_data, "Latency(s)": latency}

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "api:app",  
        host=config("HOST", default="0.0.0.0"),  # Global
        port=config("PORT", default=8074, cast=int),  # Port
        reload=config('DEBUG', default=False, cast=bool)  # Reload 
    )

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Using for chunking Table
# from fastapi import FastAPI, UploadFile, File
# from docling.document_converter import DocumentConverter
# from docling_core.transforms.chunker import HierarchicalChunker
# from docling.chunking import HybridChunker

# from decouple import config
# import io
# import os
# import time 

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

#     chunk_data = []

#     current_doc_item_index = 1  

#     for _, chunk in enumerate(chunks):
#         title = chunk.meta.headings
#         ref_text = chunk.text        

#         chunk_info = {
#             "ChunkIndex": current_doc_item_index,  
#             "Chunk": ref_text,
#             "Title": title             
#         }
#         chunk_data.append(chunk_info)
#         current_doc_item_index += 1

#     end_time = time.time()
#     latency = end_time - start_time
    
#     return {"List_Chunks": chunk_data, "Latency(s)": latency}

# if __name__ == "__main__":
#     import uvicorn
    
#     uvicorn.run(
#         "api:app",  
#         host=config("HOST", default="0.0.0.0"),  # Global
#         port=config("PORT", default=8075, cast=int),  # Port
#         reload=config('DEBUG', default=False, cast=bool)  # Reload 
#     )



