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
    
    @classmethod
    def ensure_photos_dir(cls) -> str:
        """Ensure photos directory exists and return its path"""
        if not os.path.exists(cls.PHOTOS_DIR):
            os.makedirs(cls.PHOTOS_DIR)
        return cls.PHOTOS_DIR
    
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
    def compress_image(cls, file_content: bytes, target_size_kb: int = 500) -> bytes:
        """
        Compress image to target size
        Returns: compressed image bytes
        """
        try:
            # Open image
            image = PILImage.open(io.BytesIO(file_content))
            
            # Convert to RGB if necessary (for JPEG)
            if image.mode in ('RGBA', 'LA', 'P'):
                image = image.convert('RGB')
            
            # Start with high quality and reduce until target size is reached
            quality = 95
            target_size_bytes = target_size_kb * 1024
            
            while quality > 10:
                output = io.BytesIO()
                image.save(output, format='JPEG', quality=quality, optimize=True)
                compressed_size = len(output.getvalue())
                
                if compressed_size <= target_size_bytes:
                    return output.getvalue()
                
                quality -= 10
            
            # If still too large, resize the image
            while quality > 10:
                # Resize image
                width, height = image.size
                new_width = int(width * 0.8)
                new_height = int(height * 0.8)
                resized_image = image.resize((new_width, new_height), PILImage.Resampling.LANCZOS)
                
                output = io.BytesIO()
                resized_image.save(output, format='JPEG', quality=quality, optimize=True)
                compressed_size = len(output.getvalue())
                
                if compressed_size <= target_size_bytes:
                    return output.getvalue()
                
                quality -= 10
                image = resized_image
            
            # Return the smallest we could get
            output = io.BytesIO()
            image.save(output, format='JPEG', quality=10, optimize=True)
            return output.getvalue()
            
        except Exception as e:
            print(f"Error compressing image: {e}")
            return file_content  # Return original if compression fails

    @classmethod
    def save_photo(cls, file_content: bytes, original_filename: str) -> Optional[str]:
        """
        Save photo file and return the saved path
        Returns: saved_path or None if failed
        """
        try:
            # Generate unique filename (always use .jpg for compressed images)
            unique_filename = f"{uuid.uuid4()}.jpg"
            
            # Ensure directory exists
            photos_dir = cls.ensure_photos_dir()
            file_path = os.path.join(photos_dir, unique_filename)
            
            # Compress image if it's too large
            original_size = len(file_content)
            if original_size > 500 * 1024:  # If larger than 500KB
                file_content = cls.compress_image(file_content, 500)
                print(f"Compressed image from {original_size // 1024}KB to {len(file_content) // 1024}KB")
            
            # Save file
            with open(file_path, 'wb') as f:
                f.write(file_content)
            
            print(f"Photo saved to: {file_path}")
            return file_path
            
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
        url = f"/static/{photo_path}"
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
