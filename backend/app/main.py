from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api import upload, transpile, files, translate
import os

app = FastAPI(
    title="Sigma to RML Transpiler API",
    description="API for converting Sigma security rules to Runtime Monitoring Language (RML)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # or ["*"] for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(transpile.router, prefix="/transpile", tags=["Transpile"])
app.include_router(files.file_router, prefix="/files", tags=["File Management"])
app.include_router(translate.router, prefix="/translate", tags=["Translate"])

@app.get("/")
def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Sigma2RML backend",
        "version": "1.0.0",
        "description": "Sigma to RML Transpiler API",
        "endpoints": {
            "upload": "/upload",
            "transpile": "/transpile", 
            "files": "/files",
            "translate": "/translate",
            "docs": "/docs"
        }
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    try:
        # Check if required directories exist
        required_dirs = ["uploaded_files", "translated_files"]
        dir_status = {}
        
        for dir_name in required_dirs:
            if os.path.exists(dir_name):
                dir_status[dir_name] = "exists"
            else:
                dir_status[dir_name] = "missing"
        
        # Check if database file exists
        db_status = "exists" if os.path.exists("file_registry.json") else "missing"
        
        return {
            "status": "healthy",
            "directories": dir_status,
            "database": db_status,
            "timestamp": "2024-01-01T00:00:00Z"  # You can add actual timestamp here
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "unhealthy", "error": str(e)}
        )

@app.get("/stats")
def get_stats():
    """Get API usage statistics"""
    try:
        from app.storage.db import load_db
        
        files = load_db()
        total_files = len(files)
        translated_files = len([f for f in files if f.get("translated", False)])
        
        # Count files by type
        file_types = {}
        for file_info in files:
            ext = os.path.splitext(file_info["filename"])[1].lower()
            file_types[ext] = file_types.get(ext, 0) + 1
        
        return {
            "total_files": total_files,
            "translated_files": translated_files,
            "pending_files": total_files - translated_files,
            "file_types": file_types,
            "translation_rate": round((translated_files / total_files * 100) if total_files > 0 else 0, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc),
            "type": type(exc).__name__
        }
    )
