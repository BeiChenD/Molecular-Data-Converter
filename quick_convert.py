#!/usr/bin/env python3
"""
Quick Molecular Data Converter
==============================

A simplified script for quick conversion of DCD/PSF files to XYZ coordinates.

Author: Bei Chen
"""

import MDAnalysis as mda
import numpy as np
import os

def quick_convert(psf_file, dcd_file, output_prefix="converted"):
    """
    Quickly convert DCD/PSF files to XYZ format.
    
    Args:
        psf_file (str): Path to PSF file
        dcd_file (str): Path to DCD file
        output_prefix (str): Prefix for output files
    """
    
    print(f"Loading {psf_file} and {dcd_file}...")
    
    # Load the molecular system
    u = mda.Universe(psf_file, dcd_file)
    
    print(f"System loaded successfully!")
    print(f"Atoms: {u.atoms.n_atoms}")
    print(f"Frames: {len(u.trajectory)}")
    
    # Convert first frame
    u.trajectory[0]  # Go to first frame
    coords = u.atoms.positions
    
    # Save as XYZ file
    output_file = f"{output_prefix}_frame_0.xyz"
    with open(output_file, 'w') as f:
        f.write(f"{len(coords)}\n")
        f.write(f"Frame 0 from {dcd_file}\n")
        
        for i, coord in enumerate(coords):
            # Try to get atom names/elements
            if hasattr(u.atoms, 'names'):
                atom_name = u.atoms.names[i]
            else:
                atom_name = f"ATOM{i}"
            
            f.write(f"{atom_name:4s} {coord[0]:12.6f} {coord[1]:12.6f} {coord[2]:12.6f}\n")
    
    print(f"First frame saved to: {output_file}")
    
    # Save coordinates as simple text file
    np.savetxt(f"{output_prefix}_coordinates.txt", coords, 
               fmt="%.6f", header="X Y Z coordinates (Angstroms)")
    
    print(f"Raw coordinates saved to: {output_prefix}_coordinates.txt")
    
    return u, coords

if __name__ == "__main__":
    # Quick conversion
    universe, coordinates = quick_convert("H3O_ws.psf", "H3O_ws_short.dcd")
    
    print(f"\nCoordinates shape: {coordinates.shape}")
    print(f"Coordinate range:")
    print(f"  X: {coordinates[:, 0].min():.2f} to {coordinates[:, 0].max():.2f} Å")
    print(f"  Y: {coordinates[:, 1].min():.2f} to {coordinates[:, 1].max():.2f} Å") 
    print(f"  Z: {coordinates[:, 2].min():.2f} to {coordinates[:, 2].max():.2f} Å")
