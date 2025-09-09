"""
Owner service for business logic related to owners
"""
from app.database_folder.orm import AsyncOrm
from app.niceGUI_folder.validators import OwnerValidator


class OwnerService:
    """Service class for owner-related business logic"""
    
    @staticmethod
    async def get_owner_data(owner_id: int):
        """Get owner data by ID"""
        try:
            owner = await AsyncOrm.get_owner_by_id(owner_id)
            if not owner:
                return None
            
            return {
                'owner_id': owner.owner_id,
                'owner_firstname': owner.owner_firstname,
                'owner_lastname': owner.owner_surname,
                'owner_email': owner.owner_email,
                'owner_phone': owner.owner_phone,
                'owner_address': owner.owner_address
            }
        except Exception as e:
            print(f"Error getting owner data: {e}")
            return None
    
    @staticmethod
    async def validate_owner_data(owner_data: dict):
        """Validate owner data"""
        try:
            validator = OwnerValidator()
            result = validator.validate(owner_data)
            return result.is_valid, '; '.join(result.errors) if result.errors else ''
        except Exception as e:
            print(f"Error validating owner data: {e}")
            return False, str(e)
    
    @staticmethod
    async def validate_owner_data_for_edit(owner_data: dict):
        """Validate owner data for editing (less strict)"""
        try:
            # Convert owner_data to format expected by validator
            validator_data = {
                'firstname': owner_data.get('owner_firstname', ''),
                'surname': owner_data.get('owner_lastname', ''),
                'email': owner_data.get('owner_email', '')
            }
            
            validator = OwnerValidator()
            result = validator.validate(validator_data)
            return result.is_valid, '; '.join(result.errors) if result.errors else ''
        except Exception as e:
            print(f"Error validating owner data for edit: {e}")
            return False, str(e)
    
    @staticmethod
    async def update_owner(owner_id: int, owner_data: dict):
        """Update owner in database"""
        try:
            # Validate data
            is_valid, error_message = await OwnerService.validate_owner_data_for_edit(owner_data)
            if not is_valid:
                return False, f"Validation failed: {error_message}"
            
            # Update in database using dictionary method
            success = await AsyncOrm.update_owner_dict(owner_id, owner_data)
            if success:
                return True, "Owner updated successfully"
            else:
                return False, "Failed to update owner in database"
                
        except Exception as e:
            print(f"Error updating owner: {e}")
            return False, f"Error updating owner: {str(e)}"
    
    @staticmethod
    async def delete_owner(owner_id: int):
        """Delete owner from database"""
        try:
            success = await AsyncOrm.delete_owner(owner_id)
            if success:
                return True, "Owner deleted successfully"
            else:
                return False, "Failed to delete owner from database"
                
        except Exception as e:
            print(f"Error deleting owner: {e}")
            return False, f"Error deleting owner: {str(e)}"
