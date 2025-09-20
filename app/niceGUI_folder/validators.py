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
        required_fields = ['firstname', 'gender', 'birthday']
        for field in required_fields:
            if not data.get(field):
                errors.append(f"{field.capitalize()} is required")

        if data.get('gender') and data['gender'] not in ['Male', 'Female']:
            errors.append("Gender must be 'Male' or 'Female'")

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

        # Validate eye color
        eye_colour = data.get('eye_colour')
        if eye_colour and eye_colour not in ['', 'Blue', 'Green', 'Yellow', 'Orange', 'Heterochromatic']:
            errors.append("Invalid eye color")

        # Validate hair type
        hair_type = data.get('hair_type')
        if hair_type and hair_type not in ['', 'Short Hair', 'Long Hair', 'Semi-Long Hair']:
            errors.append("Invalid hair type")

        # Validate litter sizes
        litter_size_male = data.get('litter_size_male')
        if litter_size_male is not None and (not isinstance(litter_size_male, int) or litter_size_male < 0 or litter_size_male > 20):
            errors.append("Litter size (male) must be between 0 and 20")

        litter_size_female = data.get('litter_size_female')
        if litter_size_female is not None and (not isinstance(litter_size_female, int) or litter_size_female < 0 or litter_size_female > 20):
            errors.append("Litter size (female) must be between 0 and 20")

        # Validate weights
        weight = data.get('weight')
        if weight is not None and (not isinstance(weight, (int, float)) or weight < 0 or weight > 50):
            errors.append("Weight must be between 0 and 50 kg")

        birth_weight = data.get('birth_weight')
        if birth_weight is not None and (not isinstance(birth_weight, (int, float)) or birth_weight < 0 or birth_weight > 200):
            errors.append("Birth weight must be between 0 and 200 g")

        transfer_weight = data.get('transfer_weight')
        if transfer_weight is not None and (not isinstance(transfer_weight, (int, float)) or transfer_weight < 0 or transfer_weight > 200):
            errors.append("Transfer weight must be between 0 and 200 g")

        # Validate jaw fault
        jaw_fault = data.get('jaw_fault')
        if jaw_fault and jaw_fault not in ['', 'None', 'Overbite', 'Underbite', 'Crossbite']:
            errors.append("Invalid jaw fault")

        # Validate hernia
        hernia = data.get('hernia')
        if hernia and hernia not in ['', 'None', 'Umbilical', 'Inguinal', 'Diaphragmatic']:
            errors.append("Invalid hernia type")

        # Validate testicles
        testicles = data.get('testicles')
        if testicles and testicles not in ['', 'Normal', 'Cryptorchid', 'Monorchid']:
            errors.append("Invalid testicles condition")

        # Validate status
        status = data.get('status')
        if status and status not in ['', 'Alive', 'Deceased', 'Missing', 'Transferred']:
            errors.append("Invalid status")

        # Validate dates
        breeding_lock_date = data.get('breeding_lock_date')
        if breeding_lock_date and isinstance(breeding_lock_date, (date, datetime)):
            if breeding_lock_date > date.today():
                errors.append("Breeding lock date cannot be in the future")

        death_date = data.get('death_date')
        if death_date and isinstance(death_date, (date, datetime)):
            if death_date > date.today():
                errors.append("Death date cannot be in the future")

        dam_id = data.get('dam_id')
        sire_id = data.get('sire_id')

        if dam_id and sire_id and dam_id == sire_id:
            errors.append("Mother and father cannot be the same cat")

        if dam_id and data.get('dam_gender') and data['dam_gender'] != 'Female':
            errors.append("Mother must be a female cat")

        if sire_id and data.get('sire_gender') and data['sire_gender'] != 'Male':
            errors.append("Father must be a male cat")


class OwnerValidator(BaseValidator):
    """Validator for owner data"""

    def _validate_data(self, data: Dict[str, Any], errors: List[str]) -> None:
        """Validate owner-specific data"""
        required_fields = ['firstname', 'surname', 'email']
        for field in required_fields:
            if not data.get(field):
                errors.append(f"Owner {field.capitalize()} is required")

        email = data.get('email')
        if email and '@' not in email:
            errors.append("Invalid email format")


class BreederValidator(BaseValidator):
    """Validator for breeder data"""

    def _validate_data(self, data: Dict[str, Any], errors: List[str]) -> None:
        """Validate breeder-specific data"""
        required_fields = ['firstname', 'surname', 'email']
        for field in required_fields:
            if not data.get(field):
                errors.append(f"Breeder {field.capitalize()} is required")

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
