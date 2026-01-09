"""
Example usage of shared models in the other projects.

This demonstrates how to create structured guitar data that will be
validated and processed by the guitar registry system.
"""

from sa_models import (
    GuitarSubmission,
    Manufacturer,
    Model,
    IndividualGuitar,
    SourceAttribution,
    Specifications,
    Finish,
    ModelReference,
    SignificanceLevel,
    ConditionRating,
    ProductionType,
    SourceType,
    FinishRarity
)


def create_gibson_les_paul_submission():
    """Create a complete submission for a Gibson Les Paul."""
    
    # Create manufacturer data
    manufacturer = Manufacturer(
        name="Gibson Guitar Corporation",
        country="USA",
        founded_year=1902,
        website="https://www.gibson.com",
        status="active",
        notes="Founded by Orville Gibson in Kalamazoo, Michigan",
        logo_source="images/gibson_logo.png"
    )
    
    # Create model data
    model = Model(
        manufacturer_name="Gibson Guitar Corporation",
        product_line_name="Les Paul",
        name="Les Paul Standard",
        year=1959,
        production_type=ProductionType.MASS,
        production_start_date="1959-01-01",
        estimated_production_quantity=1700,
        msrp_original=247.50,
        currency="USD",
        description="The legendary 1959 Les Paul Standard, considered the holy grail of electric guitars",
        specifications=Specifications(
            body_wood="Mahogany",
            neck_wood="Maple",
            fingerboard_wood="Rosewood",
            scale_length_inches=24.75,
            num_frets=22,
            nut_width_inches=1.6875,
            neck_profile="C-shape",
            bridge_type="Tune-o-matic",
            pickup_configuration="HH",
            pickup_brand="Gibson",
            pickup_model="PAF (Patent Applied For)",
            electronics_description="2 volume, 2 tone controls, 3-way selector switch",
            hardware_finish="Chrome",
            body_finish="Sunburst",
            weight_lbs=9.5,
            case_included=True,
            case_type="Brown Tolex"
        ),
        finishes=[
            Finish(
                finish_name="Cherry Sunburst",
                finish_type="Nitrocellulose",
                rarity=FinishRarity.RARE,
                notes="The most iconic finish for 1959 Les Pauls"
            ),
            Finish(
                finish_name="Gold Top",
                finish_type="Nitrocellulose",
                rarity=FinishRarity.UNCOMMON
            )
        ]
    )
    
    # Create individual guitar data
    individual_guitar = IndividualGuitar(
        model_reference=ModelReference(
            manufacturer_name="Gibson Guitar Corporation",
            model_name="Les Paul Standard",
            year=1959
        ),
        serial_number="9-0824",
        production_date="1959-06-15",
        significance_level=SignificanceLevel.HISTORIC,
        significance_notes="One of the most famous 1959 Les Pauls, owned by several notable musicians",
        current_estimated_value=500000.00,
        last_valuation_date="2024-01-15",
        condition_rating=ConditionRating.EXCELLENT,
        modifications="Original pickups replaced with period-correct PAFs in 1980s",
        provenance_notes="Originally sold at Grinnell's Music Store in Kalamazoo. Owned by multiple collectors.",
        photos=[
            {
                "file_path": "images/les_paul_9_0824_front.jpg",
                "photo_type": "primary",
                "description": "Front view of the guitar",
                "is_primary": True
            },
            {
                "file_path": "images/les_paul_9_0824_back.jpg",
                "photo_type": "body_back",
                "description": "Back view showing mahogany body"
            },
            {
                "file_path": "images/les_paul_9_0824_serial.jpg",
                "photo_type": "serial_number",
                "description": "Serial number 9-0824 on headstock"
            }
        ]
    )
    
    # Create source attribution
    source_attribution = SourceAttribution(
        source_name="Gibson 1959 Product Catalog",
        source_type=SourceType.MANUFACTURER_CATALOG,
        url="https://archive.org/gibson-1959-catalog",
        publication_date="1959-01-01",
        reliability_score=10,
        notes="Official manufacturer catalog, highest reliability"
    )
    
    # Create complete submission
    submission = GuitarSubmission(
        manufacturer=manufacturer,
        model=model,
        individual_guitar=individual_guitar,
        source_attribution=source_attribution
    )
    
    return submission


