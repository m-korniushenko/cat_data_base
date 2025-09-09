"""
File service for managing cat files
"""
import os
import uuid
from pathlib import Path
from nicegui import ui


class FileService:
    """Service class for file management"""
    
    # Configuration
    FILES_DIR = "cat_files"
    ALLOWED_EXTENSIONS = {'.pdf', '.doc', '.docx', '.txt', '.jpg', '.jpeg', '.png', '.gif', '.zip', '.rar'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    @staticmethod
    def get_cat_files_dir(microchip: str) -> Path:
        """Get the directory path for a cat's files"""
        return Path(FileService.FILES_DIR) / microchip
    
    @staticmethod
    def is_valid_file(upload_event) -> tuple[bool, str]:
        """Check if uploaded file is valid"""
        try:
            # Check file extension first
            filename = upload_event.name
            if not filename:
                return False, "No filename provided"
                
            file_ext = Path(filename).suffix.lower()
            if file_ext not in FileService.ALLOWED_EXTENSIONS:
                allowed_types = ', '.join(FileService.ALLOWED_EXTENSIONS)
                return False, f"File type {file_ext} not allowed. Allowed types: {allowed_types}"
            
            # Check file size by reading content length
            if hasattr(upload_event, 'content'):
                content = upload_event.content
                if hasattr(content, 'read'):
                    # For SpooledTemporaryFile, we need to read and check size
                    current_pos = content.tell()
                    content.seek(0, 2)  # Seek to end
                    file_size = content.tell()
                    content.seek(current_pos)  # Reset position
                    
                    if file_size > FileService.MAX_FILE_SIZE:
                        max_mb = FileService.MAX_FILE_SIZE // (1024*1024)
                        return False, f"File size exceeds {max_mb}MB limit"
            
            return True, ""
            
        except Exception as e:
            return False, f"Error validating file: {str(e)}"
    
    @staticmethod
    def save_file(microchip: str, upload_event) -> tuple[bool, str, str]:
        """Save uploaded file to cat's directory"""
        try:
            if not microchip:
                return False, "Microchip is required", ""
            
            # Validate file
            is_valid, error_msg = FileService.is_valid_file(upload_event)
            if not is_valid:
                return False, error_msg, ""
            
            # Create directory if it doesn't exist
            files_dir = FileService.get_cat_files_dir(microchip)
            files_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate unique filename while preserving original name
            original_filename = upload_event.name
            file_stem = Path(original_filename).stem
            file_ext = Path(original_filename).suffix
            
            # Create unique filename: original_name_uuid.ext
            unique_filename = f"{file_stem}_{uuid.uuid4().hex[:8]}{file_ext}"
            file_path = files_dir / unique_filename
            
            # Save file
            with open(file_path, 'wb') as f:
                content = upload_event.content
                if hasattr(content, 'read'):
                    # For SpooledTemporaryFile, read the content
                    content.seek(0)  # Reset to beginning
                    f.write(content.read())
                else:
                    # For other types, write directly
                    f.write(content)
            
            # Return relative path for database storage
            relative_path = f"{FileService.FILES_DIR}/{microchip}/{unique_filename}"
            return True, "File saved successfully", relative_path
            
        except Exception as e:
            return False, f"Error saving file: {str(e)}", ""
    
    @staticmethod
    def delete_file(file_path: str) -> bool:
        """Delete a file from disk"""
        try:
            # Normalize path for file system
            normalized_path = file_path.replace('/', '\\') if os.name == 'nt' else file_path
            full_path = Path(normalized_path)
            
            if full_path.exists():
                full_path.unlink()
                return True
            return False
            
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")
            return False
    
    @staticmethod
    def move_cat_files(old_microchip: str, new_microchip: str) -> bool:
        """Move all files from old microchip directory to new one"""
        try:
            old_dir = FileService.get_cat_files_dir(old_microchip)
            new_dir = FileService.get_cat_files_dir(new_microchip)
            
            if not old_dir.exists():
                return True  # Nothing to move
            
            # Create new directory
            new_dir.mkdir(parents=True, exist_ok=True)
            
            # Move all files
            for file_path in old_dir.iterdir():
                if file_path.is_file():
                    new_file_path = new_dir / file_path.name
                    file_path.rename(new_file_path)
            
            # Remove old directory if empty
            try:
                old_dir.rmdir()
            except OSError:
                pass  # Directory not empty, that's fine
            
            return True
            
        except Exception as e:
            print(f"Error moving cat files from {old_microchip} to {new_microchip}: {e}")
            return False
    
    @staticmethod
    def update_file_paths_in_database(file_paths: list, old_microchip: str, new_microchip: str) -> list:
        """Update file paths in database by replacing old microchip with new one"""
        try:
            updated_paths = []
            for path in file_paths:
                if path and old_microchip in path:
                    updated_path = path.replace(f"{FileService.FILES_DIR}/{old_microchip}/", f"{FileService.FILES_DIR}/{new_microchip}/")
                    updated_paths.append(updated_path)
                else:
                    updated_paths.append(path)
            return updated_paths
            
        except Exception as e:
            print(f"Error updating file paths: {e}")
            return file_paths
    
    @staticmethod
    def ensure_file_directory_renamed(old_microchip: str, new_microchip: str) -> bool:
        """Ensure the file directory is renamed when microchip changes"""
        return FileService.move_cat_files(old_microchip, new_microchip)
    
    @staticmethod
    def get_file_url(file_path: str) -> str:
        """Get URL for serving file"""
        # Normalize path for web serving (forward slashes)
        web_path = file_path.replace('\\', '/')
        return f"/static/{web_path}"
    
    @staticmethod
    def create_file_list(files: list, max_width: str = "600px") -> None:
        """Create a file list display"""
        if not files:
            ui.label("No files uploaded").classes('text-gray-500')
            return
        
        with ui.column().classes('w-full'):
            ui.label("Files:").classes('text-h6 mb-2')
            
            for i, file_path in enumerate(files):
                if not file_path:
                    continue
                    
                # Get filename from path and extract original name
                full_filename = Path(file_path).name
                # Remove UUID part to show original filename
                if '_' in full_filename:
                    parts = full_filename.split('_')
                    if len(parts) >= 2:
                        # Check if last part looks like UUID (8 hex characters)
                        last_part = parts[-1]
                        file_ext = Path(last_part).suffix
                        uuid_part = last_part.replace(file_ext, '')
                        if len(uuid_part) == 8 and all(c in '0123456789abcdef' for c in uuid_part.lower()):
                            # Remove the UUID part and rejoin
                            original_name = '_'.join(parts[:-1]) + file_ext
                        else:
                            original_name = full_filename
                    else:
                        original_name = full_filename
                else:
                    original_name = full_filename
                    
                file_url = FileService.get_file_url(file_path)
                
                with ui.row().classes('items-center gap-2 mb-1'):
                    # File icon based on extension
                    file_ext = Path(file_path).suffix.lower()
                    if file_ext in ['.pdf']:
                        icon = '📄'
                    elif file_ext in ['.doc', '.docx']:
                        icon = '📝'
                    elif file_ext in ['.txt']:
                        icon = '📃'
                    elif file_ext in ['.jpg', '.jpeg', '.png', '.gif']:
                        icon = '🖼️'
                    elif file_ext in ['.zip', '.rar']:
                        icon = '📦'
                    else:
                        icon = '📎'
                    
                    ui.label(f"{icon} {original_name}").classes('text-sm')
                    
                    # Download button
                    ui.button('Download', 
                             on_click=lambda url=file_url: ui.download(url)
                             ).props('size=sm color=primary flat')
