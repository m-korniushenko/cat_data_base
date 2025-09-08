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



@app.exception_handler(Exception)
async def swallow_disconnects(request: Request, exc: Exception):
    name = type(exc).__name__
    if name in ('ClientDisconnect', 'CancelledError', 'WebSocketDisconnect', 'RuntimeError'):
        return Response(status_code=499)
    raise exc


@ui.page('/')
async def main_page():
    await main_page_render()


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


def start_db():
    if not check_creds():
        sys.exit()
    drop_database_if_exists()
    postgres_check_and_create_database(Base)
    if not check_db_connection():
        sys.exit()
    start_add_workflow()


if __name__ in {"__main__", "__mp_main__"}:
    start_db()
    ui.run(
        port=8080,
        title='Cat Database Management System',
        show=True,
        reload=True,
    )