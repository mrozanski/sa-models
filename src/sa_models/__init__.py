"""
Guitar registry shared models - Guitar Registry Data Structures

This package provides shared Pydantic models for guitar data structures,
ensuring consistency between data generation and validation systems.
"""

from .guitar_models import (
    # Core models
    Manufacturer,
    Model,
    IndividualGuitar,
    SourceAttribution,
    Specifications,
    
    # Composite models
    GuitarSubmission,
    BatchSubmission,
    
    # Enums
    ManufacturerStatus,
    ProductionType,
    SignificanceLevel,
    ConditionRating,
    SourceType,
)

from .validation import (
    # Validation functions
    validate_guitar_submission,
    validate_batch_submission,
    validate_individual_components,
    validate_serial_number_format,
    validate_year_range,
    validate_currency_code,
    get_validation_summary,
    convert_to_json_schema,
)

__version__ = "0.1.0"
__all__ = [
    # Core models
    "Manufacturer",
    "Model", 
    "IndividualGuitar",
    "SourceAttribution",
    "Specifications",
    
    # Composite models
    "GuitarSubmission",
    "BatchSubmission",
    
    # Enums
    "ManufacturerStatus",
    "ProductionType",
    "SignificanceLevel",
    "ConditionRating",
    "SourceType",
    
    # Validation functions
    "validate_guitar_submission",
    "validate_batch_submission",
    "validate_individual_components",
    "validate_serial_number_format",
    "validate_year_range",
    "validate_currency_code",
    "get_validation_summary",
    "convert_to_json_schema",
]
