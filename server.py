import sys
import fastapi
from app.handlers_folder.cat import *
from app.handlers_folder.owner import *
from app.handlers_folder.history import *
from system_functions_folder.check_cread import check_creds
from app.database_folder.postgres import (check_db_connection,
                                          postgres_check_and_create_database,
                                          drop_database_if_exists)
import uvicorn
from app.database_folder.model import Base


app = fastapi.FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/login")
def login():
    return ...


@app.get("/logout")
def logout():
    return ...


@app.get("/api/get_cat")
def get_cat():
    return ...


@app.post("/api/add_cat")
def add_cat(cat: dict):
    return ...


@app.delete("/api/delete_cat")
def delete_cat(cat_id: int):
    return ...


@app.put("/api/update_cat")
def update_cat(cat_id: int, cat: dict):
    return ...


@app.get("/api/get_owner")
def get_owner():
    return ...


@app.post("/api/add_owner")
def add_owner(owner: dict):
    return ...


@app.delete("/api/delete_owner")
def delete_owner(owner_id: int):
    return ...


@app.put("/api/update_owner")
def update_owner(owner_id: int, owner: dict):
    return ...


def main():
    if not check_creds():
        sys.exit()
    drop_database_if_exists()
    postgres_check_and_create_database(Base)
    if not check_db_connection():
        sys.exit()


if __name__ == "__main__":
    main()
    # uvicorn.run(app, host="0.0.0.0", port=8000)