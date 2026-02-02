#!/usr/bin/env python3
"""
Quick Starter for Molecular Data Conversion
===========================================

Simply run this script and follow the prompts to convert any PSF/DCD files.

Author: Bei Chen
Date: January 26, 2026
"""

import os
import sys
import glob
from pathlib import Path

def find_molecular_files():
    """Find PSF and DCD files in the current directory."""
    psf_files = glob.glob("*.psf")
    dcd_files = glob.glob("*.dcd")
    
    return psf_files, dcd_files

def main():
    print("🧬 MOLECULAR DATA CONVERTER - QUICK START 🧬")
    print("=" * 50)
    print("Author: Bei Chen")
    print("=" * 50)
    
    # Check for molecular files
    psf_files, dcd_files = find_molecular_files()
    
    if not psf_files:
        print("❌ No PSF files found in current directory!")
        psf_file = input("Enter path to your PSF file: ").strip()
        if not os.path.exists(psf_file):
            print("❌ PSF file not found!")
            return
    else:
        if len(psf_files) == 1:
            psf_file = psf_files[0]
            print(f"✅ Found PSF file: {psf_file}")
        else:
            print("📁 Multiple PSF files found:")
            for i, file in enumerate(psf_files):
                print(f"   {i+1}. {file}")
            choice = input("Select PSF file number: ").strip()
            try:
                psf_file = psf_files[int(choice)-1]
            except (ValueError, IndexError):
                print("❌ Invalid selection!")
                return
    
    if not dcd_files:
        print("❌ No DCD files found in current directory!")
        dcd_file = input("Enter path to your DCD file: ").strip()
        if not os.path.exists(dcd_file):
            print("❌ DCD file not found!")
            return
    else:
        if len(dcd_files) == 1:
            dcd_file = dcd_files[0]
            print(f"✅ Found DCD file: {dcd_file}")
        else:
            print("📁 Multiple DCD files found:")
            for i, file in enumerate(dcd_files):
                print(f"   {i+1}. {file}")
            choice = input("Select DCD file number: ").strip()
            try:
                dcd_file = dcd_files[int(choice)-1]
            except (ValueError, IndexError):
                print("❌ Invalid selection!")
                return
    
    print(f"\n🎯 Selected files:")
    print(f"   PSF: {psf_file}")
    print(f"   DCD: {dcd_file}")
    
    print(f"\n🚀 Choose conversion method:")
    print("   1. Quick conversion (fast, basic output)")
    print("   2. Full conversion (comprehensive with plots)")
    
    method = input("Enter choice (1 or 2): ").strip()
    
    if method == "1":
        # Quick conversion
        print("\n🏃‍♂️ Running quick conversion...")
        run_quick_conversion(psf_file, dcd_file)
    elif method == "2":
        # Full conversion
        print("\n🔬 Running full conversion...")
        run_full_conversion(psf_file, dcd_file)
    else:
        print("❌ Invalid choice!")
        return

def run_quick_conversion(psf_file, dcd_file):
    """Run the quick conversion script."""
    try:
        import MDAnalysis as mda
        import numpy as np
        
        print(f"Loading {psf_file} and {dcd_file}...")
        u = mda.Universe(psf_file, dcd_file)
        
        print(f"✅ System loaded successfully!")
        print(f"   Atoms: {u.atoms.n_atoms}")
        print(f"   Frames: {len(u.trajectory)}")
        
        # Convert first frame
        u.trajectory[0]
        coords = u.atoms.positions
        
        # Create output filename
        base_name = Path(dcd_file).stem
        output_file = f"{base_name}_converted.xyz"
        
        # Save as XYZ file
        with open(output_file, 'w') as f:
            f.write(f"{len(coords)}\n")
            f.write(f"Converted from {dcd_file} by Bei Chen\n")
            
            for i, coord in enumerate(coords):
                if hasattr(u.atoms, 'names'):
                    atom_name = u.atoms.names[i]
                else:
                    atom_name = f"ATOM{i}"
                
                f.write(f"{atom_name:4s} {coord[0]:12.6f} {coord[1]:12.6f} {coord[2]:12.6f}\n")
        
        print(f"✅ Conversion complete!")
        print(f"   Output: {output_file}")
        print(f"   Coordinate range:")
        print(f"     X: {coords[:, 0].min():.2f} to {coords[:, 0].max():.2f} Å")
        print(f"     Y: {coords[:, 1].min():.2f} to {coords[:, 1].max():.2f} Å")
        print(f"     Z: {coords[:, 2].min():.2f} to {coords[:, 2].max():.2f} Å")
        
    except ImportError:
        print("❌ MDAnalysis not installed!")
        print("Install with: pip install MDAnalysis")
    except Exception as e:
        print(f"❌ Error: {e}")

def run_full_conversion(psf_file, dcd_file):
    """Run the full conversion script."""
    # Modify the main converter to use custom files
    try:
        from convert_molecular_data import MolecularDataConverter
        
        # Create converter with custom files
        converter = MolecularDataConverter(psf_file, dcd_file)
        
        # Get system info
        converter.get_system_info()
        
        # Create output directory
        output_dir = f"output_{Path(dcd_file).stem}"
        os.makedirs(output_dir, exist_ok=True)
        
        # Extract first and last frames
        print(f"\n📊 Extracting coordinates...")
        
        first_coords = converter.extract_coordinates_frame(0)
        converter.save_xyz_format(first_coords, 
                                os.path.join(output_dir, "first_frame.xyz"), 
                                frame_index=0)
        converter.save_csv_format(first_coords, 
                                os.path.join(output_dir, "first_frame.csv"), 
                                frame_index=0)
        
        last_idx = len(converter.universe.trajectory) - 1
        last_coords = converter.extract_coordinates_frame(last_idx)
        converter.save_xyz_format(last_coords, 
                                os.path.join(output_dir, "last_frame.xyz"), 
                                frame_index=last_idx)
        converter.save_csv_format(last_coords, 
                                os.path.join(output_dir, "last_frame.csv"), 
                                frame_index=last_idx)
        
        print(f"📈 Creating visualizations...")
        converter.visualize_structure(frame_index=0, output_dir=output_dir)
        
        print(f"✅ Full conversion complete!")
        print(f"   Output directory: {output_dir}/")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure MDAnalysis and other packages are installed:")
        print("pip install MDAnalysis matplotlib pandas")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
