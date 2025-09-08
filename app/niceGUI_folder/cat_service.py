"""
Service layer for cat operations following SOLID principles.
Single Responsibility: Handles business logic for cat operations.
Dependency Inversion: Depends on abstractions (ORM interface).
"""

from typing import Optional, Dict, Any, List, Tuple
from app.database_folder.orm import AsyncOrm
from app.niceGUI_folder.validators import create_cat_edit_validator, ValidationResult


class CatService:
    """Service for cat business logic operations"""
    
    def __init__(self, orm: AsyncOrm):
        self.orm = orm
        self.validator = create_cat_edit_validator()
    
    async def get_cat_for_edit(self, cat_id: int) -> Optional[Dict[str, Any]]:
        """Get cat data for editing"""
        try:
            cat_info = await self.orm.get_cat_with_parents(cat_id)
            if not cat_info:
                return None
            
            return {
                'cat': cat_info['cat'],
                'owner': cat_info['owner'],
                'breed': cat_info['breed'],
                'dam': cat_info['dam'],
                'sire': cat_info['sire']
            }
        except Exception as e:
            print(f"Error getting cat for edit: {e}")
            return None
    
    async def get_available_parents(self) -> Tuple[List[Dict], List[Dict]]:
        """Get available mothers and fathers for selection"""
        try:
            # Get female cats for mothers
            _, female_cats = await self.orm.get_cat(cat_gender="Female")
            dam_options = [
                {'label': f"{cat['cat_firstname']} {cat['cat_surname']} ({cat['cat_birthday']})", 
                 'value': str(cat['cat_id'])}
                for cat in female_cats
            ]
            
            # Get male cats for fathers
            _, male_cats = await self.orm.get_cat(cat_gender="Male")
            sire_options = [
                {'label': f"{cat['cat_firstname']} {cat['cat_surname']} ({cat['cat_birthday']})", 
                 'value': str(cat['cat_id'])}
                for cat in male_cats
            ]
            
            return dam_options, sire_options
        except Exception as e:
            print(f"Error getting available parents: {e}")
            return [], []
    
    async def get_owners_and_breeders(self) -> Tuple[List[Dict], List[Dict]]:
        """Get available owners and breeders for selection"""
        try:
            # Get owners
            print("Getting owners...")
            _, owners = await self.orm.get_owner()
            owner_names = [f"{o['owner_firstname']} {o['owner_surname']}" for o in owners]
            print(f"Found {len(owners)} owners: {owner_names}")
            
            owner_options = [
                {'label': f"{owner['owner_firstname']} {owner['owner_surname']} ({owner['owner_email']})", 
                 'value': str(owner['owner_id'])}
                for owner in owners
            ]
            
            # Get breeders
            print("Getting breeders...")
            _, breeders = await self.orm.get_breed()
            breeder_names = [f"{b['breed_firstname']} {b['breed_surname']}" for b in breeders]
            print(f"Found {len(breeders)} breeders: {breeder_names}")
            
            breeder_options = [
                {'label': f"{breeder['breed_firstname']} {breeder['breed_surname']} ({breeder['breed_email']})", 
                 'value': str(breeder['breed_id'])}
                for breeder in breeders
            ]
            
            print(f"Owner options: {owner_options}")
            print(f"Breeder options: {breeder_options}")
            
            return owner_options, breeder_options
        except Exception as e:
            print(f"Error getting owners and breeders: {e}")
            import traceback
            traceback.print_exc()
            return [], []
    
    def validate_cat_data(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate cat data before saving"""
        return self.validator.validate(data)
    
    async def update_cat(self, cat_id: int, data: Dict[str, Any]) -> Tuple[bool, str]:
        """Update cat data"""
        try:
            # Validate data first
            validation_result = self.validate_cat_data(data)
            if not validation_result.is_valid:
                error_msg = "; ".join(validation_result.errors)
                return False, f"Validation failed: {error_msg}"
            
            # Update cat in database
            success = await self.orm.update_cat(
                cat_id=cat_id,
                firstname=data['firstname'],
                surname=data['surname'],
                gender=data['gender'],
                birthday=data['birthday'],
                microchip=data.get('microchip'),
                colour=data.get('colour'),
                litter=data.get('litter'),
                haritage_number=data.get('haritage_number'),
                owner_id=data.get('owner_id'),
                breed_id=data.get('breed_id'),
                dam_id=data.get('dam_id'),
                sire_id=data.get('sire_id')
            )
            
            if success:
                return True, "Cat updated successfully"
            else:
                return False, "Failed to update cat in database"
                
        except Exception as e:
            return False, f"Error updating cat: {str(e)}"
    
    async def delete_cat(self, cat_id: int) -> Tuple[bool, str]:
        """Delete cat"""
        try:
            success = await self.orm.delete_cat(cat_id)
            if success:
                return True, "Cat deleted successfully"
            else:
                return False, "Failed to delete cat"
        except Exception as e:
            return False, f"Error deleting cat: {str(e)}"
