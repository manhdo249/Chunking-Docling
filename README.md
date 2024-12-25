# **Chungking Docling**

Welcome to **Chungking Docling**, a tool designed for document processing and linguistic analysis. This guide will help you set up, use, and customize the application to suit your needs.


## **Installation**

### Prerequisites
- **Operating System**: Windows, macOS, or Linux  
- **Python**: Version 3.10   
- **Dependencies**: Install via `pip`

### Steps
1. Clone the repository:  
   ```bash
   git clone https://github.com/manhdo249/chungking-docling.git
   cd chungking-docling
   ```

2. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```

3. Optional: Set up a virtual environment for isolated dependency management.  

## **Quick Start Guide**

1. **Run the API**  
   Launch the api using:  
   ```bash
   uvicorn api:app --host your_host --port your_port
   ```

2. **Upload and Chunking Documents**  
   Navigate to the FastAPI - Swagger UI to upload and chunking documents.  

## **Configuration**

Key configuration options include:

- **Input**: Choose PDF, DOCX, JPG, ... formats.
- **Output**: JSON format.  

## **Usage Examples**

### Run api.py
```bash
uvicorn api:app --host 0.0.0.0 --port 8073
```

### Upload file and chunking

- Open http://0.0.0.0:8073/docs on browser 
- Watch this video
<div align="center">
  
[![Video Title](https://img.youtube.com/vi/h3irWpoGu_4/0.jpg)](https://www.youtube.com/watch?v=h3irWpoGu_4)

</div>

## **Contributing**

Contributions are welcome! Follow these steps:  
1. Fork the repository.  
2. Create a feature branch: `git checkout -b feature-name`  
3. Commit changes: `git commit -m "Add new feature"`  
4. Push to the branch: `git push origin feature-name`  
5. Open a pull request.  

## **License**

This project is licensed under the MIT License. See the `LICENSE` file for details.
