# 🧬 Quick Start Guide for Molecular Data Conversion

**Author: Bei Chen**

## If you have PSF and DCD files, here's how to start:

### 🚀 **Method 1: Super Simple Start**
Just run the starter script:
```bash
python start_here.py
```
The script will:
- ✅ Automatically find your PSF/DCD files
- ✅ Guide you through the conversion process  
- ✅ Give you options for quick or detailed conversion

### 🏃‍♂️ **Method 2: Quick Conversion**
For fast, basic conversion:
```bash
python quick_convert.py
```
This creates:
- `converted_frame_0.xyz` - First frame coordinates
- `converted_coordinates.txt` - Raw coordinate array

### 🔬 **Method 3: Full Analysis**
For comprehensive conversion with plots:
```bash
python convert_molecular_data.py
```
This creates:
- Multiple XYZ and CSV files
- 3D molecular structure plots
- Trajectory analysis graphs

## 📋 **Prerequisites**
Make sure you have the required packages:
```bash
pip install MDAnalysis numpy matplotlib pandas
```

## 📁 **File Requirements**
- **PSF file**: Protein Structure File (topology)
- **DCD file**: CHARMM trajectory file (coordinates)

## 🎯 **What You'll Get**
After conversion, you'll have:
- **XYZ files**: For molecular visualization software (VMD, PyMOL, Avogadro)
- **CSV files**: For spreadsheet analysis (Excel, Google Sheets)  
- **TXT files**: Raw coordinates for custom analysis
- **PNG plots**: 3D molecular structure images

## 💡 **Example Usage**
```bash
# 1. Copy your PSF and DCD files to this directory
# 2. Run the starter:
python start_here.py

# Or run directly:
python quick_convert.py
python convert_molecular_data.py
```

## 🆘 **Troubleshooting**
- **"MDAnalysis not found"**: Run `pip install MDAnalysis`
- **"File not found"**: Make sure PSF/DCD files are in the same directory
- **"Permission denied"**: Check file permissions and disk space

## 📊 **Output Examples**
- `your_file_converted.xyz` - Standard molecular format
- `output_your_file/first_frame.csv` - Detailed coordinate data
- `output_your_file/structure_frame_0.png` - 3D visualization

**Start with `python start_here.py` for the easiest experience! 🚀**
