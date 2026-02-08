# 🔬 Radial Distribution Function (RDF) Analysis Guide

**Author: Bei Chen**  
**Date: February 8, 2026**

## 📖 Overview

This guide explains how to use the advanced RDF analysis features for molecular dynamics simulations, particularly for **droplet analysis** with **NAMD/CHARMM** trajectories.

## 🎯 What is RDF Analysis?

Radial Distribution Function (RDF) analysis shows **how atoms are distributed at different distances from a reference point** (typically the droplet center/center of mass).

### Key Questions RDF Answers:
- ✅ Where are specific elements concentrated in my droplet?
- ✅ What is the shell structure of my molecular system?
- ✅ How do Nitrogen, Hydrogen, and Oxygen distribute differently?
- ✅ What is the effective radius of my droplet?
- ✅ Are there preferred atomic layers or shells?

## 🚀 Quick Start

### Method 1: Integrated Analysis
```bash
python convert_molecular_data.py
# When prompted: "Perform elemental distribution analysis? (y/n):" type 'y'
```

### Method 2: Standalone RDF Tool  
```bash
python rdf_analyzer.py
# Auto-detects PSF and DCD files in current directory
```

### Method 3: Python API
```python
from convert_molecular_data import MolecularDataConverter

# Load your system
converter = MolecularDataConverter("system.psf", "trajectory.dcd")

# Analyze all elements
rdf_results = converter.calculate_elemental_distribution(
    elements=['N', 'H', 'O'],  # Specify elements or None for auto-detect
    max_radius=15.0,            # Maximum distance to analyze (Angstroms)
    bins=150,                    # Number of histogram bins
    save_results=True,           # Save CSV and TXT files
    plot=True,                   # Generate plots
    output_dir="rdf_output"      # Output directory
)

# Access results programmatically
for element, data in rdf_results.items():
    print(f"{element}: Peak at {data['radii'][data['densities'].argmax()]:.2f} Å")
```

## 📊 Understanding PSF and DCD Files

### The Relationship
- **PSF (Protein Structure File)**: The "identity card"
  - Contains atom names (N, H, C, O)
  - Includes atom masses and charges
  - Defines molecular connectivity (bonds)
  - **NO coordinates** - only topology

- **DCD (Binary Trajectory)**: The "movie"
  - Contains raw X, Y, Z coordinates for each frame
  - **NO labels** - doesn't know which atom is which
  - Binary format for efficiency

### How They Work Together:
```python
import MDAnalysis as mda

# PSF provides labels, DCD provides positions
u = mda.Universe("topology.psf", "trajectory.dcd")

# Now MDAnalysis knows:
# - Which coordinates belong to Nitrogen
# - Which belong to Hydrogen  
# - How they're connected
```

