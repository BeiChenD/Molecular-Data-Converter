# 🧬 Molecular Data Converter

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![MDAnalysis](https://img.shields.io/badge/MDAnalysis-2.0+-green.svg)](https://www.mdanalysis.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Author: Bei Chen**

A comprehensive Python toolkit for converting binary molecular dynamics data formats (.dcd and .psf files) into human-readable XYZ coordinates using MDAnalysis. Perfect for researchers working with CHARMM, NAMD, or other MD simulation data.

## 🚀 Quick Start

### Option 1: Interactive Launcher (Recommended)
```bash
python start_here.py
```

### Option 2: Windows Users
Double-click `START.bat`

### Option 3: Quick Conversion
```bash
python quick_convert.py
```

## 📋 Overview
This project successfully converts binary molecular dynamics data formats (.dcd and .psf files) into human-readable XYZ coordinates using MDAnalysis.

## Files Description

### Input Files
- `H3O_ws.psf` - Protein Structure File (6,953 bytes)
- `H3O_ws_short.dcd` - CHARMM trajectory file (8,480,276 bytes)

### Conversion Scripts
- `convert_molecular_data.py` - Comprehensive conversion with visualization
- `quick_convert.py` - Simple, fast conversion script  
- `simple_converter.py` - Non-interactive converter with plots
- `data_summary.py` - Analysis and summary generator

### Output Files

#### XYZ Format Files
- `converted_frame_0.xyz` - First frame in XYZ format
- `output/first_frame.xyz` - First frame with timestamp
- `output/last_frame.xyz` - Last frame coordinates

#### CSV Format Files  
- `output/first_frame.csv` - Detailed atom data with residue info
- `output/last_frame.csv` - Final frame detailed data

#### Raw Coordinates
- `converted_coordinates.txt` - Simple X,Y,Z coordinates
- `output/coordinates_array.txt` - NumPy formatted coordinates

#### Visualizations
- `output/structure_frame_0.png` - 3D molecular structure plot

## System Information
- **Total atoms**: 64
- **Total frames**: 10,000  
- **Residues**: 21 (H3O and TIP3 water molecules)
- **Time span**: 0.00 - 488.83 picoseconds
- **Coordinate range**: 
  - X: -5.35 to 5.43 Å
  - Y: -4.79 to 5.78 Å  
  - Z: -5.63 to 5.35 Å

## Molecular Composition
This appears to be a hydronium ion (H3O+) in water simulation:
- **H3O**: Hydronium ion
- **TIP3**: TIP3P water model molecules

## Usage Examples

### Quick Conversion
```python
python quick_convert.py
```

### Full Analysis
```python
python convert_molecular_data.py
```

### Generate Summary
```python
python data_summary.py
```

## Viewing the Results

### XYZ Files
XYZ files can be opened with molecular visualization software:
- **VMD** (Visual Molecular Dynamics)
- **PyMOL** 
- **Avogadro**
- **ChemSketch**
- **Jmol**

### CSV Files
CSV files can be opened with:
- **Microsoft Excel**
- **Google Sheets**
- **Python pandas**
- **R statistical software**

## Sample XYZ Data
```
64
Frame 0, Time: 0.00 ps
OH2     -0.696420    -0.383516     0.077792
H1       0.169316    -0.469596     0.549981
H2      -0.693993     0.328154    -0.583137
H3      -1.401284    -0.168756     0.743210
...
```

## Sample CSV Data
```csv
atom_index,x,y,z,atom_name,residue_name,residue_id
0,-0.696420,-0.383516,0.077792,OH2,H3O,1
1,0.169316,-0.469596,0.549981,H1,H3O,1
2,-0.693993,0.328154,-0.583137,H2,H3O,1
...
```

## Dependencies
- **MDAnalysis** (2.10.0) - Molecular dynamics analysis
- **NumPy** (2.4.1) - Numerical computations  
- **Matplotlib** (3.10.8) - Plotting and visualization
- **Pandas** (3.0.0) - Data analysis and CSV export

## Installation
```bash
pip install MDAnalysis numpy matplotlib pandas
```

## Success Metrics
✅ **Binary data successfully converted to readable formats**  
✅ **All 64 atoms coordinates extracted**  
✅ **10,000 trajectory frames accessible**  
✅ **Multiple output formats generated (XYZ, CSV, TXT)**  
✅ **Molecular structure visualization created**  
✅ **No data loss in conversion process**

## Next Steps
1. **Visualize structures** using VMD or PyMOL
2. **Analyze trajectories** with custom Python scripts
3. **Calculate properties** like RDF, diffusion, etc.
4. **Convert to other formats** using Open Babel if needed
5. **Perform statistical analysis** on coordinate data

## Notes
- The warning about DCDReader timesteps is normal and will be fixed in MDAnalysis 3.0
- All coordinate units are in Angstroms (Å)
- Time units are in picoseconds (ps)
- This appears to be a molecular dynamics simulation of hydronium in water

## 🎯 Features

- ✅ **Binary to Text Conversion**: Convert DCD/PSF files to readable formats
- ✅ **Multiple Output Formats**: XYZ, CSV, and TXT files
- ✅ **3D Visualization**: Molecular structure plots with Matplotlib
- ✅ **Trajectory Analysis**: Time-series analysis of molecular dynamics
- ✅ **Interactive Interface**: Auto-detects files and guides users
- ✅ **Cross-Platform**: Works on Windows, macOS, and Linux
- ✅ **Professional Documentation**: Complete setup and usage guides

## 📦 Installation

### Prerequisites
```bash
pip install MDAnalysis numpy matplotlib pandas
```

### Clone Repository
```bash
git clone https://github.com/BeiChenD/Molecular-Data-Converter.git
cd Molecular-Data-Converter
pip install -r requirements.txt
```

## 💻 Usage Examples

### Basic Usage
```python
from convert_molecular_data import MolecularDataConverter

# Convert your files
converter = MolecularDataConverter("your_file.psf", "your_trajectory.dcd")
coordinates = converter.extract_coordinates_frame(0)
converter.save_xyz_format(coordinates, "output.xyz")
```

### Command Line
```bash
# Auto-detect files in directory
python start_here.py

# Quick conversion
python quick_convert.py

# Full analysis with plots
python convert_molecular_data.py
```

## 📁 Project Structure

```
Molecular-Data-Converter/
├── 📄 convert_molecular_data.py    # Main conversion class
├── 🚀 start_here.py               # Interactive launcher
├── ⚡ quick_convert.py             # Fast conversion script
├── 🪟 START.bat                   # Windows double-click launcher
├── 📊 H3O_ws.psf                  # Sample data (PSF file)
├── 📊 H3O_ws_short.dcd            # Sample data (DCD trajectory)
├── 📖 HOW_TO_START.md             # Detailed setup guide
├── 📖 GET_STARTED.md              # Quick start instructions
├── 📖 README.md                   # This file
├── 📝 requirements.txt            # Python dependencies
└── 📁 output/                     # Generated results
    ├── first_frame.xyz
    ├── first_frame.csv
    ├── last_frame.xyz
    ├── last_frame.csv
    └── structure_frame_0.png
```

## 🔬 Sample Data

This repository includes sample molecular dynamics data:
- **H3O_ws.psf**: Hydronium ion in water (PSF topology file)
- **H3O_ws_short.dcd**: 10,000 frame trajectory (488.83 ps simulation)
- **System**: 64 atoms (H3O+ and TIP3P water molecules)

## 📊 Output Formats

### XYZ Format
```
64
Frame 0, Time: 0.00 ps
OH2     -0.696420    -0.383516     0.077792
H1       0.169316    -0.469596     0.549981
...
```

### CSV Format
```csv
atom_index,x,y,z,atom_name,residue_name,residue_id
0,-0.696420,-0.383516,0.077792,OH2,H3O,1
1,0.169316,-0.469596,0.549981,H1,H3O,1
...
```

## 🎨 Visualization

The toolkit creates beautiful 3D molecular structure visualizations:
- Color-coded atoms by element type
- Interactive matplotlib plots
- High-resolution PNG exports
- Trajectory analysis plots

## 🔧 API Reference

### MolecularDataConverter Class

```python
class MolecularDataConverter:
    def __init__(self, psf_file, dcd_file)
    def load_data()
    def extract_coordinates_frame(frame_index=0)
    def extract_all_coordinates()
    def save_xyz_format(coordinates, output_file, frame_index=None)
    def save_csv_format(coordinates, output_file, frame_index=None)
    def visualize_structure(frame_index=0, save_plot=True)
    def analyze_trajectory(save_analysis=True)
```

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: MDAnalysis` | `pip install MDAnalysis` |
| `File not found` | Ensure PSF/DCD files are in correct directory |
| `Permission denied` | Check file permissions and disk space |
| No output files | Script may still be running (large files take time) |

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

**Bei Chen** - Molecular Data Analysis Toolkit

- 📧 Email: [Your Email]
- 🐙 GitHub: [@BeiChenD](https://github.com/BeiChenD)

## 🙏 Acknowledgments

- [MDAnalysis](https://www.mdanalysis.org/) - Excellent molecular dynamics analysis library
- [NumPy](https://numpy.org/) - Fundamental package for scientific computing
- [Matplotlib](https://matplotlib.org/) - Comprehensive plotting library
- [Pandas](https://pandas.pydata.org/) - Data analysis and manipulation tool

---

**⭐ Star this repository if it helped you with your molecular dynamics research!**
