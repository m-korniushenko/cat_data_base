import sys
import asyncio
from typing import Any, List
from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends, Form, Query, APIRouter, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn
from nicegui import ui, app
from nicegui.events import ValueChangeEventArguments
import json
import os

# Настройка логирования
from logging_config import setup_logging, log_info, log_error, log_success, log_warning

# Инициализация логирования
logger = setup_logging()
from app.niceGUI_folder.pydentic_models import CatCreate, CatUpdate, OwnerCreate, OwnerUpdate
from app.niceGUI_folder.add_cat_page import add_cat_page_render
from app.niceGUI_folder.add_owner_page import add_owner_page_render
from app.niceGUI_folder.add_breed_page import add_breed_page_render
from app.database_folder.orm import AsyncOrm
from app.database_folder.postgres import (check_db_connection,
                                          postgres_check_and_create_database,
                                          drop_database_if_exists)
from app.database_folder.insert_info import start_add_workflow
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



@app.exception_handler(Exception)
async def swallow_disconnects(request: Request, exc: Exception):
    name = type(exc).__name__
    if name in ('ClientDisconnect', 'CancelledError', 'WebSocketDisconnect', 'RuntimeError'):
        return Response(status_code=499)
    raise exc


@ui.page('/')
async def root_page():
    auth_check_page_render()

@ui.page('/dashboard')
async def main_page():
    await main_page_render()

@ui.page('/login')
async def login_page():
    login_page_render()


@ui.page('/cats')
async def cats_page():
    await cats_page_render()


@ui.page('/owners')
async def owners_page():
    await owners_page_render()


@ui.page('/breeds')
async def breeds_page():
    await breeds_page_render()


@ui.page('/add_cat')
async def add_cat_page():
    await add_cat_page_render()


@ui.page('/add_owner')
async def add_owner_page():
    await add_owner_page_render()


@ui.page('/add_breed')
async def add_breed_page():
    await add_breed_page_render()


@ui.page('/cat_profile/{cat_id}')
async def cat_profile_page(cat_id: int):
    await cat_profile_page_render(cat_id)


@ui.page('/edit_cat/{cat_id}')
async def edit_cat_page(cat_id: int):
    await edit_cat_page_render(cat_id)


@ui.page('/edit_owner/{owner_id}')
async def edit_owner_page(owner_id: int):
    await edit_owner_page_render(owner_id)


@ui.page('/edit_breed/{breed_id}')
async def edit_breed_page(breed_id: int):
    await edit_breed_page_render(breed_id)


@ui.page('/history')
async def history_page():
    await history_page_render()

@ui.page('/studbook')
async def studbook_page():
    await studbook_page_render()


# Static file serving for photos and files
@app.get('/static/{file_path:path}')
async def serve_static_files(file_path: str):
    """Serve static files (photos and documents)"""
    # Normalize path separators for file system
    normalized_file_path = file_path.replace('/', '\\') if os.name == 'nt' else file_path
    full_path = os.path.join(os.getcwd(), normalized_file_path)
    print(f"Serving file: {file_path} -> {full_path}")
    print(f"Normalized path: {normalized_file_path}")
    print(f"File exists: {os.path.exists(full_path)}")
    print(f"Is file: {os.path.isfile(full_path) if os.path.exists(full_path) else 'N/A'}")
    
    if os.path.exists(full_path) and os.path.isfile(full_path):
        from fastapi.responses import FileResponse
        return FileResponse(full_path)
    else:
        from fastapi import HTTPException
        print(f"File not found: {full_path}")
        raise HTTPException(status_code=404, detail="File not found")


def start_db():
    log_info("Инициализация базы данных...")
    
    if not check_creds():
        log_error("Ошибка проверки учетных данных")
        sys.exit()
    
    log_info("Создание базы данных...")
    drop_database_if_exists()
    postgres_check_and_create_database(Base)
    
    if not check_db_connection():
        log_error("Ошибка подключения к базе данных")
        sys.exit()
    
    log_success("База данных готова")
    log_info("Загрузка тестовых данных...")
    start_add_workflow()
    log_success("Тестовые данные загружены")


if __name__ in {"__main__", "__mp_main__"}:
    log_info("Запуск Cat Database Management System v2.0")
    log_info("=" * 50)
    
    try:
        start_db()
        
        log_success("Сервер запущен успешно!")
        log_info("🌐 Доступ: http://localhost:8080")
        log_info("🔐 Тестовые аккаунты:")
        log_info("   Admin: admin@admin.com / admin")
        log_info("   Owner: john@example.com / password")
        log_info("🛑 Для остановки нажмите Ctrl+C")
        log_info("=" * 50)
        
        ui.run(
            port=8080,
            title='Cat Database Management System',
            show=True,
            reload=True,
        )
        
    except KeyboardInterrupt:
        log_info("Остановка сервера...")
    except Exception as e:
        log_error(f"Ошибка запуска: {e}")
        sys.exit(1)