**Key Point**: You typically have:
- ✅ ONE PSF file (topology doesn't change)
- ✅ MULTIPLE DCD files (run1.dcd, run2.dcd, etc.)

## 📈 Output Files Explained

### 1. **rdf_<element>.csv**
Numerical data for each element's radial distribution.

**Columns:**
- `radius_angstrom`: Distance from center of mass (Å)
- `density_per_angstrom3`: Atomic density at that radius (atoms/Å³)
- `avg_count_per_frame`: Average number of atoms in that shell per frame
- `total_counts`: Total measurements in that shell across all frames
- `shell_volume_angstrom3`: Volume of the spherical shell

**Use for:** Quantitative analysis, plotting custom graphs, statistical tests

### 2. **distances_<element>.txt**
Raw distance measurements for every atom in every frame.

**Format:** One distance per line (in Angstroms)

**Use for:** Custom analysis, distribution fitting, advanced statistics

### 3. **elemental_distribution_analysis.png**
Comprehensive 6-panel visualization:

1. **Radial Density Profile**: Density vs distance
2. **Average Count per Shell**: Number of atoms per shell
3. **Cumulative Distribution**: Total atoms within radius
4. **Normalized g(r)**: Standard RDF (values > 1 = enrichment, < 1 = depletion)
5. **Distance Histogram**: Probability distribution  
6. **Elemental Composition**: Bar chart of average atoms per frame

**Use for:** Publications, presentations, quick visual analysis

### 4. **elemental_analysis_summary.txt**
Detailed statistical report including:
- Mean, median, std deviation of distances
- Peak density locations
- Percentile distributions (25%, 50%, 75%)
- Atom counts per frame
- Interpretation guide

**Use for:** Reporting results, documentation, understanding data

## 🔍 Interpreting Results

### Radial Density Profile

```
High peak at small radius → Core/center concentration
Multiple peaks → Distinct atomic shells/layers
Gradual increase → Diffuse distribution
Plateau at large r → Bulk-like behavior
```

### Normalized g(r)

```
g(r) > 1.0 → Higher concentration than average (enrichment)
g(r) < 1.0 → Lower concentration (depletion)  
g(r) ≈ 1.0 → Uniform distribution (bulk-like)
Sharp peaks → Well-defined structure
Smooth curve → Disordered system
```

### Cumulative Distribution

```
Steep rise → Most atoms concentrated in that region
Inflection point → Characteristic droplet radius
Final plateau → Total number of atoms of that element
```

## 💡 Common Analysis Scenarios

### Scenario 1: Hydronium Ion (H3O+) in Water

**Question**: "Where is the hydronium ion located relative to water molecules?"

**Analysis**:
```python
converter = MolecularDataConverter("h3o_water.psf", "simulation.dcd")
rdf_results = converter.calculate_elemental_distribution(elements=['H', 'O'])
```

**Look for**:
- Different peak locations for H vs O
- Enrichment/depletion in normalized g(r)
- Cumulative counts to estimate solvation shell

### Scenario 2: Nitrogen Distribution in Droplet

**Question**: "How does Nitrogen distribute from droplet center?"

**Analysis**:
```python
rdf_n = converter.calculate_radial_distribution(element='N', max_radius=20.0)
```

**Examine**:
- Peak density location (core vs surface)
- Standard deviation (spread of distribution)  
- Cumulative plot (total N within radius)

### Scenario 3: Comparing Multiple Elements

**Question**: "Do different elements prefer different regions?"

**Analysis**:
```python
rdf_multi = converter.calculate_elemental_distribution(elements=['N', 'H', 'O', 'C'])
```

**Compare**:
- Relative peak positions
- Peak heights (concentrations)
- Cumulative curves (spatial ordering)

## 🎨 Customizing Analysis

### Adjust Radius Range
```python
# For small droplets
rdf = converter.calculate_elemental_distribution(max_radius=10.0)

# For large systems
rdf = converter.calculate_elemental_distribution(max_radius=30.0)
```

### Change Resolution
```python
# Higher resolution (more bins)
rdf = converter.calculate_elemental_distribution(bins=300)

# Faster calculation (fewer bins)
rdf = converter.calculate_elemental_distribution(bins=50)
```

### Select Specific Frames
```python
# Analyze only last 1000 frames (equilibrated portion)
u = mda.Universe("system.psf", "trajectory.dcd")
u.trajectory = u.trajectory[-1000:]
converter = MolecularDataConverter("system.psf", "trajectory.dcd")
```

## 📐 Mathematical Background

### Radial Density Calculation

```
ρ(r) = N(r) / (V_shell * N_frames)

Where:
- N(r) = number of atoms at radius r
- V_shell = 4/3 * π * (r_outer³ - r_inner³)
- N_frames = number of trajectory frames
```

### Normalized g(r)

```
g(r) = ρ(r) / ρ_bulk

Where:
- ρ(r) = local density at radius r
- ρ_bulk = average bulk density (typically from outer shells)
```

## 🔧 Troubleshooting

### Problem: "No element information available"
**Solution**: PSF file doesn't contain element data. Analysis will use all atoms as one group.

### Problem: "Peak at radius 0"
**Cause**: Center of mass calculation issue or very small system
**Solution**: Check that system has >1 atom and verify coordinates

### Problem: "Flat RDF curve"
**Cause**: max_radius too small or system is very uniform
**Solution**: Increase `max_radius` parameter or check system equilibration

### Problem: "Noisy RDF curve"
**Cause**: Too few frames or too many bins
**Solution**: Analyze more frames or reduce `bins` parameter

## 📚 References & Further Reading

### MDAnalysis Documentation
- [Universe](https://docs.mdanalysis.org/stable/documentation_pages/core/universe.html)
- [Trajectory Analysis](https://docs.mdanalysis.org/stable/documentation_pages/core/groups.html)

### RDF Theory
- Allen & Tildesley, "Computer Simulation of Liquids" (Chapter 2)
- Frenkel & Smit, "Understanding Molecular Simulation" (Chapter 4)

### NAMD/CHARMM
- [NAMD User Guide](https://www.ks.uiuc.edu/Research/namd/current/ug/)
- [CHARMM Documentation](https://www.charmm.org/charmm/documentation/)

## 💬 Support

For issues or questions:
1. Check this guide first
2. Review the generated `elemental_analysis_summary.txt`
3. Open an issue on GitHub: https://github.com/BeiChenD/Molecular-Data-Converter

---

**🎉 Happy Analyzing! Your droplet structure awaits discovery!**

*Bei Chen - Molecular Data Conversion Tools*
