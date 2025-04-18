from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3, uvicorn
from datetime import datetime
from pydantic import BaseModel

app = FastAPI()

comm="""app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)"""

def init_db():
    conn = sqlite3.connect('downloads.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS downloads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

class DownloadRequest(BaseModel):
    date: str

@app.post("/record-download/")
async def record_download(request: DownloadRequest):
    try:
        datetime.fromisoformat(request.date)
        
        conn = sqlite3.connect('downloads.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO downloads (date) VALUES (?)', (request.date,))
        conn.commit()
        conn.close()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/download-count/")
async def get_download_count():
    try:
        conn = sqlite3.connect('downloads.db')
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM downloads')
        count = cursor.fetchone()[0]
        conn.close()
        return {"count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
