import sys
import asyncio
import os
import time
import uuid
from typing import Any, List
from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends, Form, Query, APIRouter, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn
from nicegui import ui, app
from nicegui.events import ValueChangeEventArguments
import json


from logging_config import setup_logging, log_info, log_error, log_success, log_warning
logger = setup_logging()
from app.niceGUI_folder.pydentic_models import CatCreate, CatUpdate, OwnerCreate, OwnerUpdate
from app.niceGUI_folder.add_cat_page import add_cat_page_render
from app.niceGUI_folder.add_owner_page import add_owner_page_render
from app.niceGUI_folder.add_breed_page import add_breed_page_render
from app.database_folder.orm import AsyncOrm
from app.database_folder.postgres import (check_db_connection,
                                          postgres_check_and_create_database,
                                          drop_database_if_exists)
from app.database_folder.insert_info import start_add_workflow, add_owner
from app.database_folder.model import Base
from system_functions_folder.check_cread import check_creds
from app.niceGUI_folder.main_page import main_page_render
from app.niceGUI_folder.cats_page import cats_page_render
from app.niceGUI_folder.owners_page import owners_page_render
from app.niceGUI_folder.breeds_page import breeds_page_render
from app.niceGUI_folder.cat_profile_page import cat_profile_page_render
from app.niceGUI_folder.edit_cat_page import edit_cat_page_render
from app.niceGUI_folder.edit_owner_page import edit_owner_page_render
from app.niceGUI_folder.edit_breed_page import edit_breed_page_render
from app.niceGUI_folder.history_page import history_page_render
from app.niceGUI_folder.login_page import login_page_render
from app.niceGUI_folder.auth_check_page import auth_check_page_render
from app.niceGUI_folder.studbook_page import studbook_page_render
from app.niceGUI_folder.auth_service import AuthService
from app.niceGUI_folder.session_manager import SessionManager




def require_auth(request: Request):
    """Check if user is authenticated and return user data"""
    session_id = request.cookies.get("session_id")
    if not session_id or not SessionManager.is_authenticated(session_id):
        return None
    return SessionManager.get_current_user(session_id)


@app.exception_handler(Exception)
async def swallow_disconnects(request: Request, exc: Exception):
    name = type(exc).__name__
    if name in ('ClientDisconnect', 'CancelledError', 'WebSocketDisconnect', 'RuntimeError'):
        return Response(status_code=499)
    raise exc


@ui.page('/')
async def root_page(request: Request):
    auth_check_page_render(request)

@ui.page('/dashboard')
async def main_page(request: Request):
    user = require_auth(request)
    if not user:
        return RedirectResponse(url='/login', status_code=303)
    await main_page_render(request)

@ui.page('/login')
async def login_page(request: Request):
    login_page_render(request)


@ui.page('/cats')
async def cats_page(request: Request):
    user = require_auth(request)
    if not user:
        return RedirectResponse(url='/login', status_code=303)
    await cats_page_render(request)


@ui.page('/owners')
async def owners_page(request: Request):
    user = require_auth(request)
    if not user:
        return RedirectResponse(url='/login', status_code=303)
    await owners_page_render(request)


@ui.page('/breeds')
async def breeds_page(request: Request):
    user = require_auth(request)
    if not user:
        return RedirectResponse(url='/login', status_code=303)
    await breeds_page_render(request)


@ui.page('/add_cat')
async def add_cat_page(request: Request):
    user = require_auth(request)
    if not user:
        return RedirectResponse(url='/login', status_code=303)
    await add_cat_page_render(request)


@ui.page('/add_owner')
async def add_owner_page(request: Request):
    user = require_auth(request)
    if not user:
        return RedirectResponse(url='/login', status_code=303)
    await add_owner_page_render(request)


@ui.page('/add_breed')
async def add_breed_page(request: Request):
    user = require_auth(request)
    if not user:
        return RedirectResponse(url='/login', status_code=303)
    await add_breed_page_render(request)


@ui.page('/cat_profile/{cat_id}')
async def cat_profile_page(request: Request, cat_id: int):
    user = require_auth(request)
    if not user:
        return RedirectResponse(url='/login', status_code=303)
    await cat_profile_page_render(request, cat_id)


@ui.page('/edit_cat/{cat_id}')
async def edit_cat_page(request: Request, cat_id: int):
    user = require_auth(request)
    if not user:
        return RedirectResponse(url='/login', status_code=303)
    await edit_cat_page_render(cat_id, request)


@ui.page('/edit_owner/{owner_id}')
async def edit_owner_page(request: Request, owner_id: int):
    user = require_auth(request)
    if not user:
        return RedirectResponse(url='/login', status_code=303)
    await edit_owner_page_render(request, owner_id)


