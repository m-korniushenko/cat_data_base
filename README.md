# 🐱 Cat Database Management System

A modern web application built with FastAPI and NiceGUI for managing cat and owner information.

## Features

-   **🐱 Cat Management**: Add, edit, delete, and view cat information
-   **👤 Owner Management**: Manage cat owners with permissions
-   **📊 Dashboard**: Overview of database statistics
-   **🔐 Authentication**: Secure login system
-   **📱 Modern UI**: Beautiful and responsive interface with NiceGUI
-   **🔌 REST API**: Full REST API for programmatic access

## Tech Stack

-   **Backend**: FastAPI (Python)
-   **Frontend**: NiceGUI (Python-based UI framework)
-   **Database**: PostgreSQL with SQLAlchemy ORM
-   **Authentication**: JWT-based authentication

## Installation

1. **Clone the repository**:

    ```bash
    git clone <repository-url>
    cd cat_data_base
    ```

2. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

3. **Set up environment variables**:
   Create a `.env` file in the root directory:

    ```env
    DATABASE_URL=postgresql://username:password@localhost:5432/cat_database
    JWT_SECRET=your-secret-key
    ```

4. **Initialize the database**:
    ```bash
    python -c "from server import start_db; start_db()"
    ```

## Running the Application

### Option 1: Using the startup script

```bash
python run.py
```

### Option 2: Direct execution

```bash
python server.py
```

### Option 3: Separate FastAPI and NiceGUI

```bash
# Terminal 1: FastAPI server
uvicorn server:app --host 127.0.0.1 --port 8000 --reload

# Terminal 2: NiceGUI interface
python -c "from server import ui; ui.run(port=8080)"
```

## Access Points

-   **🌐 Web Interface**: http://127.0.0.1:8080
-   **📊 API Documentation**: http://127.0.0.1:8000/docs
-   **🔌 API Base URL**: http://127.0.0.1:8000/api

## API Endpoints

### Cats

-   `GET /api/cats` - Get all cats
-   `GET /api/cats/{cat_id}` - Get specific cat
-   `POST /api/cats` - Create new cat
-   `PUT /api/cats/{cat_id}` - Update cat
-   `DELETE /api/cats/{cat_id}` - Delete cat

### Owners

-   `GET /api/owners` - Get all owners
-   `GET /api/owners/{owner_id}` - Get specific owner
-   `POST /api/owners` - Create new owner
-   `PUT /api/owners/{owner_id}` - Update owner
-   `DELETE /api/owners/{owner_id}` - Delete owner

### Health Check

-   `GET /api/health` - System health status

## Database Schema

### Cats Table

-   `cat_id` (Primary Key)
-   `owner_id` (Foreign Key)
-   `cat_firstname`
-   `cat_surname`
-   `cat_gender`
-   `cat_birthday`
-   `cat_microchip_number`
-   `cat_breed`
-   `cat_colour`
-   `cat_litter`
-   `cat_ifc`

### Owners Table

-   `owner_id` (Primary Key)
-   `owner_firstname`
-   `owner_surname`
-   `owner_mail`
-   `owner_hashed_password`
-   `owner_permission`

## Usage

1. **Start the application** using one of the methods above
2. **Navigate to the web interface** at http://127.0.0.1:8080
3. **Use the navigation** to switch between Cats and Owners management
4. **Add, edit, or delete** records using the intuitive interface
5. **Use the API** for programmatic access to the data

## Development

### Project Structure

```
cat_data_base/
├── app/
│   ├── database_folder/     # Database models and ORM
│   ├── fast_ui/            # FastUI components
│   └── handlers_folder/    # Request handlers
├── system_functions_folder/ # System utilities
├── server.py               # Main FastAPI + NiceGUI application
├── run.py                  # Startup script
└── requirements.txt        # Python dependencies
```

### Adding New Features

1. **Database Models**: Add new models in `app/database_folder/model.py`
2. **ORM Methods**: Add CRUD operations in `app/database_folder/orm.py`
3. **API Endpoints**: Add new endpoints in `server.py`
4. **UI Components**: Add new pages in `server.py` using NiceGUI

## Troubleshooting

### Common Issues

1. **Database Connection Error**:

    - Check your `.env` file configuration
    - Ensure PostgreSQL is running
    - Verify database credentials

2. **Port Already in Use**:

    - Change ports in `server.py` or `run.py`
    - Kill existing processes using the ports

3. **Import Errors**:
    - Ensure all dependencies are installed: `pip install -r requirements.txt`
    - Check Python path and virtual environment

### Logs

Check the console output for detailed error messages and logs.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please open an issue in the repository.
