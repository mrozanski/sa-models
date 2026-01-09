"""
Tests for guitar registry Pydantic models.
"""

import pytest
from decimal import Decimal
from datetime import date
from pydantic import ValidationError

from sa_models import (
    Manufacturer,
    Model,
    IndividualGuitar,
    SourceAttribution,
    GuitarSubmission,
    BatchSubmission,
    ModelReference,
    Specifications,
    Finish,
)


class TestManufacturer:
    """Test Manufacturer model validation."""
    
    def test_valid_manufacturer(self):
        """Test valid manufacturer data."""
        data = {
            "name": "Gibson Guitar Corporation",
            "country": "USA",
            "founded_year": 1902,
            "status": "active"
        }
        manufacturer = Manufacturer.model_validate(data)
        assert manufacturer.name == "Gibson Guitar Corporation"
        assert manufacturer.country == "USA"
        assert manufacturer.founded_year == 1902
        assert manufacturer.status == "active"
    
    def test_manufacturer_required_fields(self):
        """Test that name is required."""
        with pytest.raises(ValidationError):
            Manufacturer.model_validate({})
    
    def test_manufacturer_invalid_year(self):
        """Test invalid founded year."""
        with pytest.raises(ValidationError):
            Manufacturer.model_validate({
                "name": "Test",
                "founded_year": 1700  # Too early
            })


class TestModel:
    """Test Model model validation."""
    
    def test_valid_model(self):
        """Test valid model data."""
        data = {
            "manufacturer_name": "Gibson Guitar Corporation",
            "name": "Les Paul Standard",
            "year": 1959,
            "production_type": "mass"
        }
        model = Model.model_validate(data)
        assert model.manufacturer_name == "Gibson Guitar Corporation"
        assert model.name == "Les Paul Standard"
        assert model.year == 1959
        assert model.production_type == "mass"
        assert model.currency == "USD"  # Default value
    
    def test_model_required_fields(self):
        """Test required fields."""
        with pytest.raises(ValidationError):
            Model.model_validate({
                "name": "Test",
                # Missing manufacturer_name and year
            })


class TestIndividualGuitar:
    """Test IndividualGuitar model validation."""
    
    def test_valid_with_model_reference(self):
        """Test valid individual guitar with model reference."""
        data = {
            "model_reference": {
                "manufacturer_name": "Gibson Guitar Corporation",
                "model_name": "Les Paul Standard",
                "year": 1959
            },
            "serial_number": "9-0824",
            "significance_level": "historic"
        }
        guitar = IndividualGuitar.model_validate(data)
        assert guitar.model_reference is not None
        assert guitar.serial_number == "9-0824"
        assert guitar.significance_level == "historic"
    
    def test_valid_with_fallback(self):
        """Test valid individual guitar with fallback fields."""
        data = {
            "manufacturer_name_fallback": "Unknown Manufacturer",
            "model_name_fallback": "Unknown Model",
            "serial_number": "12345",
            "significance_level": "notable"
        }
        guitar = IndividualGuitar.model_validate(data)
        assert guitar.manufacturer_name_fallback == "Unknown Manufacturer"
        assert guitar.model_name_fallback == "Unknown Model"
    
    def test_invalid_no_identification(self):
        """Test that some identification method is required."""
        with pytest.raises(ValidationError):
            IndividualGuitar.model_validate({
                "serial_number": "12345"
                # Missing both model_reference and fallback fields
            })
    
    def test_invalid_both_methods(self):
        """Test that both identification methods cannot be used."""
        with pytest.raises(ValidationError):
            IndividualGuitar.model_validate({
                "model_reference": {
                    "manufacturer_name": "Gibson",
                    "model_name": "Les Paul",
                    "year": 1959
                },
                "manufacturer_name_fallback": "Gibson",
                "model_name_fallback": "Les Paul"
            })


