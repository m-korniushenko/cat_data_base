"""
Photo Service for handling cat photos
Following SOLID principles - Single Responsibility Principle
"""
import os
import uuid
from typing import List, Optional
from nicegui import ui
import shutil
from PIL import Image as PILImage
import io


class PhotoService:
    """Service for managing cat photos"""
    
    PHOTOS_DIR = "cat_photos"
    ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
    MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB
    STANDARD_SIZE = (400, 400)  # Standard square size for all photos
    
    @classmethod
    def ensure_photos_dir(cls) -> str:
        """Ensure photos directory exists and return its path"""
        if not os.path.exists(cls.PHOTOS_DIR):
            os.makedirs(cls.PHOTOS_DIR)
        return cls.PHOTOS_DIR
    
    @classmethod
    def get_cat_photos_dir(cls, microchip: str) -> str:
        """Get photos directory for a specific cat microchip"""
        if not microchip:
            # If no microchip, use a default directory
            microchip = "no_microchip"
        
        # Clean microchip for use as directory name
        clean_microchip = "".join(c for c in microchip if c.isalnum() or c in ('-', '_')).strip()
        if not clean_microchip:
            clean_microchip = "no_microchip"
        
        cat_dir = os.path.join(cls.PHOTOS_DIR, clean_microchip)
        if not os.path.exists(cat_dir):
            os.makedirs(cat_dir)
        return cat_dir
    
    @classmethod
    def move_cat_photos(cls, old_microchip: str, new_microchip: str) -> bool:
        """Move photos from old microchip directory to new microchip directory"""
        try:
            print(f"Moving photos from microchip '{old_microchip}' to '{new_microchip}'")
            
            if not old_microchip or not new_microchip:
                print("Skipping move: missing microchip values")
                return False
            
            # Clean microchip names for directory names
            old_clean = "".join(c for c in old_microchip if c.isalnum() or c in ('-', '_')).strip()
            if not old_clean:
                old_clean = "no_microchip"
            
            old_dir = os.path.join(cls.PHOTOS_DIR, old_clean)
            new_dir = cls.get_cat_photos_dir(new_microchip)
            
            print(f"Old directory: {old_dir}")
            print(f"New directory: {new_dir}")
            print(f"Old directory exists: {os.path.exists(old_dir)}")
            print(f"New directory exists: {os.path.exists(new_dir)}")
            
            if os.path.exists(old_dir) and old_dir != new_dir:
                # Ensure new directory exists
                os.makedirs(new_dir, exist_ok=True)
                
                if os.path.exists(new_dir):
                    # Move all files from old directory to new directory
                    print(f"Moving files from {old_dir} to {new_dir}")
                    files_moved = 0
                    for filename in os.listdir(old_dir):
                        old_path = os.path.join(old_dir, filename)
                        new_path = os.path.join(new_dir, filename)
                        if os.path.isfile(old_path):
                            try:
                                # If file already exists in new directory, remove it first
                                if os.path.exists(new_path):
                                    os.remove(new_path)
                                shutil.move(old_path, new_path)
                                print(f"  Moved file: {filename}")
                                files_moved += 1
                            except Exception as e:
                                print(f"  Error moving file {filename}: {e}")
                    
                    # Remove old directory if empty
                    try:
                        if not os.listdir(old_dir):
                            print(f"Removing empty directory: {old_dir}")
                            os.rmdir(old_dir)
                        else:
                            print(f"Old directory not empty, keeping: {old_dir}")
                    except Exception as e:
                        print(f"Error removing old directory: {e}")
                    
                    print(f"Successfully moved {files_moved} files from {old_dir} to {new_dir}")
                    return True
                else:
                    print(f"Failed to create new directory: {new_dir}")
                    return False
            else:
                print("No move needed: directories are the same or old directory doesn't exist")
                return True
        except Exception as e:
            print(f"Error moving cat photos: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    @classmethod
    def is_valid_photo(cls, filename: str, file_size: int = None) -> tuple[bool, str]:
        """
        Validate photo file
        Returns: (is_valid, error_message)
        """
        if not filename:
            return False, "No file selected"
        
        # Check file extension
        _, ext = os.path.splitext(filename.lower())
        if ext not in cls.ALLOWED_EXTENSIONS:
            return False, f"Invalid file type. Allowed: {', '.join(cls.ALLOWED_EXTENSIONS)}"
        
        # Check file size if provided
        if file_size is not None and file_size > cls.MAX_FILE_SIZE:
            return False, f"File too large. Maximum size: {cls.MAX_FILE_SIZE // (1024*1024)}MB"
        
        return True, ""
    
    @classmethod
    def standardize_image(cls, file_content: bytes, target_size_kb: int = 500) -> bytes:
        """
        Standardize image to 400x400 square format and compress to target size
        Returns: standardized and compressed image bytes
        """
        try:
            # Open image
            image = PILImage.open(io.BytesIO(file_content))
            
            # Convert to RGB if necessary (for JPEG)
            if image.mode in ('RGBA', 'LA', 'P'):
                image = image.convert('RGB')
            
            # Resize to standard square size (400x400) with smart cropping
            image = cls._resize_to_square(image, cls.STANDARD_SIZE)
            
            # Compress to target size
            quality = 95
            target_size_bytes = target_size_kb * 1024
            
            while quality > 10:
                output = io.BytesIO()
                image.save(output, format='JPEG', quality=quality, optimize=True)
                compressed_size = len(output.getvalue())
                
                if compressed_size <= target_size_bytes:
                    return output.getvalue()
                
                quality -= 10
            
            # Final fallback - return the last attempt
            return output.getvalue()
            
        except Exception as e:
            print(f"Error standardizing image: {e}")
            return file_content
    
    @classmethod
    def _resize_to_square(cls, image: PILImage.Image, target_size: tuple) -> PILImage.Image:
        """
        Resize image to square format with smart cropping
        """
        width, height = image.size
        target_width, target_height = target_size
        
        # Calculate scaling factor to fit the image in the target size
        scale_factor = min(target_width / width, target_height / height)
        
        # Calculate new dimensions
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        
        # Resize image maintaining aspect ratio
        resized_image = image.resize((new_width, new_height), PILImage.Resampling.LANCZOS)
        
        # Create a new square image with white background
        square_image = PILImage.new('RGB', target_size, (255, 255, 255))
        
        # Calculate position to center the resized image
        x_offset = (target_width - new_width) // 2
        y_offset = (target_height - new_height) // 2
        
        # Paste the resized image onto the square background
        square_image.paste(resized_image, (x_offset, y_offset))
        
        return square_image

    @classmethod
    def save_photo(cls, file_content: bytes, original_filename: str, microchip: str = None) -> Optional[str]:
        """
        Save photo file and return the saved path
        Returns: saved_path or None if failed
        """
        try:
            # Generate unique filename (always use .jpg for compressed images)
            unique_filename = f"{uuid.uuid4()}.jpg"
            
            # Get cat-specific directory
            cat_photos_dir = cls.get_cat_photos_dir(microchip)
            file_path = os.path.join(cat_photos_dir, unique_filename)
            
            # Standardize and compress image
            original_size = len(file_content)
            file_content = cls.standardize_image(file_content, 500)
            print(f"Standardized image from {original_size // 1024}KB to {len(file_content) // 1024}KB")
            
            # Save file
            with open(file_path, 'wb') as f:
                f.write(file_content)
            
            print(f"Photo saved to: {file_path}")
            # Return relative path for database storage with normalized separators
            normalized_path = file_path.replace('\\', '/')
            return normalized_path
            
        except Exception as e:
            print(f"Error saving photo: {e}")
            return None
    
    @classmethod
    def delete_photo(cls, photo_path: str) -> bool:
        """Delete photo file"""
        try:
            if os.path.exists(photo_path):
                os.remove(photo_path)
                return True
        except Exception as e:
            print(f"Error deleting photo: {e}")
        return False
    
    @classmethod
    def delete_photos(cls, photo_paths: List[str]) -> bool:
        """Delete multiple photo files"""
        success = True
        for path in photo_paths:
            if not cls.delete_photo(path):
                success = False
        return success
    
    @classmethod
    def get_photo_url(cls, photo_path: str) -> str:
        """Get URL for photo display"""
        if not photo_path:
            return ""
        
        # Check if file exists
        if not os.path.exists(photo_path):
            print(f"Photo file does not exist: {photo_path}")
            return ""
        
        # Convert to relative path for web serving
        # photo_path is already relative to project root
        # Normalize path separators for web (use forward slashes)
        normalized_path = photo_path.replace('\\', '/')
        url = f"/static/{normalized_path}"
        print(f"Generated photo URL: {url}")
        return url
    
    @classmethod
    def create_photo_upload_widget(cls, on_upload_callback=None) -> ui.upload:
        """Create photo upload widget"""
        upload = ui.upload(
            on_upload=on_upload_callback,
            auto_upload=True,
            max_file_size=cls.MAX_FILE_SIZE
        ).props('accept=image/*').classes('w-full')
        
        return upload
    
    @classmethod
    def create_photo_gallery(cls, photo_paths: List[str], max_width: str = "400px") -> ui.row:
        """Create photo gallery display"""
        print(f"Creating photo gallery with {len(photo_paths)} photos: {photo_paths}")
        gallery = ui.row().classes('flex-wrap gap-4 p-2 w-full')
        
        for i, photo_path in enumerate(photo_paths):
            print(f"Processing photo {i+1}: {photo_path}")
            if photo_path and os.path.exists(photo_path):
                print(f"Photo {i+1} exists, adding to gallery")
                with gallery:
                    # Convert local path to URL for web display
                    photo_url = cls.get_photo_url(photo_path)
                    print(f"Displaying photo: {photo_path} -> {photo_url}")
                    if photo_url:
                        # Try using ui.image with proper URL
                        try:
                            # Use direct CSS styles for better control
                            ui.html(f'<img src="{photo_url}" style="max-width: 400px; width: 100%; height: auto; border-radius: 12px; box-shadow: 0 4px 8px rgba(0,0,0,0.15); transition: box-shadow 0.3s ease; cursor: pointer; margin: 8px;" onmouseover="this.style.boxShadow=\'0 8px 16px rgba(0,0,0,0.2)\'" onmouseout="this.style.boxShadow=\'0 4px 8px rgba(0,0,0,0.15)\'" />')
                            print(f"Successfully added photo {i+1} with direct HTML")
                        except Exception as e:
                            print(f"Error displaying image: {e}")
                            # Fallback to ui.image
                            ui.image(photo_url).classes('max-w-md rounded-lg shadow-lg hover:shadow-xl transition-shadow cursor-pointer')
                            print(f"Successfully added photo {i+1} with ui.image fallback")
            else:
                print(f"Photo {i+1} does not exist or is empty: {photo_path}")
        
        print(f"Gallery created with {len(gallery.default_slot.children) if hasattr(gallery, 'default_slot') else 'unknown'} children")
        return gallery
    
    @classmethod
    def update_photo_paths(cls, old_photo_paths: List[str], old_microchip: str, new_microchip: str) -> List[str]:
        """Update photo paths when microchip changes"""
        print(f"Updating photo paths: {len(old_photo_paths)} photos from '{old_microchip}' to '{new_microchip}'")
        
        if not old_photo_paths or old_microchip == new_microchip:
            print("No update needed: no photos or microchip unchanged")
            return old_photo_paths
        
        try:
            # Move photos to new directory
            print("Step 1: Moving photos to new directory")
            cls.move_cat_photos(old_microchip, new_microchip)
            
            # Update paths in the list
            print("Step 2: Updating photo paths in list")
            new_paths = []
            for i, old_path in enumerate(old_photo_paths):
                print(f"Processing photo {i+1}: {old_path}")
                if old_path and os.path.exists(old_path):
                    # Extract filename from old path
                    filename = os.path.basename(old_path)
                    print(f"  Filename: {filename}")
                    
                    # Create new path with new microchip directory
                    new_dir = cls.get_cat_photos_dir(new_microchip)
                    new_path = os.path.join(new_dir, filename)
                    # Normalize path separators for consistency
                    normalized_path = new_path.replace('\\', '/')
                    
                    print(f"  New path: {normalized_path}")
                    print(f"  New path exists: {os.path.exists(new_path)}")
                    
                    new_paths.append(normalized_path)
                else:
                    print(f"  File doesn't exist, keeping old path: {old_path}")
                    # Keep old path if file doesn't exist
                    new_paths.append(old_path)
            
            print(f"Final updated photo paths: {new_paths}")
            return new_paths
        except Exception as e:
            print(f"Error updating photo paths: {e}")
            import traceback
            traceback.print_exc()
            return old_photo_paths
    
    @classmethod
    def ensure_photo_directory_renamed(cls, old_microchip: str, new_microchip: str) -> bool:
        """Ensure photo directory is renamed after microchip change"""
        try:
            print(f"Ensuring photo directory is renamed from '{old_microchip}' to '{new_microchip}'")
            
            if not old_microchip or not new_microchip or old_microchip == new_microchip:
                print("No rename needed: missing microchip or same microchip")
                return True
            
            # Clean microchip names for directory names
            old_clean = "".join(c for c in old_microchip if c.isalnum() or c in ('-', '_')).strip()
            if not old_clean:
                old_clean = "no_microchip"
            
            new_clean = "".join(c for c in new_microchip if c.isalnum() or c in ('-', '_')).strip()
            if not new_clean:
                new_clean = "no_microchip"
            
            old_dir = os.path.join(cls.PHOTOS_DIR, old_clean)
            new_dir = os.path.join(cls.PHOTOS_DIR, new_clean)
            
            print(f"Checking directories: {old_dir} -> {new_dir}")
            
            if os.path.exists(old_dir) and old_dir != new_dir:
                print(f"Old directory exists, moving to new directory")
                return cls.move_cat_photos(old_microchip, new_microchip)
            elif os.path.exists(new_dir):
                print(f"New directory already exists: {new_dir}")
                return True
            else:
                print(f"No old directory found, nothing to move")
                return True
                
        except Exception as e:
            print(f"Error ensuring directory rename: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    @classmethod
    def update_photo_paths_in_database(cls, old_photo_paths: List[str], old_microchip: str, new_microchip: str) -> List[str]:
        """Update photo paths in database by replacing old microchip with new microchip in path names"""
        try:
            print(f"Updating photo paths in database: replacing '{old_microchip}' with '{new_microchip}'")
            
            if not old_photo_paths or old_microchip == new_microchip:
                print("No path update needed: no photos or microchip unchanged")
                return old_photo_paths
            
            # Clean microchip names for directory names
            old_clean = "".join(c for c in old_microchip if c.isalnum() or c in ('-', '_')).strip()
            if not old_clean:
                old_clean = "no_microchip"
            
            new_clean = "".join(c for c in new_microchip if c.isalnum() or c in ('-', '_')).strip()
            if not new_clean:
                new_clean = "no_microchip"
            
            updated_paths = []
            for i, old_path in enumerate(old_photo_paths):
                print(f"Processing path {i+1}: {old_path}")
                
                if old_path and old_clean in old_path:
                    # Replace old microchip directory with new one in the path
                    new_path = old_path.replace(old_clean, new_clean)
                    print(f"  Updated path: {old_path} -> {new_path}")
                    updated_paths.append(new_path)
                else:
                    print(f"  No change needed: {old_path}")
                    updated_paths.append(old_path)
            
            print(f"Final updated paths for database: {updated_paths}")
            return updated_paths
            
        except Exception as e:
            print(f"Error updating photo paths in database: {e}")
            import traceback
            traceback.print_exc()
            return old_photo_paths
