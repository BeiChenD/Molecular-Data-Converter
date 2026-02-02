#!/usr/bin/env python3
"""
Simple Molecular Visualizer
===========================

A non-interactive script to convert and visualize molecular data.
"""

import MDAnalysis as mda
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

def main():
    print("Simple Molecular Data Converter & Visualizer")
    print("=" * 50)
    
    # Load molecular system
    psf_file = "H3O_ws.psf"
    dcd_file = "H3O_ws_short.dcd"
    
    print(f"Loading {psf_file} and {dcd_file}...")
    u = mda.Universe(psf_file, dcd_file)
    
    print(f"System Info:")
    print(f"  Atoms: {u.atoms.n_atoms}")
    print(f"  Frames: {len(u.trajectory)}")
    print(f"  Residues: {u.atoms.n_residues}")
    print(f"  Time range: {u.trajectory[0].time:.2f} - {u.trajectory[-1].time:.2f} ps")
    
    # Create output directory
    os.makedirs("output", exist_ok=True)
    
    # Extract first frame coordinates
    u.trajectory[0]
    coords = u.atoms.positions
    
    # Save as XYZ
    with open("output/simple_frame_0.xyz", 'w') as f:
        f.write(f"{len(coords)}\n")
        f.write(f"H3O hydrated system - Frame 0\n")
        for i, coord in enumerate(coords):
            atom_name = u.atoms.names[i] if hasattr(u.atoms, 'names') else f"ATOM{i}"
            f.write(f"{atom_name:4s} {coord[0]:12.6f} {coord[1]:12.6f} {coord[2]:12.6f}\n")
    
    print("✓ XYZ file saved to: output/simple_frame_0.xyz")
    
    # Save coordinates as numpy array
    np.savetxt("output/coordinates_array.txt", coords, 
               fmt="%.6f", header="X Y Z coordinates (Angstroms)")
    print("✓ Raw coordinates saved to: output/coordinates_array.txt")
    
    # Create 3D visualization
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Color by residue if available
    if hasattr(u.atoms, 'resnames'):
        unique_residues = np.unique(u.atoms.resnames)
        colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown']
        
        for i, res_name in enumerate(unique_residues):
            mask = u.atoms.resnames == res_name
            res_coords = coords[mask]
            color = colors[i % len(colors)]
            ax.scatter(res_coords[:, 0], res_coords[:, 1], res_coords[:, 2], 
                      c=color, label=res_name, s=50, alpha=0.7)
    else:
        ax.scatter(coords[:, 0], coords[:, 1], coords[:, 2], 
                  c='blue', s=50, alpha=0.7)
    
    ax.set_xlabel('X (Angstroms)')
    ax.set_ylabel('Y (Angstroms)')
    ax.set_zlabel('Z (Angstroms)')
    ax.set_title('Molecular Structure (Frame 0)')
    
    if hasattr(u.atoms, 'resnames'):
        ax.legend()
    
    plt.tight_layout()
    plt.savefig("output/molecular_structure.png", dpi=300, bbox_inches='tight')
    print("✓ 3D structure plot saved to: output/molecular_structure.png")
    
    # Create 2D projections
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    projections = [('X-Y', coords[:, 0], coords[:, 1]), 
                   ('X-Z', coords[:, 0], coords[:, 2]), 
                   ('Y-Z', coords[:, 1], coords[:, 2])]
    
    for i, (title, x, y) in enumerate(projections):
        if hasattr(u.atoms, 'resnames'):
            for j, res_name in enumerate(unique_residues):
                mask = u.atoms.resnames == res_name
                color = colors[j % len(colors)]
                axes[i].scatter(x[mask], y[mask], c=color, label=res_name, s=30, alpha=0.7)
        else:
            axes[i].scatter(x, y, c='blue', s=30, alpha=0.7)
        
        axes[i].set_title(f'{title} Projection')
        axes[i].set_xlabel(f'{title.split("-")[0]} (Angstroms)')
        axes[i].set_ylabel(f'{title.split("-")[1]} (Angstroms)')
        axes[i].grid(True, alpha=0.3)
        if i == 0 and hasattr(u.atoms, 'resnames'):
            axes[i].legend()
    
    plt.tight_layout()
    plt.savefig("output/projections.png", dpi=300, bbox_inches='tight')
    print("✓ 2D projections saved to: output/projections.png")
    
    # Trajectory analysis (sample every 100th frame to speed up)
    print("\nAnalyzing trajectory (sampling every 100th frame)...")
    
    n_frames = len(u.trajectory)
    sample_frames = range(0, n_frames, 100)
    times = []
    center_of_mass = []
    
    for frame_idx in sample_frames:
        u.trajectory[frame_idx]
        times.append(u.trajectory.time)
        center_of_mass.append(u.atoms.center_of_mass())
    
    times = np.array(times)
    center_of_mass = np.array(center_of_mass)
    
    # Plot center of mass trajectory
    plt.figure(figsize=(12, 8))
    
    plt.subplot(2, 2, 1)
    plt.plot(times, center_of_mass[:, 0], 'r-', label='X')
    plt.plot(times, center_of_mass[:, 1], 'g-', label='Y') 
    plt.plot(times, center_of_mass[:, 2], 'b-', label='Z')
    plt.xlabel('Time (ps)')
    plt.ylabel('Center of Mass (Å)')
    plt.title('Center of Mass vs Time')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(2, 2, 2)
    distances = np.linalg.norm(center_of_mass, axis=1)
    plt.plot(times, distances, 'k-')
    plt.xlabel('Time (ps)')
    plt.ylabel('Distance from Origin (Å)')
    plt.title('Distance from Origin')
    plt.grid(True)
    
    plt.subplot(2, 2, 3)
    drift = np.linalg.norm(center_of_mass - center_of_mass[0], axis=1)
    plt.plot(times, drift, 'm-')
    plt.xlabel('Time (ps)')
    plt.ylabel('Drift from Initial Position (Å)')
    plt.title('System Drift')
    plt.grid(True)
    
    plt.subplot(2, 2, 4)
    plt.plot(center_of_mass[:, 0], center_of_mass[:, 1], 'b-', alpha=0.7)
    plt.scatter(center_of_mass[0, 0], center_of_mass[0, 1], c='green', s=100, label='Start')
    plt.scatter(center_of_mass[-1, 0], center_of_mass[-1, 1], c='red', s=100, label='End')
    plt.xlabel('X (Å)')
    plt.ylabel('Y (Å)')
    plt.title('Center of Mass Trajectory (X-Y)')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig("output/trajectory_analysis.png", dpi=300, bbox_inches='tight')
    print("✓ Trajectory analysis saved to: output/trajectory_analysis.png")
    
    print("\n" + "=" * 50)
    print("CONVERSION AND ANALYSIS COMPLETE!")
    print("\nFiles created:")
    print("  - output/simple_frame_0.xyz (XYZ coordinates)")
    print("  - output/coordinates_array.txt (Raw coordinates)")
    print("  - output/molecular_structure.png (3D visualization)")
    print("  - output/projections.png (2D projections)")
    print("  - output/trajectory_analysis.png (Time evolution)")
    print("=" * 50)

if __name__ == "__main__":
    main()
