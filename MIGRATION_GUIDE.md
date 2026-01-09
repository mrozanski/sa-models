# Migration Guide: From JSON Schema to Pydantic Models

This guide helps you migrate your guitar registry project from JSON schema validation to the shared Pydantic models.

## Overview

The migration involves:
1. Installing the shared models package
2. Replacing JSON schema validation with Pydantic models
3. Updating validation logic in `uniqueness_management_system.py`
4. Updating the CLI processor

## Step 1: Install Shared Models

### Option A: Install from PyPI (when published)
```bash
pip install sa-models
```

### Option B: Install from local development
```bash
# Clone the shared models repository
git clone https://github.com/mrozanski/sa-models.git
cd sa-models
pip install -e .
```

## Step 2: Update Dependencies

Add to your `requirements.txt` or `pyproject.toml`:
```
sa-models>=0.1.0
```

## Step 3: Replace JSON Schema Validation

### Before (in `uniqueness_management_system.py`):
```python
import jsonschema

MANUFACTURER_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "minLength": 1, "maxLength": 100},
        "country": {"type": ["string", "null"], "maxLength": 50},
        # ... more properties
    },
    "required": ["name"],
    "additionalProperties": False
}

def validate_manufacturer(self, data: Dict) -> ValidationResult:
    try:
        jsonschema.validate(data, MANUFACTURER_SCHEMA)
    except jsonschema.ValidationError as e:
        return ValidationResult(False, "invalid_schema", conflicts=[str(e)])
    # ... rest of validation logic
```

### After (using shared models):
```python
from sa_models import Manufacturer, ValidationError

def validate_manufacturer(self, data: Dict) -> ValidationResult:
    try:
        # Validate with Pydantic
        manufacturer = Manufacturer.model_validate(data)
        
        # Continue with existing business logic validation
        return self._validate_manufacturer_business_rules(manufacturer)
        
    except ValidationError as e:
        # Convert Pydantic errors to your format
        conflicts = [f"{err['loc']}: {err['msg']}" for err in e.errors()]
        return ValidationResult(False, "invalid_schema", conflicts=conflicts)
```

## Step 4: Update All Validation Methods

Replace all JSON schema validation calls:

```python
# Old way
jsonschema.validate(data, MODEL_SCHEMA)
jsonschema.validate(data, INDIVIDUAL_GUITAR_SCHEMA)
jsonschema.validate(data, SPECIFICATIONS_SCHEMA)

# New way
from sa_models import Model, IndividualGuitar, Specifications

Model.model_validate(data)
IndividualGuitar.model_validate(data)
Specifications.model_validate(data)
```

## Step 5: Update CLI Processor

### In `guitar_processor_cli.py`:

```python
from sa_models import GuitarSubmission, BatchSubmission, ValidationError

def load_json_file(self, file_path: str):
    """Load and validate JSON file using Pydantic models."""
    try:
        # ... existing file loading code ...
        
        # Validate with Pydantic instead of basic JSON parsing
        if isinstance(data, list):
            # Batch submission
            validated_data = BatchSubmission(submissions=data)
            if self.verbose:
                print(f"✓ Validated batch submission with {len(validated_data.submissions)} items")
        else:
            # Single submission
            validated_data = GuitarSubmission.model_validate(data)
            if self.verbose:
                print(f"✓ Validated single submission")
        
        return validated_data.model_dump()  # Convert back to dict for compatibility
        
    except ValidationError as e:
        print(f"✗ Data validation failed:")
        for error in e.errors():
            field_path = " -> ".join(str(loc) for loc in error["loc"])
            print(f"  • {field_path}: {error['msg']}")
        return None
    except Exception as e:
        print(f"✗ Error reading file {file_path}: {e}")
        return None
```

## Step 6: Update Business Logic Validation

### Before:
```python
def _validate_manufacturer_business_rules(self, data: Dict) -> ValidationResult:
    # Business logic validation
    name = data.get('name', '').strip()
    if len(name) < 2:
        return ValidationResult(False, "invalid_name", conflicts=["Name too short"])
    # ... more validation
```

### After:
```python
def _validate_manufacturer_business_rules(self, manufacturer: Manufacturer) -> ValidationResult:
    # Business logic validation using validated Pydantic model
    name = manufacturer.name.strip()
    if len(name) < 2:
        return ValidationResult(False, "invalid_name", conflicts=["Name too short"])
    # ... more validation
```

## Step 7: Update Error Handling

### Before:
```python
except jsonschema.ValidationError as e:
    conflicts = [str(e)]
```

### After:
```python
except ValidationError as e:
    conflicts = [f"{' -> '.join(str(loc) for loc in error['loc'])}: {error['msg']}" 
                 for error in e.errors()]
```

## Step 8: Test the Migration

1. **Run existing tests** to ensure nothing breaks
2. **Test with sample data** to verify validation works
3. **Check error messages** are still helpful
4. **Verify business logic** still functions correctly

## Step 9: Clean Up

Remove unused imports and JSON schema constants:
```python
# Remove these imports
import jsonschema

# Remove these constants
MANUFACTURER_SCHEMA = {...}
MODEL_SCHEMA = {...}
INDIVIDUAL_GUITAR_SCHEMA = {...}
# ... etc
```

## Benefits After Migration

1. **Type Safety**: Runtime validation with clear error messages
2. **IDE Support**: Autocomplete, type checking, and refactoring
3. **Consistency**: Identical data structures across projects
4. **Maintenance**: Single source of truth for all data models
5. **Documentation**: Self-documenting models with field descriptions

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure the shared models package is installed
2. **Validation Errors**: Check that your data matches the new model structure
3. **Type Errors**: Use `.model_dump()` to convert Pydantic models back to dictionaries
4. **Business Logic**: Ensure your business validation methods accept Pydantic models

### Rollback Plan

If issues arise, you can temporarily revert to JSON schema validation:
```python
# Temporary fallback
try:
    # Try Pydantic validation
    manufacturer = Manufacturer.model_validate(data)
except ImportError:
    # Fall back to JSON schema
    jsonschema.validate(data, MANUFACTURER_SCHEMA)
```

## Next Steps

After successful migration:
1. **Update documentation** to reflect new validation approach
2. **Add tests** for the new Pydantic validation
3. **Consider adding** more sophisticated validation rules
4. **Share models** with the Eddie project for consistency
