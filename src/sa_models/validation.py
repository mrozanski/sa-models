"""
Validation utilities for guitar registry data structures.

This module provides helper functions for common validation tasks
and compatibility with existing JSON schema validation.
"""

from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, ValidationError

from .guitar_models import (
    GuitarSubmission,
    BatchSubmission,
    Manufacturer,
    Model,
    IndividualGuitar,
    SourceAttribution,
    Specifications,
)


def validate_guitar_submission(data: Dict[str, Any]) -> GuitarSubmission:
    """
    Validate guitar submission data and return a validated model.
    
    Args:
        data: Dictionary containing guitar submission data
        
    Returns:
        Validated GuitarSubmission model
        
    Raises:
        ValidationError: If data fails validation
    """
    try:
        return GuitarSubmission.model_validate(data)
    except ValidationError as e:
        # Provide more helpful error messages
        raise ValidationError(
            model=GuitarSubmission,
            errors=e.errors(),
            title="Guitar submission validation failed"
        )


def validate_batch_submission(data: List[Dict[str, Any]]) -> BatchSubmission:
    """
    Validate batch submission data and return a validated model.
    
    Args:
        data: List of dictionaries containing guitar submission data
        
    Returns:
        Validated BatchSubmission model
        
    Raises:
        ValidationError: If data fails validation
    """
    try:
        return BatchSubmission(submissions=data)
    except ValidationError as e:
        raise ValidationError(
            model=BatchSubmission,
            errors=e.errors(),
            title="Batch submission validation failed"
        )


def validate_individual_components(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate individual components of a guitar submission separately.
    
    This is useful for partial validation or when you want to validate
    components before assembling the full submission.
    
    Args:
        data: Dictionary containing guitar data components
        
    Returns:
        Dictionary with validated components
        
    Raises:
        ValidationError: If any component fails validation
    """
    validated = {}
    errors = []
    
    # Validate manufacturer if present
    if 'manufacturer' in data:
        try:
            validated['manufacturer'] = Manufacturer.model_validate(data['manufacturer'])
        except ValidationError as e:
            errors.extend([f"Manufacturer validation failed: {err}" for err in e.errors()])
    
    # Validate model if present
    if 'model' in data:
        try:
            validated['model'] = Model.model_validate(data['model'])
        except ValidationError as e:
            errors.extend([f"Model validation failed: {err}" for err in e.errors()])
    
    # Validate individual guitar if present
    if 'individual_guitar' in data:
        try:
            validated['individual_guitar'] = IndividualGuitar.model_validate(data['individual_guitar'])
        except ValidationError as e:
            errors.extend([f"Individual guitar validation failed: {err}" for err in e.errors()])
    
    # Validate source attribution if present
    if 'source_attribution' in data:
        try:
            validated['source_attribution'] = SourceAttribution.model_validate(data['source_attribution'])
        except ValidationError as e:
            errors.extend([f"Source attribution validation failed: {err}" for err in e.errors()])
    
    # Validate specifications if present
    if 'specifications' in data:
        try:
            validated['specifications'] = Specifications.model_validate(data['specifications'])
        except ValidationError as e:
            errors.extend([f"Specifications validation failed: {err}" for err in e.errors()])
    

    
    if errors:
        raise ValidationError(
            model=BaseModel,
            errors=[{"type": "validation_error", "msg": error} for error in errors],
            title="Component validation failed"
        )
    
    return validated


def convert_to_json_schema() -> Dict[str, Any]:
    """
    Generate JSON schema from Pydantic models for compatibility with existing systems.
    
    Returns:
        Dictionary containing JSON schema definitions
    """
    return {
        "manufacturer": Manufacturer.model_json_schema(),
        "model": Model.model_json_schema(),
        "individual_guitar": IndividualGuitar.model_json_schema(),
        "source_attribution": SourceAttribution.model_json_schema(),
        "specifications": Specifications.model_json_schema(),
        "guitar_submission": GuitarSubmission.model_json_schema(),
        "batch_submission": BatchSubmission.model_json_schema(),
    }


def validate_serial_number_format(serial_number: str) -> bool:
    """
    Validate serial number format for common guitar manufacturers.
    
    Args:
        serial_number: Serial number string to validate
        
    Returns:
        True if format is valid, False otherwise
    """
    if not serial_number:
        return False
    
    # Remove common separators
    cleaned = serial_number.replace('-', '').replace(' ', '').replace('.', '')
    
    # Must contain only alphanumeric characters
    if not cleaned.isalnum():
        return False
    
    # Must be reasonable length (3-20 characters)
    if len(cleaned) < 3 or len(cleaned) > 20:
        return False
    
    return True


def validate_year_range(year: int, min_year: int = 1900, max_year: int = 2030) -> bool:
    """
    Validate year is within reasonable range for guitar manufacturing.
    
    Args:
        year: Year to validate
        min_year: Minimum valid year
        max_year: Maximum valid year
        
    Returns:
        True if year is valid, False otherwise
    """
    return min_year <= year <= max_year


def validate_currency_code(currency: str) -> bool:
    """
    Validate ISO currency code format.
    
    Args:
        currency: Currency code string to validate
        
    Returns:
        True if format is valid, False otherwise
    """
    if not currency:
        return False
    
    # Must be exactly 3 characters
    if len(currency) != 3:
        return False
    
    # Must be uppercase letters
    if not currency.isalpha() or not currency.isupper():
        return False
    
    return True


def get_validation_summary(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get a summary of validation results for debugging and reporting.
    
    Args:
        data: Dictionary containing guitar data
        
    Returns:
        Dictionary with validation summary
    """
    summary = {
        "has_manufacturer": "manufacturer" in data,
        "has_model": "model" in data,
        "has_individual_guitar": "individual_guitar" in data,
        "has_source_attribution": "source_attribution" in data,
        "has_specifications": "specifications" in data,
        "validation_errors": [],
        "is_valid": True
    }
    
    try:
        validate_guitar_submission(data)
    except ValidationError as e:
        summary["validation_errors"] = [str(error) for error in e.errors()]
        summary["is_valid"] = False
    
    return summary
