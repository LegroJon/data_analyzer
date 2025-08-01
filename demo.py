#!/usr/bin/env python3
"""
Demo script for the Data Analyzer.

This script demonstrates the functionality without requiring user input.
It uses sample data to show parsing capabilities.
"""

import sys
import os
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

from task_parser import TaskParser, generate_output_filename


def create_sample_data():
    """Create sample input data for demonstration."""
    sample_data = {
        "original_format.txt": """1. 07-CO-3036 Integrate Indirect Fire Support - Company 07 - Infantry (Collective) Approved
2. 71-CO-5100 Conduct Troop Leading Procedures 71 - Mission Command (Collective) Approved
3. 07-CO-3027 Integrate Direct Fires - Company 07 - Infantry (Collective) Approved
071-410-0010 Conduct a Leader's Reconnaissance 071 - Infantry (Individual) Approved
071-420-0005 Maneuver a Dismounted Platoon/Section 071 - Infantry (Individual) Approved
07-PLT-D8005 React to Direct Fire Contact While Mounted Rifle Platoon Battle Drill 07 - Infantry (Collective) Approved""",
        
        "drill_format.txt": """D8005 Approved React Direct Fire Contact While Mounted
D9508 Approved Establish Security at the Halt
D1234 Approved Move Under Direct Fire Contact"""
    }
    
    # Ensure input directory exists
    input_dir = project_root / "data" / "input"
    input_dir.mkdir(parents=True, exist_ok=True)
    
    # Create sample files
    for filename, content in sample_data.items():
        file_path = input_dir / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Created sample file: {file_path}")
    
    return list(sample_data.keys())


def run_demo():
    """Run the demonstration."""
    print("=" * 60)
    print("Data Analyzer - Demonstration")
    print("=" * 60)
    
    # Create sample data
    print("\n1. Creating sample input files...")
    sample_files = create_sample_data()
    
    # Initialize parser
    parser = TaskParser()
    
    # Process each sample file
    for filename in sample_files:
        print(f"\n2. Processing {filename}...")
        
        # Determine pattern type from filename
        pattern_type = "original" if "original" in filename else "drill"
        
        # Set up file paths
        input_path = project_root / "data" / "input" / filename
        output_filename = generate_output_filename(str(input_path), "demo")
        output_path = project_root / "data" / "output" / output_filename
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            # Parse the file
            tasks = parser.parse_file(str(input_path), pattern_type)
            print(f"   Parsed {len(tasks)} tasks")
            
            # Save to CSV
            parser.save_to_csv(tasks, str(output_path), pattern_type, include_headers=True)
            print(f"   Saved results to: {output_path}")
            
            # Show sample of parsed data
            if tasks:
                print(f"   Sample task: {tasks[0].to_list(pattern_type)}")
                
        except Exception as e:
            print(f"   Error processing {filename}: {e}")
    
    print("\n" + "=" * 60)
    print("Demo completed successfully!")
    print("Check the 'data/output/' directory for generated CSV files.")
    print("=" * 60)


if __name__ == "__main__":
    try:
        run_demo()
    except KeyboardInterrupt:
        print("\nDemo cancelled by user.")
    except Exception as e:
        print(f"Demo failed with error: {e}")
        sys.exit(1)
