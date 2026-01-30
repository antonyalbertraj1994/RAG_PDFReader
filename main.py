# This is a sample Python script.
from starlette.staticfiles import StaticFiles

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import Embedding

from google import genai

from fastapi.responses import JSONResponse

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from fastapi.responses import FileResponse

# Load environment variables
#load_dotenv()
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)



# Configure Gemini
# response = client.models.generate_content(
#     model="gemini-3-flash-preview", contents="Explain how AI works in a few words"
# )
# Initialize FastAPI app
app = FastAPI()
app.mount("/pdfjs", StaticFiles(directory="pdfjs"), name="pdfjs")

HTML_FOLDER = "pdfjs/web"

# Route to serve a specific HTML file
@app.get("/page1")
async def page1():
    return FileResponse(os.path.join(HTML_FOLDER, "splittest.html"))


# Enable CORS (equivalent to app.use(cors()))
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request body schema
class SummaryRequest(BaseModel):
    text: str

# Response schema (optional but clean)
class SummaryResponse(BaseModel):
    summary: str

from fastapi import UploadFile, File

@app.post("/upload-pdf")
async def upload_pdf(pdf: UploadFile = File(...)):
    content = await pdf.read()
    with open(f"uploaded_{pdf.filename}", "wb") as f:
        f.write(content)
    return {"filename": pdf.filename, "size": len(content)}


@app.post("/summary", response_model=SummaryResponse)
async def summarize_text(request: SummaryRequest):
    if not request.text:
        raise HTTPException(status_code=400, detail="No text provided")
    print("InputPrompt",request.text)
    prompt = f'Summarize the following text in 2-3 concise sentences: "{request.text}"'

    try:
        #model = genai.GenerativeModel("gemini-2.0-flash")
        # response = client.models.generate_content(
        #     model="gemini-3-flash-preview", contents=prompt)
        #
        # print(response.text)

        #response = model.generate_content(prompt)

        outputanswer = Embedding.search(request.text)


        #summary = response.text or "No summary received"
        print(f"Summary: {outputanswer}")

        return {"summary": outputanswer}

    except Exception as e:
        print("Error calling Gemini:", e)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/pdf", response_model=SummaryResponse)
async def summarize_text1(request: SummaryRequest):
    if not request.text:
        raise HTTPException(status_code=400, detail="No text provided")
    print(request.text)
    prompt = f'Summarize the following text in 2-3 concise sentences: "{request.text}"'

    try:
        #model = genai.GenerativeModel("gemini-2.0-flash")
        text = request.text + "Yolo"
        return {"summary": text}

    except Exception as e:
        print("Error calling Gemini:", e)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    # Check file type (optional but recommended)
    if file.content_type != "application/pdf":
        return JSONResponse(
            status_code=400,
            content={"error": "Only PDF files are allowed."}
        )

    # Build a safe file path
    file_path = os.path.join(UPLOAD_FOLDER, "input.pdf")

    # Read file contents and save to disk
    with open(file_path, "wb") as f:
        contents = await file.read()  # async read
        f.write(contents)
    Embedding.setupVectorStore()
    return {"status": "success", "filename": file.filename, "path": file_path}