def create_fender_stratocaster_submission():
    """Create a submission for a Fender Stratocaster using only model reference."""
    
    # Create individual guitar with model reference (no new manufacturer/model data)
    individual_guitar = IndividualGuitar(
        model_reference=ModelReference(
            manufacturer_name="Fender Musical Instruments Corporation",
            model_name="Stratocaster",
            year=1954
        ),
        serial_number="01234",
        production_date="1954-06-15",
        significance_level=SignificanceLevel.HISTORIC,
        significance_notes="Early production Stratocaster, one of the first 100 made",
        current_estimated_value=75000.00,
        last_valuation_date="2024-01-20",
        condition_rating=ConditionRating.VERY_GOOD,
        modifications="Original pickups replaced in 1970s, otherwise unmodified",
        provenance_notes="Original owner family, never sold",
        photos=[
            {
                "file_path": "images/strat_01234_main.jpg",
                "photo_type": "primary",
                "description": "Main view of the Stratocaster",
                "is_primary": True
            }
        ]
    )
    
    # Create source attribution
    source_attribution = SourceAttribution(
        source_name="Fender 1954 Product Catalog",
        source_type=SourceType.MANUFACTURER_CATALOG,
        reliability_score=10,
        notes="Official manufacturer documentation"
    )
    
    # Create submission (no manufacturer/model since they already exist)
    submission = GuitarSubmission(
        individual_guitar=individual_guitar,
        source_attribution=source_attribution
    )
    
    return submission


def create_unknown_guitar_submission():
    """Create a submission for a guitar with incomplete information using fallback fields."""
    
    individual_guitar = IndividualGuitar(
        manufacturer_name_fallback="Unknown Manufacturer",
        model_name_fallback="Unknown Model",
        year_estimate="circa 1960s",
        description="Vintage electric guitar with single coil pickups, likely from the 1960s. Has a distinctive headstock shape and chrome hardware.",
        serial_number="UNK001",
        significance_level=SignificanceLevel.NOTABLE,
        significance_notes="Interesting vintage guitar with unknown origins",
        current_estimated_value=15000.00,
        condition_rating=ConditionRating.GOOD,
        modifications="Bridge pickup replaced, tuners upgraded",
        provenance_notes="Found in a vintage guitar shop, no known history",
        photos=[
            {
                "file_path": "images/unknown_guitar_main.jpg",
                "photo_type": "primary",
                "description": "Main view of the unknown guitar",
                "is_primary": True
            }
        ]
    )
    
    source_attribution = SourceAttribution(
        source_name="Vintage Guitar Shop Inventory",
        source_type=SourceType.MANUAL_ENTRY,
        reliability_score=6,
        notes="Information provided by shop owner, some details uncertain"
    )
    
    submission = GuitarSubmission(
        individual_guitar=individual_guitar,
        source_attribution=source_attribution
    )
    
    return submission


def export_submissions():
    """Export all submissions to JSON files."""
    
    submissions = [
        create_gibson_les_paul_submission(),
        create_fender_stratocaster_submission(),
        create_unknown_guitar_submission()
    ]
    
    # Export individual submissions
    for i, submission in enumerate(submissions):
        filename = f"guitar_submission_{i+1}.json"
        with open(filename, 'w') as f:
            f.write(submission.model_dump_json(indent=2))
        print(f"✓ Exported {filename}")
    
    # Export as batch
    from sa_models import BatchSubmission
    batch = BatchSubmission(submissions=submissions)
    
    with open("batch_submission.json", 'w') as f:
        f.write(batch.model_dump_json(indent=2))
    print("✓ Exported batch_submission.json")
    
    return submissions


if __name__ == "__main__":
    print("🎸 Creating guitar submissions...")
    
    try:
        submissions = export_submissions()
        print(f"\n✓ Successfully created {len(submissions)} submissions")
        
        # Validate that all submissions are correct
        for i, submission in enumerate(submissions):
            print(f"  • Submission {i+1}: {submission.individual_guitar.serial_number or 'No serial'}")
        
        print("\n📁 Files exported:")
        print("  • guitar_submission_1.json (Gibson Les Paul)")
        print("  • guitar_submission_2.json (Fender Stratocaster)")
        print("  • guitar_submission_3.json (Unknown Guitar)")
        print("  • batch_submission.json (All submissions)")
        
    except Exception as e:
        print(f"✗ Error creating submissions: {e}")
        import traceback
        traceback.print_exc()
