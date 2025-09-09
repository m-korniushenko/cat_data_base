#!/usr/bin/env python3
"""
Startup script for Cat Database Management System
"""

import uvicorn

if __name__ == "__main__":
    print("🚀 Starting Cat Database Management System...")
    print("📊 FastAPI will be available at: http://127.0.0.1:8000")
    print("🐱 NiceGUI will be available at: http://127.0.0.1:8080")
    print("📚 API Documentation at: http://127.0.0.1:8000/docs")
    
    # Start FastAPI server
    uvicorn.run(
        "server:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
