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
    
    def calculate_radial_distribution(self, element=None, max_radius=15.0, bins=150, 
                                     save_results=True, output_dir="output"):
        """
        Calculate radial density profile (RDF) of atoms from the center of mass.
        This shows how atoms are distributed at different distances from the droplet center.
        
        Args:
            element (str): Element to analyze (e.g., 'N', 'H', 'O'). If None, analyzes all atoms.
            max_radius (float): Maximum radius to consider (in Angstroms)
            bins (int): Number of bins for the histogram
            save_results (bool): Whether to save results to files
            output_dir (str): Directory to save outputs
            
        Returns:
            dict: Contains radii, densities, counts, and raw distances
        """
        print(f"\n{'='*60}")
        print("RADIAL DISTRIBUTION FUNCTION (RDF) ANALYSIS")
        print(f"{'='*60}")
        
        n_frames = len(self.universe.trajectory)
        
        # Select atoms based on element
        if element:
            if hasattr(self.universe.atoms, 'elements'):
                atom_group = self.universe.atoms[self.universe.atoms.elements == element]
                print(f"Analyzing element: {element}")
            elif hasattr(self.universe.atoms, 'names'):
                # Try to match by atom name if elements not available
                atom_group = self.universe.atoms[
                    [element in name for name in self.universe.atoms.names]
                ]
                print(f"Analyzing atoms matching name: {element}")
            else:
                print("Warning: Cannot filter by element. Using all atoms.")
                atom_group = self.universe.atoms
        else:
            atom_group = self.universe.atoms
            print("Analyzing all atoms")
        
        print(f"Number of atoms selected: {len(atom_group)}")
        print(f"Number of frames: {n_frames}")
        print(f"Calculating distances from center of mass...")
        
        # Collect distances from COM for all frames
        all_distances = []
        
        for frame_idx, ts in enumerate(self.universe.trajectory):
            # Calculate center of mass of entire system (droplet center)
            com = self.universe.atoms.center_of_mass()
            
            # Calculate distances of selected atoms from COM
            positions = atom_group.positions
            distances = np.linalg.norm(positions - com, axis=1)
            all_distances.extend(distances)
            
            if (frame_idx + 1) % max(1, n_frames // 10) == 0:
                print(f"  Progress: {frame_idx+1}/{n_frames} frames")
        
        all_distances = np.array(all_distances)
        
        # Create histogram (radial distribution)
        hist, bin_edges = np.histogram(all_distances, bins=bins, range=(0, max_radius))
        radii = (bin_edges[:-1] + bin_edges[1:]) / 2  # Bin centers
        bin_width = bin_edges[1] - bin_edges[0]
        
        # Calculate radial density (normalize by shell volume)
        # Shell volume = 4/3 * pi * (r_outer^3 - r_inner^3)
        shell_volumes = (4/3) * np.pi * (bin_edges[1:]**3 - bin_edges[:-1]**3)
        densities = hist / (shell_volumes * n_frames)  # atoms per Å³
        
        # Calculate number density (atoms per shell per frame)
        avg_counts_per_frame = hist / n_frames
        
        print(f"\n📊 RDF Statistics:")
        print(f"   Total distance measurements: {len(all_distances)}")
        print(f"   Average distance from COM: {np.mean(all_distances):.3f} Å")
        print(f"   Min distance: {np.min(all_distances):.3f} Å")
        print(f"   Max distance: {np.max(all_distances):.3f} Å")
        print(f"   Std deviation: {np.std(all_distances):.3f} Å")
        
        # Save results
        if save_results:
            os.makedirs(output_dir, exist_ok=True)
            
            # Save numerical data to CSV
            element_label = element if element else "all"
            csv_file = os.path.join(output_dir, f"rdf_{element_label}.csv")
            
            rdf_data = pd.DataFrame({
                'radius_angstrom': radii,
                'density_per_angstrom3': densities,
                'avg_count_per_frame': avg_counts_per_frame,
                'total_counts': hist,
                'shell_volume_angstrom3': shell_volumes
            })
            rdf_data.to_csv(csv_file, index=False, float_format='%.6f')
            print(f"✅ RDF data saved to: {csv_file}")
            
            # Save raw distances for further analysis
            dist_file = os.path.join(output_dir, f"distances_{element_label}.txt")
            np.savetxt(dist_file, all_distances, fmt='%.6f', 
                      header=f'Distances from COM for {element_label} atoms (Angstroms)')
            print(f"✅ Raw distances saved to: {dist_file}")
        
        return {
            'radii': radii,
            'densities': densities,
            'counts': avg_counts_per_frame,
            'raw_distances': all_distances,
            'element': element
        }
    
    def calculate_elemental_distribution(self, elements=None, max_radius=15.0, bins=150,
                                        save_results=True, plot=True, output_dir="output"):
        """
        Calculate and compare radial distributions for multiple elements.
        Generates comprehensive analysis and publication-quality plots.
        
        Args:
            elements (list): List of element symbols to analyze (e.g., ['N', 'H', 'O'])
            max_radius (float): Maximum radius for analysis (Angstroms)
            bins (int): Number of bins for histograms
            save_results (bool): Whether to save results
            plot (bool): Whether to generate plots
            output_dir (str): Output directory
            
        Returns:
            dict: RDF data for each element
        """
        print(f"\n{'='*60}")
        print("ELEMENTAL DISTRIBUTION ANALYSIS")
        print(f"{'='*60}")
        
        # Auto-detect elements if not specified
        if elements is None:
            if hasattr(self.universe.atoms, 'elements'):
                elements = list(np.unique(self.universe.atoms.elements))
                print(f"Auto-detected elements: {elements}")
            else:
                print("❌ Cannot detect elements. Please specify manually.")
                return None
        
        # Calculate RDF for each element
        rdf_results = {}
        
        for element in elements:
            print(f"\n--- Processing element: {element} ---")
            rdf_data = self.calculate_radial_distribution(
                element=element,
                max_radius=max_radius,
                bins=bins,
                save_results=save_results,
                output_dir=output_dir
            )
            rdf_results[element] = rdf_data
        
        # Create comprehensive comparison plots
        if plot and rdf_results:
            self._plot_elemental_comparison(rdf_results, output_dir)
        
        # Generate summary report
        if save_results:
            self._save_elemental_summary(rdf_results, elements, output_dir)
        
        return rdf_results
    
    def _plot_elemental_comparison(self, rdf_results, output_dir="output"):
        """Generate publication-quality comparison plots for elemental distributions."""
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Color scheme for elements
        element_colors = {
            'H': '#1f77b4',  # Blue
            'N': '#ff7f0e',  # Orange
            'O': '#d62728',  # Red
            'C': '#2ca02c',  # Green
            'S': '#9467bd',  # Purple
            'P': '#8c564b',  # Brown
        }
        
        # Create comprehensive figure with multiple subplots
        fig = plt.figure(figsize=(18, 12))
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
        
        # 1. Radial Density Profile (atoms/Å³)
        ax1 = fig.add_subplot(gs[0, 0])
        for element, data in rdf_results.items():
            color = element_colors.get(element, '#000000')
            ax1.plot(data['radii'], data['densities'], 
                    label=f'{element}', linewidth=2, color=color)
        ax1.set_xlabel('Distance from COM (Å)', fontsize=12)
        ax1.set_ylabel('Density (atoms/Å³)', fontsize=12)
        ax1.set_title('Radial Density Profile', fontsize=14, fontweight='bold')
        ax1.legend(fontsize=10)
        ax1.grid(True, alpha=0.3)
        
        # 2. Average Count per Shell
        ax2 = fig.add_subplot(gs[0, 1])
        for element, data in rdf_results.items():
            color = element_colors.get(element, '#000000')
            ax2.plot(data['radii'], data['counts'], 
                    label=f'{element}', linewidth=2, color=color)
        ax2.set_xlabel('Distance from COM (Å)', fontsize=12)
        ax2.set_ylabel('Avg. Atoms per Shell', fontsize=12)
        ax2.set_title('Average Atomic Count per Radial Shell', fontsize=14, fontweight='bold')
        ax2.legend(fontsize=10)
        ax2.grid(True, alpha=0.3)
        
        # 3. Cumulative Distribution
        ax3 = fig.add_subplot(gs[1, 0])
        for element, data in rdf_results.items():
            color = element_colors.get(element, '#000000')
            cumulative = np.cumsum(data['counts'])
            ax3.plot(data['radii'], cumulative, 
                    label=f'{element}', linewidth=2, color=color)
        ax3.set_xlabel('Distance from COM (Å)', fontsize=12)
        ax3.set_ylabel('Cumulative Atom Count', fontsize=12)
        ax3.set_title('Cumulative Radial Distribution', fontsize=14, fontweight='bold')
        ax3.legend(fontsize=10)
        ax3.grid(True, alpha=0.3)
        
        # 4. Normalized RDF (g(r))
        ax4 = fig.add_subplot(gs[1, 1])
        for element, data in rdf_results.items():
            color = element_colors.get(element, '#000000')
            # Normalize to average bulk density
            avg_density = np.mean(data['densities'][-20:])  # Last 20 points
            if avg_density > 0:
                normalized_rdf = data['densities'] / avg_density
            else:
                normalized_rdf = data['densities']
            ax4.plot(data['radii'], normalized_rdf, 
                    label=f'{element}', linewidth=2, color=color)
        ax4.axhline(y=1.0, color='k', linestyle='--', alpha=0.3, label='Bulk density')
        ax4.set_xlabel('Distance from COM (Å)', fontsize=12)
        ax4.set_ylabel('g(r) (normalized)', fontsize=12)
        ax4.set_title('Normalized Radial Distribution Function', fontsize=14, fontweight='bold')
        ax4.legend(fontsize=10)
        ax4.grid(True, alpha=0.3)
        
        # 5. Distance Distribution Histogram
        ax5 = fig.add_subplot(gs[2, 0])
        for element, data in rdf_results.items():
            color = element_colors.get(element, '#000000')
            ax5.hist(data['raw_distances'], bins=100, alpha=0.5, 
                    label=f'{element}', color=color, density=True)
        ax5.set_xlabel('Distance from COM (Å)', fontsize=12)
        ax5.set_ylabel('Probability Density', fontsize=12)
        ax5.set_title('Distance Distribution Histogram', fontsize=14, fontweight='bold')
        ax5.legend(fontsize=10)
        ax5.grid(True, alpha=0.3)
        
        # 6. Element Composition Bar Chart
        ax6 = fig.add_subplot(gs[2, 1])
        elements = list(rdf_results.keys())
        atom_counts = [len(rdf_results[elem]['raw_distances']) / 
                      len(self.universe.trajectory) for elem in elements]
        colors_list = [element_colors.get(elem, '#000000') for elem in elements]
        ax6.bar(elements, atom_counts, color=colors_list, alpha=0.7, edgecolor='black')
        ax6.set_xlabel('Element', fontsize=12)
        ax6.set_ylabel('Average Atoms per Frame', fontsize=12)
        ax6.set_title('Elemental Composition', fontsize=14, fontweight='bold')
        ax6.grid(True, alpha=0.3, axis='y')
        
        plt.suptitle('Comprehensive Elemental Distribution Analysis', 
                    fontsize=16, fontweight='bold', y=0.995)
          # Save figure
        plot_file = os.path.join(output_dir, 'elemental_distribution_analysis.png')
        plt.savefig(plot_file, dpi=300, bbox_inches='tight')
        print(f"✅ Elemental comparison plot saved to: {plot_file}")
        
        plt.show()
    
    def _save_elemental_summary(self, rdf_results, elements, output_dir="output"):
        """Save a comprehensive text summary of elemental distribution analysis."""
        
        summary_file = os.path.join(output_dir, 'elemental_analysis_summary.txt')
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("ELEMENTAL DISTRIBUTION ANALYSIS SUMMARY\n")
            f.write(f"Author: Bei Chen\n")
            f.write(f"Analysis Date: {pd.Timestamp.now()}\n")
            f.write("="*70 + "\n\n")
            
            f.write(f"Molecular System Information:\n")
            f.write(f"  Total atoms: {self.universe.atoms.n_atoms}\n")
            f.write(f"  Total frames analyzed: {len(self.universe.trajectory)}\n")
            f.write(f"  Time range: {self.universe.trajectory[0].time:.2f} - "
                   f"{self.universe.trajectory[-1].time:.2f} ps\n\n")
            
            f.write("="*70 + "\n")
            f.write("RADIAL DISTRIBUTION STATISTICS BY ELEMENT\n")
            f.write("="*70 + "\n\n")
            
            for element in elements:
                if element in rdf_results:
                    data = rdf_results[element]
                    distances = data['raw_distances']
                    
                    f.write(f"Element: {element}\n")
                    f.write(f"{'-'*50}\n")
                    f.write(f"  Atoms per frame: {len(distances) / len(self.universe.trajectory):.2f}\n")
                    f.write(f"  Average distance from COM: {np.mean(distances):.3f} Å\n")
                    f.write(f"  Standard deviation: {np.std(distances):.3f} Å\n")
                    f.write(f"  Minimum distance: {np.min(distances):.3f} Å\n")
                    f.write(f"  Maximum distance: {np.max(distances):.3f} Å\n")
                    f.write(f"  Median distance: {np.median(distances):.3f} Å\n")
                    
                    # Peak density location
                    peak_idx = np.argmax(data['densities'])
                    f.write(f"  Peak density at: {data['radii'][peak_idx]:.3f} Å "
                           f"({data['densities'][peak_idx]:.6f} atoms/Å³)\n")
                    
                    # Calculate distribution percentiles
                    p25, p50, p75 = np.percentile(distances, [25, 50, 75])
                    f.write(f"  25th percentile: {p25:.3f} Å\n")
                    f.write(f"  50th percentile: {p50:.3f} Å\n")
                    f.write(f"  75th percentile: {p75:.3f} Å\n\n")
            
            f.write("="*70 + "\n")
            f.write("INTERPRETATION GUIDE\n")
            f.write("="*70 + "\n\n")
            f.write("Radial Density Profile:\n")
            f.write("  - Shows how atoms are distributed at different distances from droplet center\n")
            f.write("  - Peak locations indicate preferred atomic shells\n")
            f.write("  - Higher density = more atoms at that distance\n\n")
            
            f.write("Normalized g(r):\n")
            f.write("  - Values > 1: Higher concentration than bulk average\n")
            f.write("  - Values < 1: Lower concentration (depletion)\n")
            f.write("  - Values ≈ 1: Uniform distribution (bulk-like)\n\n")
            
            f.write("Cumulative Distribution:\n")
            f.write("  - Shows total number of atoms within a given radius\n")
            f.write("  - Useful for determining droplet size and structure\n\n")
            
            f.write("="*70 + "\n")
            f.write("FILES GENERATED\n")
            f.write("="*70 + "\n\n")
            f.write("  • rdf_<element>.csv - Radial distribution data for each element\n")
            f.write("  • distances_<element>.txt - Raw distance measurements\n")
            f.write("  • elemental_distribution_analysis.png - Comprehensive plots\n")
            f.write("  • elemental_analysis_summary.txt - This summary file\n\n")
        
        print(f"✅ Analysis summary saved to: {summary_file}")

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
    
    # NEW: Elemental Distribution Analysis
    print(f"\n{'='*60}")
    print("ADVANCED ELEMENTAL & RADIAL DISTRIBUTION ANALYSIS")
    print(f"{'='*60}")
    print("This analysis calculates:")
    print("  • Radial Distribution Functions (RDF)")
    print("  • Elemental density profiles from droplet center")
    print("  • Atomic shell structures")
    print("  • Publication-quality comparison plots")
    print("")
    
    perform_rdf = input("Perform elemental distribution analysis? (y/n): ").lower().strip()
    
    if perform_rdf in ['y', 'yes']:
        # Auto-detect elements or use default
        if hasattr(converter.universe.atoms, 'elements'):
            available_elements = list(np.unique(converter.universe.atoms.elements))
            print(f"\nDetected elements: {', '.join(available_elements)}")
            print(f"Analyzing all detected elements...")
            
            # Perform comprehensive elemental analysis
            rdf_results = converter.calculate_elemental_distribution(
                elements=available_elements,
                max_radius=15.0,
                bins=150,
                save_results=True,
                plot=True,
                output_dir=output_dir
            )
            
            print(f"\n✅ Elemental distribution analysis complete!")
            print(f"\n📁 Generated files:")
            print(f"   • rdf_<element>.csv - Radial distribution data")
            print(f"   • distances_<element>.txt - Raw distance measurements")
            print(f"   • elemental_distribution_analysis.png - Comprehensive plots")
            print(f"   • elemental_analysis_summary.txt - Detailed summary report")
        else:
            print("⚠️  Element information not available in PSF file.")
            print("   Calculating distribution for all atoms combined...")
            
            # Calculate for all atoms
            rdf_data = converter.calculate_radial_distribution(
                element=None,
                max_radius=15.0,
                bins=150,
                save_results=True,
                output_dir=output_dir
            )
            print(f"\n✅ RDF analysis complete!")
            print(f"   Check {output_dir}/ for results")
    
    print(f"\n" + "="*50)
    print("CONVERSION COMPLETE!")
    print(f"All output files saved to: {output_dir}/")
    print("="*50)

if __name__ == "__main__":
    main()
