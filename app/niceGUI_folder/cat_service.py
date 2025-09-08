"""
Service layer for cat operations following SOLID principles.
Single Responsibility: Handles business logic for cat operations.
Dependency Inversion: Depends on abstractions (ORM interface).
"""

from typing import Optional, Dict, Any, List, Tuple
from datetime import date
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
    
    async def get_available_parents(self, exclude_cat_id: int = None) -> Tuple[List[Dict], List[Dict]]:
        """Get available mothers and fathers for selection"""
        try:
            # Get female cats for mothers
            _, female_cats = await self.orm.get_cat(cat_gender="Female")
            print(f"Found {len(female_cats)} female cats")
            
            # Filter out the current cat if specified
            if exclude_cat_id:
                female_cats = [cat for cat in female_cats if cat['cat_id'] != exclude_cat_id]
                print(f"After filtering, {len(female_cats)} female cats available")
            
            dam_options = [
                {'label': f"{cat['cat_firstname']} {cat['cat_surname']} ({cat.get('cat_birthday', 'N/A')})", 
                 'value': str(cat['cat_id'])}
                for cat in female_cats
            ]
            
            # Get male cats for fathers
            _, male_cats = await self.orm.get_cat(cat_gender="Male")
            print(f"Found {len(male_cats)} male cats")
            
            # Filter out the current cat if specified
            if exclude_cat_id:
                male_cats = [cat for cat in male_cats if cat['cat_id'] != exclude_cat_id]
                print(f"After filtering, {len(male_cats)} male cats available")
            
            sire_options = [
                {'label': f"{cat['cat_firstname']} {cat['cat_surname']} ({cat.get('cat_birthday', 'N/A')})", 
                 'value': str(cat['cat_id'])}
                for cat in male_cats
            ]
            
            print(f"Dam options: {dam_options}")
            print(f"Sire options: {sire_options}")
            
            return dam_options, sire_options
        except Exception as e:
            print(f"Error getting available parents: {e}")
            import traceback
            traceback.print_exc()
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
    
    def validate_cat_data_for_edit(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate cat data for editing (without owner/breeder validation)"""
        errors = []
        
        # Required fields
        required_fields = ['firstname', 'surname', 'gender', 'birthday']
        for field in required_fields:
            if not data.get(field):
                errors.append(f"{field.capitalize()} is required")
        
        # Validate birthday format
        birthday = data.get('birthday')
        if birthday:
            try:
                if isinstance(birthday, str):
                    from datetime import datetime
                    birthday = datetime.strptime(birthday, '%Y-%m-%d').date()
                if birthday > date.today():
                    errors.append("Birthday cannot be in the future")
            except ValueError:
                errors.append("Invalid birthday format")
        
        # Validate microchip (if provided and not empty)
        microchip = data.get('microchip')
        if microchip and microchip.strip() and len(microchip.strip()) < 5:
            errors.append("Microchip number must be at least 5 characters")
        elif microchip and not microchip.strip():
            # If microchip is empty string, set it to None
            data['microchip'] = None
        
        # Validate parent IDs (if provided)
        dam_id = data.get('dam_id')
        sire_id = data.get('sire_id')
        
        if dam_id and sire_id and dam_id == sire_id:
            errors.append("Mother and father cannot be the same cat")
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            data=data if len(errors) == 0 else None
        )
    
    async def update_cat(self, cat_id: int, data: Dict[str, Any]) -> Tuple[bool, str]:
        """Update cat data"""
        try:
            # Validate data first (using edit-specific validator)
            validation_result = self.validate_cat_data_for_edit(data)
            if not validation_result.is_valid:
                error_msg = "; ".join(validation_result.errors)
                return False, f"Validation failed: {error_msg}"
            
            # Convert birthday string to date object
            from datetime import datetime
            try:
                birthday_date = datetime.strptime(data['birthday'], '%Y-%m-%d').date()
            except ValueError:
                return False, "Invalid birthday format. Use YYYY-MM-DD"
            
            # Update cat in database
            print(f"Updating cat {cat_id} with data: {data}")
            success = await self.orm.update_cat(
                cat_id=cat_id,
                firstname=data['firstname'],
                surname=data['surname'],
                gender=data['gender'],
                birthday=birthday_date,
                microchip=data.get('microchip'),
                colour=data.get('colour'),
                litter=data.get('litter'),
                haritage_number=data.get('haritage_number'),
                owner_id=data.get('owner_id'),
                breed_id=data.get('breed_id'),
                dam_id=data.get('dam_id'),
                sire_id=data.get('sire_id'),
                cat_photos=data.get('cat_photos')
            )
            print(f"Update result: {success}")
            
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
