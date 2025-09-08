"""
Validators for cat data validation following SOLID principles.
Single Responsibility: Each validator handles one specific validation concern.
"""

from datetime import date, datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Result of validation operation"""
    is_valid: bool
    errors: List[str]
    data: Optional[Dict[str, Any]] = None


class BaseValidator:
    """Base validator class following Open/Closed principle"""
    
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate data and return result"""
        errors = []
        
        # Override in subclasses
        self._validate_data(data, errors)
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            data=data if len(errors) == 0 else None
        )
    
    def _validate_data(self, data: Dict[str, Any], errors: List[str]) -> None:
        """Override in subclasses to implement specific validation"""
        pass


class CatValidator(BaseValidator):
    """Validator for cat data"""
    
    def _validate_data(self, data: Dict[str, Any], errors: List[str]) -> None:
        """Validate cat-specific data"""
        # Required fields
        required_fields = ['firstname', 'surname', 'gender', 'birthday']
        for field in required_fields:
            if not data.get(field):
                errors.append(f"{field.capitalize()} is required")
        
        # Validate gender
        if data.get('gender') and data['gender'] not in ['Male', 'Female']:
            errors.append("Gender must be 'Male' or 'Female'")
        
        # Validate birthday
        birthday = data.get('birthday')
        if birthday:
            if isinstance(birthday, str):
                try:
                    birthday = datetime.strptime(birthday, '%Y-%m-%d').date()
                except ValueError:
                    errors.append("Invalid birthday format. Use YYYY-MM-DD")
            elif isinstance(birthday, (date, datetime)):
                if birthday > date.today():
                    errors.append("Birthday cannot be in the future")
            else:
                errors.append("Invalid birthday format")
        
        # Validate microchip (if provided and not empty)
        microchip = data.get('microchip')
        if microchip and microchip.strip() and len(microchip.strip()) < 5:
            errors.append("Microchip number must be at least 5 characters")
        
        # Validate parent IDs (if provided)
        dam_id = data.get('dam_id')
        sire_id = data.get('sire_id')
        
        if dam_id and sire_id and dam_id == sire_id:
            errors.append("Mother and father cannot be the same cat")
        
        # Validate parent genders
        if dam_id and data.get('dam_gender') and data['dam_gender'] != 'Female':
            errors.append("Mother must be a female cat")
        
        if sire_id and data.get('sire_gender') and data['sire_gender'] != 'Male':
            errors.append("Father must be a male cat")


class OwnerValidator(BaseValidator):
    """Validator for owner data"""
    
    def _validate_data(self, data: Dict[str, Any], errors: List[str]) -> None:
        """Validate owner-specific data"""
        # Required fields
        required_fields = ['firstname', 'surname', 'email']
        for field in required_fields:
            if not data.get(field):
                errors.append(f"Owner {field.capitalize()} is required")
        
        # Validate email format
        email = data.get('email')
        if email and '@' not in email:
            errors.append("Invalid email format")


class BreederValidator(BaseValidator):
    """Validator for breeder data"""
    
    def _validate_data(self, data: Dict[str, Any], errors: List[str]) -> None:
        """Validate breeder-specific data"""
        # Required fields
        required_fields = ['firstname', 'surname', 'email']
        for field in required_fields:
            if not data.get(field):
                errors.append(f"Breeder {field.capitalize()} is required")
        
        # Validate email format
        email = data.get('email')
        if email and '@' not in email:
            errors.append("Invalid breeder email format")


class CompositeValidator:
    """Composite validator following Composite pattern"""
    
    def __init__(self):
        self.validators = []
    
    def add_validator(self, validator: BaseValidator) -> None:
        """Add a validator to the composite"""
        self.validators.append(validator)
    
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate data using all validators"""
        all_errors = []
        
        for validator in self.validators:
            result = validator.validate(data)
            if not result.is_valid:
                all_errors.extend(result.errors)
        
        return ValidationResult(
            is_valid=len(all_errors) == 0,
            errors=all_errors,
            data=data if len(all_errors) == 0 else None
        )


def create_cat_edit_validator() -> CompositeValidator:
    """Factory function to create validator for cat editing"""
    validator = CompositeValidator()
    validator.add_validator(CatValidator())
    validator.add_validator(OwnerValidator())
    validator.add_validator(BreederValidator())
    return validator
