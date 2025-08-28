# Cat Database Management System

A comprehensive cat breeding and management system built with Python, SQLAlchemy, and NiceGUI.

## Features

### Core Entities

1. **Cats** - Complete cat profiles with:

    - Basic information (name, gender, birth/death dates)
    - Identifiers (microchip, studbook numbers)
    - Breed and color information (including EMS color codes)
    - Genetic data (inbreeding coefficient)
    - Show results and titles
    - Relationships to litters, breeders, and owners

2. **Owners** - Cat owners with contact information and permissions

3. **Litters** - Breeding litters with:

    - Litter name and date
    - Parent relationships (mother and father cats)

4. **Breeders** - Professional breeders with:

    - Contact information
    - Address details
    - Associated cats

5. **Cat Documents** - Document management for:
    - Photos
    - Veterinary reports
    - Certificates
    - Other cat-related documents

### Database Structure

The system uses PostgreSQL with the following main tables:

-   `cat` - Main cat information with relationships
-   `owner` - Cat owners
-   `litter` - Breeding litters
-   `breeder` - Professional breeders
-   `cat_document` - Associated documents
-   `history` - System activity log
-   `cat_connection` - Cat relationships
-   `cat_type` - Cat type classifications
-   `owner_permission` - User permissions
-   `country_city` - Location data

### Key Features

-   **Modern UI**: Built with NiceGUI for a responsive web interface
-   **Relationship Management**: Proper foreign key relationships between entities
-   **Data Validation**: Pydantic models for data validation
-   **Async Operations**: Full async/await support for database operations
-   **Extensible**: Easy to add new features and entities

## Installation

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Configure database connection in `config.py`

3. Run the application:

```bash
python server.py
```

## Usage

### Adding Cats

-   Navigate to "Add Cat" page
-   Fill in basic information
-   Select owner, litter, and breeder from dropdowns
-   Add optional information like show results and titles

### Managing Litters

-   Navigate to "Litters" page
-   Add new litters with parent information
-   View existing litters and their relationships

### Managing Breeders

-   Navigate to "Breeders" page
-   Add new breeders with contact information
-   View and manage breeder profiles

### Viewing Data

-   Dashboard shows statistics for all entities
-   Individual pages for viewing and managing each entity type
-   Search and filter capabilities

## Database Schema

### Cat Table

-   `cat_id` (Primary Key)
-   `cat_firstname`, `cat_surname`
-   `cat_gender`, `cat_birthday`, `cat_date_of_death`
-   `cat_microchip_number`, `cat_studbook_number`
-   `cat_breed`, `cat_EMS_colour`
-   `cat_inbreeding_coefficient`
-   `litter_id`, `breeder_id`, `owner_id` (Foreign Keys)
-   `cat_show_results`, `cat_title`

### Litter Table

-   `litter_id` (Primary Key)
-   `litter_name`, `litter_date`
-   `mother_id`, `father_id` (Foreign Keys to Cat)

### Breeder Table

-   `breeder_id` (Primary Key)
-   `name`, `mail`, `phone`
-   `address`, `city`, `zip`

## Development

The system is built with:

-   **Backend**: Python, SQLAlchemy, FastAPI
-   **Frontend**: NiceGUI
-   **Database**: PostgreSQL
-   **Validation**: Pydantic

### Project Structure

```
cat_data_base/
├── app/
│   ├── database_folder/     # Database models and ORM
│   ├── handlers_folder/     # API handlers
│   └── niceGUI_folder/      # UI components
├── system_functions_folder/ # System utilities
├── server.py               # Main application
└── requirements.txt        # Dependencies
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.