class TestGuitarSubmission:
    """Test GuitarSubmission model validation."""
    
    def test_valid_with_manufacturer_model(self):
        """Test valid submission with manufacturer and model."""
        data = {
            "manufacturer": {
                "name": "Gibson Guitar Corporation",
                "country": "USA"
            },
            "model": {
                "manufacturer_name": "Gibson Guitar Corporation",
                "name": "Les Paul Standard",
                "year": 1959
            },
            "individual_guitar": {
                "model_reference": {
                    "manufacturer_name": "Gibson Guitar Corporation",
                    "model_name": "Les Paul Standard",
                    "year": 1959
                },
                "serial_number": "9-0824"
            },
            "source_attribution": {
                "source_name": "Guitar Registry Test"
            }
        }
        submission = GuitarSubmission.model_validate(data)
        assert submission.manufacturer is not None
        assert submission.model is not None
        assert submission.individual_guitar is not None
        assert submission.source_attribution is not None
    
    def test_valid_with_model_reference_only(self):
        """Test valid submission with only model reference."""
        data = {
            "individual_guitar": {
                "model_reference": {
                    "manufacturer_name": "Gibson Guitar Corporation",
                    "model_name": "Les Paul Standard",
                    "year": 1959
                },
                "serial_number": "9-0824"
            },
            "source_attribution": {
                "source_name": "Guitar Registry Test"
            }
        }
        submission = GuitarSubmission.model_validate(data)
        assert submission.manufacturer is None
        assert submission.model is None
        assert submission.individual_guitar.model_reference is not None
    
    def test_invalid_missing_required(self):
        """Test that required fields are enforced."""
        with pytest.raises(ValidationError):
            GuitarSubmission.model_validate({
                "individual_guitar": {
                    "serial_number": "9-0824"
                }
                # Missing source_attribution
            })


class TestBatchSubmission:
    """Test BatchSubmission model validation."""
    
    def test_valid_batch(self):
        """Test valid batch submission."""
        data = [
            {
                "individual_guitar": {
                    "model_reference": {
                        "manufacturer_name": "Gibson",
                        "model_name": "Les Paul",
                        "year": 1959
                    },
                    "serial_number": "001"
                },
                "source_attribution": {
                    "source_name": "Test Source 1"
                }
            },
            {
                "individual_guitar": {
                    "model_reference": {
                        "manufacturer_name": "Fender",
                        "model_name": "Stratocaster",
                        "year": 1954
                    },
                    "serial_number": "002"
                },
                "source_attribution": {
                    "source_name": "Test Source 2"
                }
            }
        ]
        batch = BatchSubmission.model_validate({"submissions": data})
        assert len(batch.submissions) == 2
        assert batch.submissions[0].individual_guitar.serial_number == "001"
        assert batch.submissions[1].individual_guitar.serial_number == "002"
    
    def test_empty_batch(self):
        """Test that empty batch is rejected."""
        with pytest.raises(ValidationError):
            BatchSubmission.model_validate({"submissions": []})


class TestSpecifications:
    """Test Specifications model validation."""
    
    def test_valid_specifications(self):
        """Test valid specifications."""
        data = {
            "body_wood": "Mahogany",
            "neck_wood": "Maple",
            "scale_length_inches": 24.75,
            "num_frets": 22,
            "pickup_configuration": "HH"
        }
        specs = Specifications.model_validate(data)
        assert specs.body_wood == "Mahogany"
        assert specs.neck_wood == "Maple"
        assert specs.scale_length_inches == 24.75
        assert specs.num_frets == 22
        assert specs.pickup_configuration == "HH"
    
    def test_specifications_optional_fields(self):
        """Test that all fields are optional."""
        specs = Specifications.model_validate({})
        assert specs.body_wood is None
        assert specs.neck_wood is None


class TestFinish:
    """Test Finish model validation."""
    
    def test_valid_finish(self):
        """Test valid finish."""
        data = {
            "finish_name": "Cherry Sunburst",
            "finish_type": "Nitrocellulose",
            "rarity": "common"
        }
        finish = Finish.model_validate(data)
        assert finish.finish_name == "Cherry Sunburst"
        assert finish.finish_type == "Nitrocellulose"
        assert finish.rarity == "common"
        assert finish.notes is None  # Optional field


if __name__ == "__main__":
    pytest.main([__file__])