@ui.page('/edit_breed/{breed_id}')
async def edit_breed_page(request: Request, breed_id: int):
    user = require_auth(request)
    if not user:
        return RedirectResponse(url='/login', status_code=303)
    await edit_breed_page_render(request, breed_id)


@ui.page('/history')
async def history_page(request: Request):
    user = require_auth(request)
    if not user:
        return RedirectResponse(url='/login', status_code=303)
    await history_page_render(request)

@ui.page('/studbook')
async def studbook_page(request: Request):
    user = require_auth(request)
    if not user:
        return RedirectResponse(url='/login', status_code=303)
    await studbook_page_render(request)


# Authentication routes
@app.post('/login')
async def login_post(email: str = Form(...), password: str = Form(...)):
    """Handle login form submission"""
    try:
        # Authenticate user
        user_data = await AuthService.authenticate_user(email, password)
        
        if user_data:
            # Generate unique session_id
            session_id = str(uuid.uuid4())
            
            # Store session in SessionManager
            SessionManager.set_current_user(user_data, session_id)
            
            # Create response with redirect to dashboard
            response = RedirectResponse(url='/dashboard', status_code=303)
            
            # Set cookie with session_id
            response.set_cookie(
                key="session_id",
                value=session_id,
                httponly=True,
                secure=False,
                samesite="lax",
                max_age=86400  # 24 часа
            )
            
            return response
        else:
            # Authentication failed, redirect back to login
            return RedirectResponse(url='/login?error=invalid_credentials', status_code=303)
            
    except Exception as e:
        print(f"Login error: {e}")
        return RedirectResponse(url='/login?error=server_error', status_code=303)


@app.post('/logout')
async def logout_post(request: Request):
    """Handle logout"""
    try:
        session_id = request.cookies.get("session_id")
        if session_id:
            # Clear session from SessionManager
            SessionManager.clear_session(session_id)
        
        # Create response with redirect to login
        response = RedirectResponse(url='/login', status_code=303)
        
        # Delete cookie
        response.delete_cookie("session_id")
        
        return response
    except Exception as e:
        print(f"Logout error: {e}")
        return RedirectResponse(url='/login', status_code=303)


@app.get('/static/{file_path:path}')
async def serve_static_files(file_path: str):
    normalized_file_path = file_path.replace('/', '\\') if os.name == 'nt' else file_path
    full_path = os.path.join(os.getcwd(), normalized_file_path)
    print(f"Serving file: {file_path} -> {full_path}")
    print(f"Normalized path: {normalized_file_path}")
    print(f"File exists: {os.path.exists(full_path)}")
    print(f"Is file: {os.path.isfile(full_path) if os.path.exists(full_path) else 'N/A'}")
    
    if os.path.exists(full_path) and os.path.isfile(full_path):
        return FileResponse(full_path)
    else:
        print(f"File not found: {full_path}")
        raise HTTPException(status_code=404, detail="File not found")


@app.get('/exports/{filename}')
async def serve_exports(filename: str):
    """Serve exported files from exports directory"""
    exports_dir = os.path.join(os.getcwd(), 'exports')
    file_path = os.path.join(exports_dir, filename)
    
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path, filename=filename)
    else:
        raise HTTPException(status_code=404, detail="Export file not found")


def start_db():
    log_info("Initializing database...")
    
    if not check_creds():
        log_error("Credentials verification error")
        sys.exit()
    
    log_info("Creating database...")
    try:
        drop_database_if_exists()
        if postgres_check_and_create_database(Base):
            asyncio.run(add_owner())
            log_success("Admin user added")
    except Exception as e:
        log_warning(f"Database already exists or creation error: {e}")
        if not check_db_connection():
            log_error("Cannot connect to database")
            sys.exit()

    max_retries = 5
    for attempt in range(max_retries):
        if check_db_connection():
            log_success("Database connection verified")
            break
        else:
            log_warning(f"Database connection attempt {attempt + 1}/{max_retries} failed")
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                log_error("Database connection error - max retries exceeded")
                sys.exit()
    
    log_success("Database ready")
    log_info("Loading test data...")
    # start_add_workflow()
    log_success("Test data loaded")


if __name__ in {"__main__", "__mp_main__"}:
    log_info("Starting Cat Database Management System v2.0")
    log_info("=" * 50)
    
    try:
        start_db()
        
        log_success("Server started successfully!")
        log_info("🌐 Access: http://localhost:8080")
        log_info("🛑 Press Ctrl+C to stop")
        log_info("=" * 50)
        
        ui.run(
            port=8080,
            title='Cat Database Management System',
            show=True,
            reload=False,
        )
        
    except KeyboardInterrupt:
        log_info("Stopping server...")
    except Exception as e:
        log_error(f"Startup error: {e}")
        sys.exit(1)
