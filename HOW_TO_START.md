# 🧬 COMPLETE SETUP GUIDE - Bei Chen

## 🎯 **If you have PSF or DCD files, follow these steps:**

### **Step 1: Setup**
1. **Place your files**: Copy your `.psf` and `.dcd` files into this directory
2. **Install packages**: Run this command:
   ```powershell
   pip install MDAnalysis numpy matplotlib pandas
   ```

### **Step 2: Choose Your Method**

#### 🚀 **EASIEST - Auto-detect files:**
```powershell
python start_here.py
```
- Automatically finds your PSF/DCD files
- Guides you through the process
- Asks what type of conversion you want

#### 🏃‍♂️ **QUICK - Basic conversion:**
```powershell
python quick_convert.py
```
- Fast conversion of first frame
- Creates `.xyz` and `.txt` files
- Perfect for quick visualization

#### 🔬 **FULL - Complete analysis:**
```powershell
python convert_molecular_data.py
```
- Comprehensive conversion with plots
- Creates multiple output formats
- Includes trajectory analysis

### **Step 3: View Results**

Your converted files will be saved as:
- **XYZ files**: Open with VMD, PyMOL, Avogadro, ChemSketch
- **CSV files**: Open with Excel, Google Sheets
- **TXT files**: Raw coordinates for custom analysis
- **PNG images**: 3D molecular structure plots

## 📋 **File Structure Example**
```
Your Directory/
├── your_molecule.psf      ← Your input files
├── your_trajectory.dcd    ← Your input files
├── start_here.py          ← Run this first!
├── quick_convert.py       ← For quick conversion
├── convert_molecular_data.py  ← For full analysis
└── output/                ← Results appear here
    ├── first_frame.xyz
    ├── first_frame.csv
    ├── last_frame.xyz
    ├── last_frame.csv
    └── structure_frame_0.png
```

## 🔧 **Customizing for Different Files**

If your files have different names, you can:

1. **Edit the file names** in the scripts, or
2. **Rename your files** to match the expected names:
   - `H3O_ws.psf` and `H3O_ws_short.dcd`

## 💻 **Command Examples**
```powershell
# Method 1: Let the script find your files
python start_here.py

# Method 2: Quick conversion (works with H3O_ws files)
python quick_convert.py

# Method 3: Full conversion (works with H3O_ws files)  
python convert_molecular_data.py
```

## 🆘 **Troubleshooting**
- **"ModuleNotFoundError"**: Install packages with `pip install MDAnalysis numpy matplotlib pandas`
- **"File not found"**: Make sure your PSF/DCD files are in the same directory
- **No output**: Check if the script is still running (might take time for large files)

## ✅ **Success Indicators**
You'll know it worked when you see:
- ✅ "System loaded successfully!"
- ✅ "XYZ coordinates saved to: ..."
- ✅ "CONVERSION COMPLETE!"
- ✅ New files in the output folder

## 📊 **What You Get**
- **Readable coordinates** instead of binary data
- **Multiple formats** for different software
- **3D visualizations** of your molecular structure
- **Trajectory analysis** (if using full converter)

**🎉 Start with `python start_here.py` for the best experience!**

---
*Created by Bei Chen - Molecular Data Conversion Tools*
