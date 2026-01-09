# Eddie Shared Models

Shared Pydantic models for guitar registry data structures, used by both the Eddie project (data generation) and the Guitar Registry project (data ingestion).

## Overview

This package provides a single source of truth for guitar data structures, ensuring consistency between data generation and validation systems. It replaces the JSON schema validation in the guitar registry with type-safe Pydantic models.

## Installation

### For Development
```bash
git clone https://github.com/mrozanski/sa-models.git
cd sa-models
pip install -e .
```

### For Production
```bash
pip install sa-models
```

## Usage

### Basic Import
```python
from sa_models import GuitarSubmission, Manufacturer, Model, IndividualGuitar
```

### Data Validation
```python
# Validate incoming data
try:
    submission = GuitarSubmission.model_validate(data)
    print(f"Valid submission for {submission.manufacturer.name}")
except ValidationError as e:
    print(f"Validation failed: {e}")
```

### Data Generation (Eddie Project)
```python
# Create structured data
submission = GuitarSubmission(
    manufacturer=Manufacturer(
        name="Gibson Guitar Corporation",
        country="USA",
        founded_year=1902
    ),
    model=Model(
        manufacturer_name="Gibson Guitar Corporation",
        name="Les Paul Standard",
        year=1959
    ),
    individual_guitar=IndividualGuitar(
        serial_number="9-0824",
        significance_level="historic"
    ),
    source_attribution=SourceAttribution(
        source_name="Guitar Registry Test"
    )
)

# Export to JSON
json_data = submission.model_dump_json(indent=2)
```

### Data Processing (Guitar Registry Project)
```python
# Process validated data
submission = GuitarSubmission.model_validate(data)
manufacturer_id = process_manufacturer(submission.manufacturer)
model_id = process_model(submission.model, manufacturer_id)
guitar_id = process_individual_guitar(submission.individual_guitar, model_id)
```

## Model Structure

### Core Models
- `Manufacturer`: Company information
- `Model`: Guitar model specifications  
- `IndividualGuitar`: Specific guitar instances
- `SourceAttribution`: Data source information
- `Specifications`: Technical details
- `Finish`: Color and finish information

### Composite Models
- `GuitarSubmission`: Complete submission with all required entities
- `BatchSubmission`: Multiple guitar submissions

## Migration from JSON Schema

This package replaces the JSON schema validation in `uniqueness_management_system.py`:

**Before (JSON Schema):**
```python
MANUFACTURER_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "minLength": 1, "maxLength": 100},
        # ... more properties
    }
}
```

**After (Pydantic):**
```python
from sa_models import Manufacturer

# Automatic validation with type hints
manufacturer = Manufacturer(name="Gibson", country="USA")
```

## Benefits

1. **Type Safety**: Runtime validation with clear error messages
2. **IDE Support**: Autocomplete, type checking, and refactoring
3. **Documentation**: Self-documenting models with field descriptions
4. **Consistency**: Identical data structures across projects
5. **Maintenance**: Single source of truth for all data models
6. **Testing**: Easy to test data generation and validation

## Development

### Adding New Fields
1. Update the Pydantic model in `guitar_models.py`
2. Add validation rules and field descriptions
3. Update tests
4. Release new version
5. Update both projects to use new version

### Testing
```bash
pytest tests/
pytest tests/ --cov=sa_models
```

### Building
```bash
python -m build
```

## License

GNU Affero General Public License v3 - see LICENSE file for details.
