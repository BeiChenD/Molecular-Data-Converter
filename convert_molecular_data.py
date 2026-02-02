#!/usr/bin/env python3
"""
Molecular Data Converter
========================

This program converts binary molecular dynamics data formats (.dcd and .psf files)
to XYZ coordinates using MDAnalysis. It provides multiple output formats and 
visualization capabilities.

Author: Bei Chen
Date: January 26, 2026
"""

import MDAnalysis as mda
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
import sys
from pathlib import Path

class MolecularDataConverter:
    """
    A class to handle conversion of molecular dynamics data from binary formats
    to human-readable coordinate formats.
    """
    
    def __init__(self, psf_file, dcd_file):
        """
        Initialize the converter with PSF and DCD files.
        
        Args:
            psf_file (str): Path to the PSF (Protein Structure File)
            dcd_file (str): Path to the DCD (CHARMM trajectory file)
        """
        self.psf_file = psf_file
        self.dcd_file = dcd_file
        self.universe = None
        self.load_data()
    
    def load_data(self):
        """Load the molecular data using MDAnalysis."""
        try:
            print(f"Loading PSF file: {self.psf_file}")
            print(f"Loading DCD file: {self.dcd_file}")
            
            # Create MDAnalysis Universe
            self.universe = mda.Universe(self.psf_file, self.dcd_file)
            
            print(f"Successfully loaded molecular system!")
            print(f"Number of atoms: {self.universe.atoms.n_atoms}")
            print(f"Number of frames: {len(self.universe.trajectory)}")
            print(f"Time range: {self.universe.trajectory[0].time:.2f} - {self.universe.trajectory[-1].time:.2f} ps")
            
        except Exception as e:
            print(f"Error loading files: {e}")
            sys.exit(1)
    
    def get_system_info(self):
        """Print detailed information about the molecular system."""
        print("\n" + "="*50)
        print("MOLECULAR SYSTEM INFORMATION")
        print("="*50)
        
        atoms = self.universe.atoms
        print(f"Total atoms: {atoms.n_atoms}")
        print(f"Total frames: {len(self.universe.trajectory)}")
        
        # Get unique elements
        if hasattr(atoms, 'elements'):
            elements = np.unique(atoms.elements)
            print(f"Elements present: {', '.join(elements)}")
        
        # Get unique residues
        if hasattr(atoms, 'resnames'):
            residues = np.unique(atoms.resnames)
            print(f"Residue types: {', '.join(residues)}")
            print(f"Number of residues: {atoms.n_residues}")
        
        # Box dimensions
        if self.universe.trajectory[0].dimensions is not None:
            box = self.universe.trajectory[0].dimensions
            print(f"Box dimensions: {box[0]:.2f} x {box[1]:.2f} x {box[2]:.2f} Å")
        
        print("="*50)
    
    def extract_coordinates_frame(self, frame_index=0):
        """
        Extract coordinates from a specific frame.
        
        Args:
            frame_index (int): Frame number to extract (default: 0 for first frame)
            
        Returns:
            numpy.ndarray: Array of coordinates (N_atoms x 3)
        """
        self.universe.trajectory[frame_index]
        return self.universe.atoms.positions.copy()
    
    def extract_all_coordinates(self):
        """
        Extract coordinates from all frames.
        
        Returns:
            numpy.ndarray: Array of coordinates (N_frames x N_atoms x 3)
        """
        n_frames = len(self.universe.trajectory)
        n_atoms = self.universe.atoms.n_atoms
        
        all_coords = np.zeros((n_frames, n_atoms, 3))
        
        print(f"\nExtracting coordinates from {n_frames} frames...")
        
        for i, ts in enumerate(self.universe.trajectory):
            all_coords[i] = self.universe.atoms.positions.copy()
            if (i + 1) % max(1, n_frames // 10) == 0:
                print(f"Progress: {i+1}/{n_frames} frames ({(i+1)/n_frames*100:.1f}%)")
        
        return all_coords
    
    def save_xyz_format(self, coordinates, output_file, frame_index=None):
        """
        Save coordinates in XYZ format.
        
        Args:
            coordinates (numpy.ndarray): Coordinates to save
            output_file (str): Output file path
            frame_index (int): Frame index if saving single frame
        """
        atoms = self.universe.atoms
        n_atoms = len(coordinates)
        
        with open(output_file, 'w') as f:
            f.write(f"{n_atoms}\n")
            
            if frame_index is not None:
                f.write(f"Frame {frame_index}, Time: {self.universe.trajectory[frame_index].time:.2f} ps\n")
            else:
                f.write("Molecular coordinates from MD simulation\n")
            
            for i, coord in enumerate(coordinates):
                # Try to get element name, fallback to atom name or index
                if hasattr(atoms, 'elements') and len(atoms.elements) > i:
                    element = atoms.elements[i]
                elif hasattr(atoms, 'names') and len(atoms.names) > i:
                    element = atoms.names[i]
                else:
                    element = f"ATOM{i}"
                
                f.write(f"{element:4s} {coord[0]:12.6f} {coord[1]:12.6f} {coord[2]:12.6f}\n")
        
        print(f"XYZ coordinates saved to: {output_file}")
    
    def save_csv_format(self, coordinates, output_file, frame_index=None):
        """
        Save coordinates in CSV format with additional atom information.
        
        Args:
            coordinates (numpy.ndarray): Coordinates to save
            output_file (str): Output file path
            frame_index (int): Frame index if saving single frame
        """
        atoms = self.universe.atoms
        
        data = {
            'atom_index': range(len(coordinates)),
            'x': coordinates[:, 0],
            'y': coordinates[:, 1],
            'z': coordinates[:, 2]
        }
        
        # Add additional atom information if available
        if hasattr(atoms, 'names'):
            data['atom_name'] = atoms.names
        if hasattr(atoms, 'elements'):
            data['element'] = atoms.elements
        if hasattr(atoms, 'resnames'):
            data['residue_name'] = atoms.resnames
        if hasattr(atoms, 'resids'):
            data['residue_id'] = atoms.resids
        
        df = pd.DataFrame(data)
        df.to_csv(output_file, index=False, float_format='%.6f')
        
        print(f"CSV coordinates saved to: {output_file}")
    
    def visualize_structure(self, frame_index=0, save_plot=True, output_dir="output"):
        """
        Create 3D visualization of the molecular structure.
        
        Args:
            frame_index (int): Frame to visualize
            save_plot (bool): Whether to save the plot
            output_dir (str): Directory to save plots
        """
        coordinates = self.extract_coordinates_frame(frame_index)
        
        # Create 3D plot
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Color atoms by element if available
        atoms = self.universe.atoms
        if hasattr(atoms, 'elements'):
            # Create color map for different elements
            unique_elements = np.unique(atoms.elements)
            colors = plt.cm.tab10(np.linspace(0, 1, len(unique_elements)))
            element_colors = {elem: colors[i] for i, elem in enumerate(unique_elements)}
            
            for element in unique_elements:
                mask = atoms.elements == element
                if np.any(mask):
                    coords = coordinates[mask]
                    ax.scatter(coords[:, 0], coords[:, 1], coords[:, 2], 
                             c=[element_colors[element]], label=element, s=50, alpha=0.7)
        else:
            ax.scatter(coordinates[:, 0], coordinates[:, 1], coordinates[:, 2], 
                      c='blue', s=50, alpha=0.7)
        
        ax.set_xlabel('X (Å)')
        ax.set_ylabel('Y (Å)')
        ax.set_zlabel('Z (Å)')
        ax.set_title(f'Molecular Structure - Frame {frame_index}')
        
        if hasattr(atoms, 'elements'):
            ax.legend()
        
        plt.tight_layout()
        
        if save_plot:
            os.makedirs(output_dir, exist_ok=True)
            plot_file = os.path.join(output_dir, f'structure_frame_{frame_index}.png')
            plt.savefig(plot_file, dpi=300, bbox_inches='tight')
            print(f"Structure plot saved to: {plot_file}")
        
        plt.show()
    
    def analyze_trajectory(self, save_analysis=True, output_dir="output"):
        """
        Perform trajectory analysis and create plots.
        
        Args:
            save_analysis (bool): Whether to save analysis plots
            output_dir (str): Directory to save analysis
        """
        print("\nAnalyzing molecular trajectory...")
        
        n_frames = len(self.universe.trajectory)
        times = []
        center_of_mass = []
        
        for ts in self.universe.trajectory:
            times.append(ts.time)
            center_of_mass.append(self.universe.atoms.center_of_mass())
        
        times = np.array(times)
        center_of_mass = np.array(center_of_mass)
        
        # Create analysis plots
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Center of mass trajectory
        axes[0, 0].plot(times, center_of_mass[:, 0], label='X')
        axes[0, 0].plot(times, center_of_mass[:, 1], label='Y')
        axes[0, 0].plot(times, center_of_mass[:, 2], label='Z')
        axes[0, 0].set_xlabel('Time (ps)')
        axes[0, 0].set_ylabel('Center of Mass (Å)')
        axes[0, 0].set_title('Center of Mass vs Time')
        axes[0, 0].legend()
        axes[0, 0].grid(True)
        
        # 3D trajectory of center of mass
        axes[0, 1].remove()
        axes[0, 1] = fig.add_subplot(2, 2, 2, projection='3d')
        axes[0, 1].plot(center_of_mass[:, 0], center_of_mass[:, 1], center_of_mass[:, 2])
        axes[0, 1].scatter(center_of_mass[0, 0], center_of_mass[0, 1], center_of_mass[0, 2], 
                          c='green', s=100, label='Start')
        axes[0, 1].scatter(center_of_mass[-1, 0], center_of_mass[-1, 1], center_of_mass[-1, 2], 
                          c='red', s=100, label='End')
        axes[0, 1].set_xlabel('X (Å)')
        axes[0, 1].set_ylabel('Y (Å)')
        axes[0, 1].set_zlabel('Z (Å)')
        axes[0, 1].set_title('Center of Mass Trajectory')
        axes[0, 1].legend()
        
        # Distance from origin
        distances = np.linalg.norm(center_of_mass, axis=1)
        axes[1, 0].plot(times, distances)
        axes[1, 0].set_xlabel('Time (ps)')
        axes[1, 0].set_ylabel('Distance from Origin (Å)')
        axes[1, 0].set_title('Distance from Origin vs Time')
        axes[1, 0].grid(True)
        
        # RMSD-like measure (deviation from first frame)
        first_frame_com = center_of_mass[0]
        deviations = np.linalg.norm(center_of_mass - first_frame_com, axis=1)
        axes[1, 1].plot(times, deviations)
        axes[1, 1].set_xlabel('Time (ps)')
        axes[1, 1].set_ylabel('Deviation from First Frame (Å)')
        axes[1, 1].set_title('Center of Mass Deviation')
        axes[1, 1].grid(True)
        
        plt.tight_layout()
        
        if save_analysis:
            os.makedirs(output_dir, exist_ok=True)
            analysis_file = os.path.join(output_dir, 'trajectory_analysis.png')
            plt.savefig(analysis_file, dpi=300, bbox_inches='tight')
            print(f"Trajectory analysis saved to: {analysis_file}")
        
        plt.show()

def main():
    """Main function to run the molecular data converter."""
    
    # File paths
    psf_file = "H3O_ws.psf"
    dcd_file = "H3O_ws_short.dcd"
    output_dir = "output"
    
    # Check if files exist
    if not os.path.exists(psf_file):
        print(f"Error: PSF file '{psf_file}' not found!")
        return
    if not os.path.exists(dcd_file):
        print(f"Error: DCD file '{dcd_file}' not found!")
        return
    
    print("Molecular Data Converter")
    print("=" * 30)
    
    # Create converter instance
    converter = MolecularDataConverter(psf_file, dcd_file)
    
    # Get system information
    converter.get_system_info()
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Extract and save coordinates for the first frame
    print(f"\nExtracting coordinates for first frame...")
    first_frame_coords = converter.extract_coordinates_frame(0)
    
    # Save in different formats
    converter.save_xyz_format(first_frame_coords, 
                            os.path.join(output_dir, "first_frame.xyz"), 
                            frame_index=0)
    
    converter.save_csv_format(first_frame_coords, 
                            os.path.join(output_dir, "first_frame.csv"), 
                            frame_index=0)
    
    # Extract coordinates for last frame
    last_frame_idx = len(converter.universe.trajectory) - 1
    print(f"\nExtracting coordinates for last frame (frame {last_frame_idx})...")
    last_frame_coords = converter.extract_coordinates_frame(last_frame_idx)
    
    converter.save_xyz_format(last_frame_coords, 
                            os.path.join(output_dir, "last_frame.xyz"), 
                            frame_index=last_frame_idx)
    
    converter.save_csv_format(last_frame_coords, 
                            os.path.join(output_dir, "last_frame.csv"), 
                            frame_index=last_frame_idx)
    
    # Option to extract all frames
    n_frames = len(converter.universe.trajectory)
    if n_frames > 10:
        print(f"\nFound {n_frames} frames. Extract all? (y/n): ", end="")
        response = input().lower().strip()
        if response in ['y', 'yes']:
            all_coords = converter.extract_all_coordinates()
            
            # Save selected frames
            frame_indices = [0, n_frames//4, n_frames//2, 3*n_frames//4, n_frames-1]
            for i, frame_idx in enumerate(frame_indices):
                if frame_idx < n_frames:
                    converter.save_xyz_format(all_coords[frame_idx], 
                                            os.path.join(output_dir, f"frame_{frame_idx}.xyz"), 
                                            frame_index=frame_idx)
    else:
        # Extract all frames if there are few
        all_coords = converter.extract_all_coordinates()
        for frame_idx in range(n_frames):
            converter.save_xyz_format(all_coords[frame_idx], 
                                    os.path.join(output_dir, f"frame_{frame_idx}.xyz"), 
                                    frame_index=frame_idx)
    
    # Visualize structure
    print(f"\nCreating visualizations...")
    converter.visualize_structure(frame_index=0, output_dir=output_dir)
    
    # Analyze trajectory
    converter.analyze_trajectory(output_dir=output_dir)
    
    print(f"\n" + "="*50)
    print("CONVERSION COMPLETE!")
    print(f"All output files saved to: {output_dir}/")
    print("="*50)

if __name__ == "__main__":
    main()
