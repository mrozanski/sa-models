"""
Core Pydantic models for guitar registry data structures.

These models provide type-safe validation and serialization for guitar data,
replacing the JSON schema validation in the guitar registry system.
"""

from datetime import date
from decimal import Decimal
from enum import Enum
from typing import List, Optional, Union
from pydantic import BaseModel, Field, field_validator, model_validator, HttpUrl


# Enums
class ManufacturerStatus(str, Enum):
    """Manufacturer operational status."""
    ACTIVE = "active"
    DEFUNCT = "defunct"
    ACQUIRED = "acquired"


class ProductionType(str, Enum):
    """Guitar production type."""
    MASS = "mass"
    LIMITED = "limited"
    CUSTOM = "custom"
    PROTOTYPE = "prototype"
    ONE_OFF = "one-off"


class SignificanceLevel(str, Enum):
    """Historical significance of a guitar."""
    HISTORIC = "historic"
    NOTABLE = "notable"
    RARE = "rare"
    CUSTOM = "custom"


class ConditionRating(str, Enum):
    """Guitar condition rating."""
    MINT = "mint"
    EXCELLENT = "excellent"
    VERY_GOOD = "very_good"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    RELIC = "relic"


class SourceType(str, Enum):
    """Type of data source."""
    MANUFACTURER_CATALOG = "manufacturer_catalog"
    AUCTION_RECORD = "auction_record"
    MUSEUM = "museum"
    BOOK = "book"
    WEBSITE = "website"
    MANUAL_ENTRY = "manual_entry"
    PRICE_GUIDE = "price_guide"





# Core Models
class Manufacturer(BaseModel):
    """Guitar manufacturer information."""
    
    name: str = Field(..., min_length=1, max_length=100, description="Official company name")
    country: Optional[str] = Field(None, max_length=50, description="Country of headquarters")
    founded_year: Optional[int] = Field(None, ge=1800, le=2030, description="Year company was established")
    website: Optional[HttpUrl] = Field(None, description="Current company website URL")
    status: ManufacturerStatus = Field(ManufacturerStatus.ACTIVE, description="Operational status")
    notes: Optional[str] = Field(None, description="Additional historical or contextual information")
    logo_source: Optional[str] = Field(None, description="Path to company logo image file")


class Model(BaseModel):
    """Guitar model specifications."""
    
    manufacturer_name: str = Field(..., description="Manufacturer name (will be resolved to manufacturer_id)")
    product_line_name: Optional[str] = Field(None, description="Product series or line name")
    name: str = Field(..., min_length=1, max_length=150, description="Model name as it appears in catalogs")
    year: int = Field(..., ge=1900, le=2030, description="Year the model was introduced")
    production_type: ProductionType = Field(ProductionType.MASS, description="Production volume type")
    production_start_date: Optional[date] = Field(None, description="Production start date")
    production_end_date: Optional[date] = Field(None, description="Production end date")
    estimated_production_quantity: Optional[int] = Field(None, ge=1, description="Total units produced")
    msrp_original: Optional[Decimal] = Field(None, ge=0, description="Original retail price")
    currency: str = Field("USD", max_length=3, description="ISO currency code")
    description: Optional[str] = Field(None, description="Detailed description of the model")
    specifications: Optional[Union["Specifications", List["Specifications"]]] = Field(None, description="Technical specifications (single object or array for multiple variants)")


class IndividualGuitar(BaseModel):
    """Individual guitar instance with hybrid FK + fallback approach."""
    
    # Foreign key reference (optional - for complete data)
    model_reference: Optional["ModelReference"] = Field(None, description="Reference to existing model")
    
    # Fallback text fields (for incomplete data)
    manufacturer_name_fallback: Optional[str] = Field(None, max_length=100, description="Manufacturer name when exact match not found")
    model_name_fallback: Optional[str] = Field(None, max_length=150, description="Model name when exact match not found")
    year_estimate: Optional[str] = Field(None, max_length=50, description="Year estimate like 'circa 1959', 'late 1950s'")
    description: Optional[str] = Field(None, description="General description when model info is incomplete")
    
    # Guitar-specific fields
    serial_number: Optional[str] = Field(None, max_length=50, description="Guitar's unique serial number")
    production_date: Optional[date] = Field(None, description="Specific production date if known")
    production_number: Optional[int] = Field(None, description="Production sequence number if known")
    significance_level: SignificanceLevel = Field(SignificanceLevel.NOTABLE, description="Historical significance level")
    significance_notes: Optional[str] = Field(None, description="Explanation of significance")
    current_estimated_value: Optional[Decimal] = Field(None, description="Current market value estimate")
    last_valuation_date: Optional[date] = Field(None, description="Date of last valuation")
    condition_rating: Optional[ConditionRating] = Field(None, description="Current condition rating")
    modifications: Optional[str] = Field(None, description="Description of any modifications")
    provenance_notes: Optional[str] = Field(None, description="History of ownership and usage")
    specifications: Optional["Specifications"] = Field(None, description="Individual-specific specifications")
    photos: Optional[List["Photo"]] = Field(None, description="Array of photo objects for image processing")
    
    @model_validator(mode='after')
    def validate_identification_method(self) -> 'IndividualGuitar':
        """Ensure exactly one identification method is provided."""
        has_model_ref = self.model_reference is not None
        has_fallback = (self.manufacturer_name_fallback is not None and 
                       (self.model_name_fallback is not None or self.description is not None))
        
        if not has_model_ref and not has_fallback:
            raise ValueError("Must provide either model_reference OR fallback manufacturer + (model OR description)")
        
        if has_model_ref and has_fallback:
            raise ValueError("Cannot provide both model_reference AND fallback fields")
        
        return self


