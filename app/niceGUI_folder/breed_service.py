"""
Breed service for business logic related to breeds
"""
from app.database_folder.orm import AsyncOrm
from app.niceGUI_folder.validators import BreederValidator


class BreedService:
    """Service class for breed-related business logic"""
    
    @staticmethod
    async def get_breed_data(breed_id: int):
        """Get breed data by ID"""
        try:
            breed = await AsyncOrm.get_breed_by_id(breed_id)
            if not breed:
                return None
            
            return {
                'breed_id': breed.breed_id,
                'breed_firstname': breed.breed_firstname,
                'breed_lastname': breed.breed_surname,
                'breed_email': breed.breed_email,
                'breed_phone': breed.breed_phone,
                'breed_gender': breed.breed_gender,
                'breed_birthday': breed.breed_birthday,
                'breed_address': breed.breed_address,
                'breed_city': breed.breed_city,
                'breed_country': breed.breed_country,
                'breed_zip': breed.breed_zip,
                'breed_description': breed.breed_description
            }
        except Exception as e:
            print(f"Error getting breed data: {e}")
            return None
    
    @staticmethod
    async def validate_breed_data(breed_data: dict):
        """Validate breed data"""
        try:
            validator = BreederValidator()
            result = validator.validate(breed_data)
            return result.is_valid, '; '.join(result.errors) if result.errors else ''
        except Exception as e:
            print(f"Error validating breed data: {e}")
            return False, str(e)
    
    @staticmethod
    async def validate_breed_data_for_edit(breed_data: dict):
        """Validate breed data for editing (less strict)"""
        try:
            # Convert breed_data to format expected by validator
            validator_data = {
                'firstname': breed_data.get('breed_firstname', ''),
                'surname': breed_data.get('breed_lastname', ''),
                'email': breed_data.get('breed_email', '')
            }
            
            validator = BreederValidator()
            result = validator.validate(validator_data)
            return result.is_valid, '; '.join(result.errors) if result.errors else ''
        except Exception as e:
            print(f"Error validating breed data for edit: {e}")
            return False, str(e)
    
    @staticmethod
    async def update_breed(breed_id: int, breed_data: dict):
        """Update breed in database"""
        try:
            # Validate data
            is_valid, error_message = await BreedService.validate_breed_data_for_edit(breed_data)
            if not is_valid:
                return False, f"Validation failed: {error_message}"
            
            # Update in database
            success = await AsyncOrm.update_breed(breed_id, breed_data)
            if success:
                return True, "Breed updated successfully"
            else:
                return False, "Failed to update breed in database"
                
        except Exception as e:
            print(f"Error updating breed: {e}")
            return False, f"Error updating breed: {str(e)}"
    
    @staticmethod
    async def delete_breed(breed_id: int):
        """Delete breed from database"""
        try:
            success = await AsyncOrm.delete_breed(breed_id)
            if success:
                return True, "Breed deleted successfully"
            else:
                return False, "Failed to delete breed from database"
                
        except Exception as e:
            print(f"Error deleting breed: {e}")
            return False, f"Error deleting breed: {str(e)}"
