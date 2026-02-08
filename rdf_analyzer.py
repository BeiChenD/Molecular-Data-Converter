#!/usr/bin/env python3
"""
Radial Distribution Function (RDF) Analyzer
==========================================

Specialized tool for calculating radial density profiles and elemental 
distributions in molecular dynamics simulations. Designed for droplet analysis
and NAMD/CHARMM trajectories.

Author: Bei Chen
Date: February 8, 2026
"""

import MDAnalysis as mda
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
import glob

def analyze_droplet_rdf(psf_file, dcd_file, elements_to_analyze=None, 
                        max_radius=15.0, output_dir="rdf_analysis"):
    """
    Complete RDF analysis workflow for droplet systems.
    
    Args:
        psf_file (str): Path to PSF topology file
        dcd_file (str): Path to DCD trajectory file
        elements_to_analyze (list): Elements to analyze (None = auto-detect)
        max_radius (float): Maximum radius for RDF calculation (Angstroms)
        output_dir (str): Output directory for results
    """
    
    print("="*70)
    print("RADIAL DISTRIBUTION FUNCTION (RDF) ANALYZER")
    print("Droplet Analysis Tool for Molecular Dynamics")
    print("Author: Bei Chen")
    print("="*70)
    
    # Load molecular system
    print(f"\n📂 Loading files...")
    print(f"   PSF: {psf_file}")
    print(f"   DCD: {dcd_file}")
    
    try:
        u = mda.Universe(psf_file, dcd_file)
        print(f"✅ Successfully loaded molecular system")
        print(f"   Atoms: {u.atoms.n_atoms}")
        print(f"   Frames: {len(u.trajectory)}")
        print(f"   Time: {u.trajectory[0].time:.2f} - {u.trajectory[-1].time:.2f} ps")
    except Exception as e:
        print(f"❌ Error loading files: {e}")
        return None
    
    # Auto-detect elements
    if elements_to_analyze is None:
        if hasattr(u.atoms, 'elements'):
            elements_to_analyze = list(np.unique(u.atoms.elements))
            print(f"\n🔍 Auto-detected elements: {', '.join(elements_to_analyze)}")
        else:
            print(f"\n⚠️  No element information available")
            print(f"   Will analyze all atoms as a single group")
            elements_to_analyze = ['ALL']
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Calculate RDF for each element
    print(f"\n📊 Calculating Radial Distribution Functions...")
    print(f"   Max radius: {max_radius} Å")
    print(f"   Output: {output_dir}/")
    
    rdf_results = {}
    
    for element in elements_to_analyze:
        print(f"\n--- Analyzing: {element} ---")
        
        # Select atoms
        if element == 'ALL':
            atom_group = u.atoms
        elif hasattr(u.atoms, 'elements'):
            atom_group = u.atoms[u.atoms.elements == element]
        else:
            continue
        
        if len(atom_group) == 0:
            print(f"⚠️  No {element} atoms found, skipping...")
            continue
        
        print(f"   Selected {len(atom_group)} atoms")
        
        # Calculate distances from COM
        all_distances = []
        n_frames = len(u.trajectory)
        
        for frame_idx, ts in enumerate(u.trajectory):
            com = u.atoms.center_of_mass()
            positions = atom_group.positions
            distances = np.linalg.norm(positions - com, axis=1)
            all_distances.extend(distances)
            
            if (frame_idx + 1) % max(1, n_frames // 10) == 0:
                print(f"   Progress: {frame_idx+1}/{n_frames} ({(frame_idx+1)/n_frames*100:.0f}%)")
        
        all_distances = np.array(all_distances)
        
        # Calculate RDF
        bins = 150
        hist, bin_edges = np.histogram(all_distances, bins=bins, range=(0, max_radius))
        radii = (bin_edges[:-1] + bin_edges[1:]) / 2
        
        # Normalize by shell volume
        shell_volumes = (4/3) * np.pi * (bin_edges[1:]**3 - bin_edges[:-1]**3)
        densities = hist / (shell_volumes * n_frames)
        avg_counts = hist / n_frames
        
        # Store results
        rdf_results[element] = {
            'radii': radii,
            'densities': densities,
            'counts': avg_counts,
            'distances': all_distances
        }
        
        # Print statistics
        print(f"   Mean distance: {np.mean(all_distances):.3f} ± {np.std(all_distances):.3f} Å")
        print(f"   Range: {np.min(all_distances):.3f} - {np.max(all_distances):.3f} Å")
        
        # Peak density
        peak_idx = np.argmax(densities)
        print(f"   Peak density at: {radii[peak_idx]:.3f} Å")
        
        # Save CSV
        csv_file = os.path.join(output_dir, f"rdf_{element}.csv")
        df = pd.DataFrame({
            'radius_A': radii,
            'density_per_A3': densities,
            'avg_count_per_frame': avg_counts
        })
        df.to_csv(csv_file, index=False)
        print(f"   ✅ Saved: {csv_file}")
    
    # Generate plots
    print(f"\n🎨 Generating plots...")
    plot_rdf_comparison(rdf_results, output_dir)
    
    # Generate summary report
    print(f"\n📝 Generating summary report...")
    generate_rdf_report(rdf_results, u, output_dir)
    
    print(f"\n{'='*70}")
    print("✅ RDF ANALYSIS COMPLETE!")
    print(f"📁 Results saved to: {output_dir}/")
    print(f"{'='*70}")
    
    return rdf_results

def plot_rdf_comparison(rdf_results, output_dir):
    """Create comprehensive RDF comparison plots."""
    
    colors = {'H': '#1f77b4', 'N': '#ff7f0e', 'O': '#d62728', 
              'C': '#2ca02c', 'ALL': '#000000'}
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # 1. Radial Density
    ax1 = axes[0, 0]
    for elem, data in rdf_results.items():
        color = colors.get(elem, '#888888')
        ax1.plot(data['radii'], data['densities'], label=elem, 
                linewidth=2, color=color)
    ax1.set_xlabel('Distance from COM (Å)', fontsize=11)
    ax1.set_ylabel('Density (atoms/Å³)', fontsize=11)
    ax1.set_title('Radial Density Profile', fontsize=13, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. Average Count per Shell
    ax2 = axes[0, 1]
    for elem, data in rdf_results.items():
        color = colors.get(elem, '#888888')
        ax2.plot(data['radii'], data['counts'], label=elem, 
                linewidth=2, color=color)
    ax2.set_xlabel('Distance from COM (Å)', fontsize=11)
    ax2.set_ylabel('Atoms per Shell', fontsize=11)
    ax2.set_title('Average Count per Radial Shell', fontsize=13, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 3. Cumulative Distribution
    ax3 = axes[1, 0]
    for elem, data in rdf_results.items():
        color = colors.get(elem, '#888888')
        cumulative = np.cumsum(data['counts'])
        ax3.plot(data['radii'], cumulative, label=elem, 
                linewidth=2, color=color)
    ax3.set_xlabel('Distance from COM (Å)', fontsize=11)
    ax3.set_ylabel('Cumulative Atoms', fontsize=11)
    ax3.set_title('Cumulative Radial Distribution', fontsize=13, fontweight='bold')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # 4. Distance Histograms
    ax4 = axes[1, 1]
    for elem, data in rdf_results.items():
        color = colors.get(elem, '#888888')
        ax4.hist(data['distances'], bins=80, alpha=0.5, 
                label=elem, color=color, density=True)
    ax4.set_xlabel('Distance from COM (Å)', fontsize=11)
    ax4.set_ylabel('Probability Density', fontsize=11)
    ax4.set_title('Distance Distribution', fontsize=13, fontweight='bold')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.suptitle('Radial Distribution Function Analysis - Bei Chen', 
                fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    plot_file = os.path.join(output_dir, 'rdf_comparison.png')
    plt.savefig(plot_file, dpi=300, bbox_inches='tight')
    print(f"   ✅ Plot saved: {plot_file}")
    plt.close()

def generate_rdf_report(rdf_results, universe, output_dir):
    """Generate a text summary report."""
    
    report_file = os.path.join(output_dir, 'rdf_analysis_report.txt')
    
    with open(report_file, 'w') as f:
        f.write("="*70 + "\n")
        f.write("RADIAL DISTRIBUTION FUNCTION (RDF) ANALYSIS REPORT\n")
        f.write("="*70 + "\n")
        f.write(f"Author: Bei Chen\n")
        f.write(f"Date: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*70 + "\n\n")
        
        f.write("SYSTEM INFORMATION\n")
        f.write("-" * 50 + "\n")
        f.write(f"Total atoms: {universe.atoms.n_atoms}\n")
        f.write(f"Frames analyzed: {len(universe.trajectory)}\n")
        f.write(f"Time range: {universe.trajectory[0].time:.2f} - "
                f"{universe.trajectory[-1].time:.2f} ps\n\n")
        
        f.write("="*70 + "\n")
        f.write("RESULTS BY ELEMENT\n")
        f.write("="*70 + "\n\n")
        
        for elem, data in rdf_results.items():
            distances = data['distances']
            
            f.write(f"Element: {elem}\n")
            f.write("-" * 50 + "\n")
            f.write(f"  Number of atoms: {len(distances) / len(universe.trajectory):.1f} per frame\n")
            f.write(f"  Mean distance from COM: {np.mean(distances):.3f} Å\n")
            f.write(f"  Standard deviation: {np.std(distances):.3f} Å\n")
            f.write(f"  Min distance: {np.min(distances):.3f} Å\n")
            f.write(f"  Max distance: {np.max(distances):.3f} Å\n")
            f.write(f"  Median distance: {np.median(distances):.3f} Å\n")
            
            # Peak information
            peak_idx = np.argmax(data['densities'])
            f.write(f"  Peak density: {data['densities'][peak_idx]:.6f} atoms/Å³\n")
            f.write(f"  Peak location: {data['radii'][peak_idx]:.3f} Å\n")
            
            # Percentiles
            p25, p50, p75 = np.percentile(distances, [25, 50, 75])
            f.write(f"  Distribution: 25%={p25:.2f}, 50%={p50:.2f}, 75%={p75:.2f} Å\n\n")
        
        f.write("="*70 + "\n")
        f.write("INTERPRETATION\n")
        f.write("="*70 + "\n")
        f.write("• Radial Density: Shows atom concentration vs distance from center\n")
        f.write("• Peak locations indicate preferred atomic shells/layers\n")
        f.write("• Cumulative plot shows total atoms within given radius\n")
        f.write("• Useful for determining droplet size and structure\n\n")
        
        f.write("FILES GENERATED\n")
        f.write("-" * 50 + "\n")
        f.write("• rdf_<element>.csv - Numerical RDF data\n")
        f.write("• rdf_comparison.png - Comparative plots\n")
        f.write("• rdf_analysis_report.txt - This report\n")
    
    print(f"   ✅ Report saved: {report_file}")

def main():
    """Main function for standalone RDF analysis."""
    
    print("\n" + "="*70)
    print("RDF ANALYZER - Standalone Tool")
    print("="*70)
    
    # Auto-detect files
    psf_files = glob.glob("*.psf")
    dcd_files = glob.glob("*.dcd")
    
    if not psf_files or not dcd_files:
        print("❌ No PSF/DCD files found in current directory")
        print("\nUsage:")
        print("  python rdf_analyzer.py")
        print("  (Place PSF and DCD files in the same directory)")
        return
    
    psf_file = psf_files[0] if len(psf_files) == 1 else input(f"Select PSF file {psf_files}: ")
    dcd_file = dcd_files[0] if len(dcd_files) == 1 else input(f"Select DCD file {dcd_files}: ")
    
    # Run analysis
    analyze_droplet_rdf(psf_file, dcd_file)

if __name__ == "__main__":
    main()