class ModelReference(BaseModel):
    """Reference to an existing model for individual guitar identification."""
    
    manufacturer_name: str = Field(..., description="Manufacturer name (case-insensitive match)")
    model_name: str = Field(..., description="Model name (case-insensitive match)")
    year: int = Field(..., description="Model year (exact match required)")


class SourceAttribution(BaseModel):
    """Data source attribution and reliability information."""
    
    source_name: str = Field(..., min_length=1, max_length=100, description="Name of the source")
    source_type: Optional[SourceType] = Field(None, description="Type of source")
    url: Optional[HttpUrl] = Field(None, max_length=500, description="URL to the source if available online")
    isbn: Optional[str] = Field(None, max_length=20, description="ISBN for books")
    publication_date: Optional[date] = Field(None, description="Date the source was published")
    reliability_score: Optional[int] = Field(None, ge=1, le=10, description="1=least reliable, 10=most reliable")
    notes: Optional[str] = Field(None, description="Additional information about the source")


class Specifications(BaseModel):
    """Technical specifications for guitars."""
    
    body_wood: Optional[str] = Field(None, max_length=50, description="Primary wood used for guitar body")
    neck_wood: Optional[str] = Field(None, max_length=50, description="Primary wood used for neck")
    fingerboard_wood: Optional[str] = Field(None, max_length=50, description="Wood used for fingerboard")
    scale_length_inches: Optional[float] = Field(None, ge=20, le=30, description="Scale length in inches")
    num_frets: Optional[int] = Field(None, ge=12, le=36, description="Number of frets")
    nut_width_inches: Optional[float] = Field(None, ge=1.0, le=2.5, description="Width of nut in inches")
    neck_profile: Optional[str] = Field(None, max_length=50, description="Neck shape profile")
    bridge_type: Optional[str] = Field(None, max_length=50, description="Type of bridge")
    pickup_configuration: Optional[str] = Field(None, max_length=150, description="Pickup styles, brand, and arrangement (e.g., '2 x single coils (SS)', '2 x PAF humbuckers', 'Seymour Duncan JB TB-4 humbucker in the bridge and two Seymour Duncan SSL-6 single coils in the middle and neck positions')")
    electronics_description: Optional[str] = Field(None, description="Description of electronics and controls")
    hardware_finish: Optional[str] = Field(None, max_length=50, description="Finish of hardware")
    body_finish: Optional[str] = Field(None, description="Finish of guitar body (e.g., 'Nitrocellulose Cherry Sunburst', 'Olympic White, Lake placid Blue', 'Sandblasted satin urethane, multiple colors')")
    weight_lbs: Optional[float] = Field(None, ge=1, le=20, description="Weight in pounds")
    case_included: Optional[bool] = Field(None, description="Whether case was included")
    case_type: Optional[str] = Field(None, max_length=50, description="Type of case if included")





class Photo(BaseModel):
    """Photo object for image processing."""
    
    file_path: str = Field(..., description="Path to the image file")
    photo_type: str = Field(..., description="Type of photo (e.g., 'primary', 'gallery', 'serial_number')")
    description: Optional[str] = Field(None, description="Description of the photo")
    is_primary: bool = Field(False, description="Whether this is the primary image")


# Composite Models
class GuitarSubmission(BaseModel):
    """Complete guitar submission with all required entities."""
    
    manufacturer: Optional[Manufacturer] = Field(None, description="Manufacturer information (if new)")
    model: Optional[Model] = Field(None, description="Model information (if new)")
    individual_guitar: IndividualGuitar = Field(..., description="Individual guitar data (required)")
    source_attribution: Optional[SourceAttribution] = Field(None, description="Source attribution (optional)")
    
    @model_validator(mode='after')
    def validate_submission_structure(self) -> 'GuitarSubmission':
        """Ensure submission has required structure."""
        # Must have either manufacturer + model OR individual_guitar with model_reference
        has_manufacturer_model = self.manufacturer is not None and self.model is not None
        has_model_reference = self.individual_guitar.model_reference is not None
        
        if not has_manufacturer_model and not has_model_reference:
            raise ValueError("Must provide either manufacturer+model OR individual_guitar with model_reference")
        
        return self


class BatchSubmission(BaseModel):
    """Multiple guitar submissions."""
    
    submissions: List[GuitarSubmission] = Field(..., min_length=1, description="List of guitar submissions")
    
    @field_validator('submissions')
    @classmethod
    def validate_submissions(cls, v: List[GuitarSubmission]) -> List[GuitarSubmission]:
        """Validate that all submissions are valid."""
        if not v:
            raise ValueError("Must provide at least one submission")
        return v


# Update forward references
Model.model_rebuild()
IndividualGuitar.model_rebuild()
GuitarSubmission.model_rebuild()
