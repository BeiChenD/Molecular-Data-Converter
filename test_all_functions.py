#!/usr/bin/env python3
"""
Comprehensive Function Testing Script
=====================================

This script tests every function in the MolecularDataConverter class
with the H3O_ws.psf and H3O_ws_short.dcd files.

Author: Bei Chen
Date: February 8, 2026
"""

import os
import sys
import traceback
from convert_molecular_data import MolecularDataConverter
import numpy as np

def print_section(title):
    """Print a formatted section header."""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def print_test(test_name, status="RUNNING"):
    """Print test status."""
    symbols = {"RUNNING": "🔄", "PASSED": "✅", "FAILED": "❌", "SKIPPED": "⏭️"}
    print(f"\n{symbols.get(status, '•')} TEST: {test_name} [{status}]")

def run_test(test_func, test_name):
    """Run a test function and handle exceptions."""
    print_test(test_name, "RUNNING")
    try:
        test_func()
        print_test(test_name, "PASSED")
        return True
    except Exception as e:
        print_test(test_name, "FAILED")
        print(f"   Error: {str(e)}")
        traceback.print_exc()
        return False

class FunctionTester:
    """Class to test all functions of MolecularDataConverter."""
    
    def __init__(self, psf_file, dcd_file):
        """Initialize tester with test files."""
        self.psf_file = psf_file
        self.dcd_file = dcd_file
        self.test_output_dir = "test_output"
        self.converter = None
        self.passed_tests = 0
        self.failed_tests = 0
        self.total_tests = 0
        
        # Create test output directory
        os.makedirs(self.test_output_dir, exist_ok=True)
    
    def test_initialization(self):
        """Test 1: MolecularDataConverter initialization."""
        self.converter = MolecularDataConverter(self.psf_file, self.dcd_file)
        assert self.converter is not None, "Converter object not created"
        assert self.converter.universe is not None, "Universe not loaded"
        print(f"   ✓ Converter initialized successfully")
        print(f"   ✓ Universe loaded: {self.converter.universe.atoms.n_atoms} atoms")
    
    def test_load_data(self):
        """Test 2: load_data() method."""
        # Already tested in initialization, but verify attributes
        assert hasattr(self.converter, 'psf_file'), "PSF file attribute missing"
        assert hasattr(self.converter, 'dcd_file'), "DCD file attribute missing"
        assert hasattr(self.converter, 'universe'), "Universe attribute missing"
        print(f"   ✓ PSF file: {self.converter.psf_file}")
        print(f"   ✓ DCD file: {self.converter.dcd_file}")
        print(f"   ✓ Frames: {len(self.converter.universe.trajectory)}")
    
    def test_get_system_info(self):
        """Test 3: get_system_info() method."""
        print(f"   Calling get_system_info()...")
        self.converter.get_system_info()
        print(f"   ✓ System info displayed successfully")
    
    def test_extract_coordinates_frame(self):
        """Test 4: extract_coordinates_frame() method."""
        # Test first frame
        coords_first = self.converter.extract_coordinates_frame(0)
        assert coords_first is not None, "First frame coordinates are None"
        assert coords_first.shape[0] > 0, "No atoms in coordinates"
        assert coords_first.shape[1] == 3, "Coordinates don't have 3 dimensions"
        print(f"   ✓ First frame extracted: shape {coords_first.shape}")
        
        # Test middle frame
        mid_frame = len(self.converter.universe.trajectory) // 2
        coords_mid = self.converter.extract_coordinates_frame(mid_frame)
        assert coords_mid is not None, "Middle frame coordinates are None"
        print(f"   ✓ Middle frame ({mid_frame}) extracted: shape {coords_mid.shape}")
        
        # Test last frame
        last_frame = len(self.converter.universe.trajectory) - 1
        coords_last = self.converter.extract_coordinates_frame(last_frame)
        assert coords_last is not None, "Last frame coordinates are None"
        print(f"   ✓ Last frame ({last_frame}) extracted: shape {coords_last.shape}")
        
        # Verify coordinates are different between frames
        assert not np.allclose(coords_first, coords_last), "First and last frames identical"
        print(f"   ✓ Frames contain different coordinates (trajectory is dynamic)")
    
    def test_extract_all_coordinates(self):
        """Test 5: extract_all_coordinates() method."""
        print(f"   Extracting all frames (this may take a moment)...")
        all_coords = self.converter.extract_all_coordinates()
        
        n_frames = len(self.converter.universe.trajectory)
        n_atoms = self.converter.universe.atoms.n_atoms
        
        assert all_coords is not None, "All coordinates are None"
        assert all_coords.shape[0] == n_frames, f"Expected {n_frames} frames, got {all_coords.shape[0]}"
        assert all_coords.shape[1] == n_atoms, f"Expected {n_atoms} atoms, got {all_coords.shape[1]}"
        assert all_coords.shape[2] == 3, "Coordinates don't have 3 dimensions"
        
        print(f"   ✓ All frames extracted: shape {all_coords.shape}")
        print(f"   ✓ {n_frames} frames × {n_atoms} atoms × 3 coordinates")
    
    def test_save_xyz_format(self):
        """Test 6: save_xyz_format() method."""
        coords = self.converter.extract_coordinates_frame(0)
        
        # Test with frame index
        output_file1 = os.path.join(self.test_output_dir, "test_frame_0.xyz")
        self.converter.save_xyz_format(coords, output_file1, frame_index=0)
        assert os.path.exists(output_file1), "XYZ file not created"
        
        # Verify file contents
        with open(output_file1, 'r') as f:
            lines = f.readlines()
            assert len(lines) > 2, "XYZ file too short"
            n_atoms = int(lines[0].strip())
            assert n_atoms == len(coords), f"Atom count mismatch: {n_atoms} vs {len(coords)}"
        
        print(f"   ✓ XYZ file created: {output_file1}")
        print(f"   ✓ File contains {n_atoms} atoms")
        
        # Test without frame index
        output_file2 = os.path.join(self.test_output_dir, "test_no_frame.xyz")
        self.converter.save_xyz_format(coords, output_file2)
        assert os.path.exists(output_file2), "XYZ file (no frame) not created"
        print(f"   ✓ XYZ file (no frame index) created: {output_file2}")
    
    def test_save_csv_format(self):
        """Test 7: save_csv_format() method."""
        coords = self.converter.extract_coordinates_frame(0)
        
        # Test CSV export
        output_file = os.path.join(self.test_output_dir, "test_frame_0.csv")
        self.converter.save_csv_format(coords, output_file, frame_index=0)
        assert os.path.exists(output_file), "CSV file not created"
        
        # Verify CSV contents
        import pandas as pd
        df = pd.read_csv(output_file)
        assert len(df) == len(coords), "CSV row count mismatch"
        assert 'x' in df.columns, "CSV missing 'x' column"
        assert 'y' in df.columns, "CSV missing 'y' column"
        assert 'z' in df.columns, "CSV missing 'z' column"
        
        print(f"   ✓ CSV file created: {output_file}")
        print(f"   ✓ CSV contains {len(df)} rows with columns: {list(df.columns)}")
    
    def test_visualize_structure(self):
        """Test 8: visualize_structure() method."""
        print(f"   Creating 3D visualization (plot will display)...")
        
        # Test with save_plot=True (don't show to avoid blocking)
        import matplotlib
        matplotlib.use('Agg')  # Use non-interactive backend
        
        self.converter.visualize_structure(
            frame_index=0, 
            save_plot=True, 
            output_dir=self.test_output_dir
        )
        
        plot_file = os.path.join(self.test_output_dir, "structure_frame_0.png")
        assert os.path.exists(plot_file), "Structure plot not created"
        print(f"   ✓ Structure visualization saved: {plot_file}")
        
        # Verify file is not empty
        file_size = os.path.getsize(plot_file)
        assert file_size > 1000, f"Plot file too small ({file_size} bytes)"
        print(f"   ✓ Plot file size: {file_size / 1024:.1f} KB")
    
    def test_analyze_trajectory(self):
        """Test 9: analyze_trajectory() method."""
        print(f"   Analyzing trajectory (this may take a moment)...")
        
        # Use non-interactive backend
        import matplotlib
        matplotlib.use('Agg')
        
        self.converter.analyze_trajectory(
            save_analysis=True,
            output_dir=self.test_output_dir
        )
        
        analysis_file = os.path.join(self.test_output_dir, "trajectory_analysis.png")
        assert os.path.exists(analysis_file), "Trajectory analysis plot not created"
        print(f"   ✓ Trajectory analysis saved: {analysis_file}")
        
        # Verify file is not empty
        file_size = os.path.getsize(analysis_file)
        assert file_size > 1000, f"Analysis file too small ({file_size} bytes)"
        print(f"   ✓ Analysis file size: {file_size / 1024:.1f} KB")
    
    def test_calculate_radial_distribution(self):
        """Test 10: calculate_radial_distribution() method."""
        print(f"   Calculating RDF (this may take a moment)...")
        
        # Test with specific element if available
        if hasattr(self.converter.universe.atoms, 'elements'):
            elements = np.unique(self.converter.universe.atoms.elements)
            test_element = elements[0] if len(elements) > 0 else None
            
            if test_element:
                print(f"   Testing with element: {test_element}")
                rdf_data = self.converter.calculate_radial_distribution(
                    element=test_element,
                    max_radius=15.0,
                    bins=100,
                    save_results=True,
                    output_dir=self.test_output_dir
                )
                
                # Verify RDF data structure
                assert 'radii' in rdf_data, "RDF data missing 'radii'"
                assert 'densities' in rdf_data, "RDF data missing 'densities'"
                assert 'counts' in rdf_data, "RDF data missing 'counts'"
                assert 'raw_distances' in rdf_data, "RDF data missing 'raw_distances'"
                
                print(f"   ✓ RDF calculated for {test_element}")
                print(f"   ✓ Radii array shape: {rdf_data['radii'].shape}")
                print(f"   ✓ Densities array shape: {rdf_data['densities'].shape}")
                print(f"   ✓ Raw distances count: {len(rdf_data['raw_distances'])}")
                
                # Verify CSV files created
                csv_file = os.path.join(self.test_output_dir, f"rdf_{test_element}.csv")
                assert os.path.exists(csv_file), f"RDF CSV not created for {test_element}"
                print(f"   ✓ RDF CSV saved: {csv_file}")
        
        # Test with all atoms
        print(f"   Testing with all atoms...")
        rdf_all = self.converter.calculate_radial_distribution(
            element=None,
            max_radius=10.0,
            bins=50,
            save_results=True,
            output_dir=self.test_output_dir
        )
        
        assert rdf_all is not None, "RDF for all atoms returned None"
        print(f"   ✓ RDF calculated for all atoms")
    
    def test_calculate_elemental_distribution(self):
        """Test 11: calculate_elemental_distribution() method."""
        print(f"   Calculating elemental distribution (this may take time)...")
        
        # Use non-interactive backend
        import matplotlib
        matplotlib.use('Agg')
        
        # Test with auto-detected elements
        if hasattr(self.converter.universe.atoms, 'elements'):
            elements = list(np.unique(self.converter.universe.atoms.elements))
            print(f"   Auto-detected elements: {elements}")
            
            # Limit to first 2 elements for faster testing
            test_elements = elements[:2] if len(elements) >= 2 else elements
            print(f"   Testing with elements: {test_elements}")
            
            rdf_results = self.converter.calculate_elemental_distribution(
                elements=test_elements,
                max_radius=12.0,
                bins=80,
                save_results=True,
                plot=True,
                output_dir=self.test_output_dir
            )
            
            assert rdf_results is not None, "Elemental distribution returned None"
            assert len(rdf_results) > 0, "No results in elemental distribution"
            
            print(f"   ✓ Elemental distribution calculated for {len(rdf_results)} elements")
            
            # Verify all elements processed
            for elem in test_elements:
                assert elem in rdf_results, f"Element {elem} not in results"
                print(f"   ✓ Element {elem} processed successfully")
            
            # Verify plot created
            plot_file = os.path.join(self.test_output_dir, "elemental_distribution_analysis.png")
            assert os.path.exists(plot_file), "Elemental distribution plot not created"
            print(f"   ✓ Distribution plot saved: {plot_file}")
            
            # Verify summary file
            summary_file = os.path.join(self.test_output_dir, "elemental_analysis_summary.txt")
            assert os.path.exists(summary_file), "Summary file not created"
            print(f"   ✓ Summary report saved: {summary_file}")
        else:
            print(f"   ⚠️  No element information available - skipping elemental test")
    
    def test_plot_elemental_comparison(self):
        """Test 12: _plot_elemental_comparison() method (private)."""
        print(f"   Testing private plotting method...")
        
        # Use non-interactive backend
        import matplotlib
        matplotlib.use('Agg')
        
        # Create mock RDF results
        mock_rdf = {
            'TEST': {
                'radii': np.linspace(0, 10, 50),
                'densities': np.random.rand(50) * 0.01,
                'counts': np.random.rand(50) * 10,
                'raw_distances': np.random.rand(1000) * 10
            }
        }
        
        self.converter._plot_elemental_comparison(mock_rdf, self.test_output_dir)
        
        plot_file = os.path.join(self.test_output_dir, "elemental_distribution_analysis.png")
        assert os.path.exists(plot_file), "Comparison plot not created"
        print(f"   ✓ Private plotting method works")
    
    def test_save_elemental_summary(self):
        """Test 13: _save_elemental_summary() method (private)."""
        print(f"   Testing private summary method...")
        
        # Create mock RDF results
        mock_rdf = {
            'TEST': {
                'radii': np.linspace(0, 10, 50),
                'densities': np.random.rand(50) * 0.01,
                'counts': np.random.rand(50) * 10,
                'raw_distances': np.random.rand(1000) * 10
            }
        }
        
        self.converter._save_elemental_summary(mock_rdf, ['TEST'], self.test_output_dir)
        
        summary_file = os.path.join(self.test_output_dir, "elemental_analysis_summary.txt")
        assert os.path.exists(summary_file), "Summary file not created by private method"
        
        # Verify file contents
        with open(summary_file, 'r') as f:
            content = f.read()
            assert 'TEST' in content, "Element name not in summary"
            assert 'Bei Chen' in content, "Author not in summary"
        
        print(f"   ✓ Private summary method works")
    
    def run_all_tests(self):
        """Run all tests sequentially."""
        print_section("COMPREHENSIVE FUNCTION TESTING")
        print(f"PSF File: {self.psf_file}")
        print(f"DCD File: {self.dcd_file}")
        print(f"Test Output: {self.test_output_dir}/")
        
        # List of all tests
        tests = [
            (self.test_initialization, "Initialization & Constructor"),
            (self.test_load_data, "load_data() Method"),
            (self.test_get_system_info, "get_system_info() Method"),
            (self.test_extract_coordinates_frame, "extract_coordinates_frame() Method"),
            (self.test_extract_all_coordinates, "extract_all_coordinates() Method"),
            (self.test_save_xyz_format, "save_xyz_format() Method"),
            (self.test_save_csv_format, "save_csv_format() Method"),
            (self.test_visualize_structure, "visualize_structure() Method"),
            (self.test_analyze_trajectory, "analyze_trajectory() Method"),
            (self.test_calculate_radial_distribution, "calculate_radial_distribution() Method"),
            (self.test_calculate_elemental_distribution, "calculate_elemental_distribution() Method"),
            (self.test_plot_elemental_comparison, "_plot_elemental_comparison() Private Method"),
            (self.test_save_elemental_summary, "_save_elemental_summary() Private Method"),
        ]
        
        # Run each test
        for test_func, test_name in tests:
            self.total_tests += 1
            if run_test(test_func, test_name):
                self.passed_tests += 1
            else:
                self.failed_tests += 1
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary."""
        print_section("TEST SUMMARY")
        
        print(f"\n📊 Results:")
        print(f"   Total Tests:  {self.total_tests}")
        print(f"   ✅ Passed:    {self.passed_tests}")
        print(f"   ❌ Failed:    {self.failed_tests}")
        print(f"   Success Rate: {(self.passed_tests/self.total_tests*100):.1f}%")
        
        print(f"\n📁 Test Output Location:")
        print(f"   {os.path.abspath(self.test_output_dir)}/")
        
        print(f"\n📝 Generated Test Files:")
        if os.path.exists(self.test_output_dir):
            files = os.listdir(self.test_output_dir)
            for file in sorted(files):
                file_path = os.path.join(self.test_output_dir, file)
                size = os.path.getsize(file_path)
                print(f"   • {file} ({size:,} bytes)")
        
        if self.failed_tests == 0:
            print(f"\n{'='*70}")
            print("🎉 ALL TESTS PASSED! 🎉")
            print("All functions are working correctly with your PSF and DCD files.")
            print(f"{'='*70}")
        else:
            print(f"\n{'='*70}")
            print("⚠️  SOME TESTS FAILED")
            print("Please review the error messages above for details.")
            print(f"{'='*70}")

def main():
    """Main function to run comprehensive tests."""
    
    # File paths
    psf_file = "H3O_ws.psf"
    dcd_file = "H3O_ws_short.dcd"
    
    # Check if files exist
    if not os.path.exists(psf_file):
        print(f"❌ Error: PSF file '{psf_file}' not found!")
        print(f"   Current directory: {os.getcwd()}")
        return 1
    
    if not os.path.exists(dcd_file):
        print(f"❌ Error: DCD file '{dcd_file}' not found!")
        print(f"   Current directory: {os.getcwd()}")
        return 1
    
    # Run tests
    tester = FunctionTester(psf_file, dcd_file)
    tester.run_all_tests()
    
    # Return exit code
    return 0 if tester.failed_tests == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
