#!/usr/bin/env python3
"""Simple immediate function test"""
import sys
sys.stdout.flush()

print("=" * 70, flush=True)
print("TESTING ALL FUNCTIONS - IMMEDIATE OUTPUT", flush=True)
print("=" * 70, flush=True)

try:
    from convert_molecular_data import MolecularDataConverter
    print("\n✅ TEST 1: Import successful", flush=True)
    
    print("\n✅ TEST 2: Loading files...", flush=True)
    converter = MolecularDataConverter("H3O_ws.psf", "H3O_ws_short.dcd")
    print(f"   Loaded {converter.universe.atoms.n_atoms} atoms, {len(converter.universe.trajectory)} frames", flush=True)
    
    print("\n✅ TEST 3: get_system_info()", flush=True)
    converter.get_system_info()
    
    print("\n✅ TEST 4: extract_coordinates_frame()", flush=True)
    coords = converter.extract_coordinates_frame(0)
    print(f"   Shape: {coords.shape}", flush=True)
    
    print("\n✅ TEST 5: save_xyz_format()", flush=True)
    import os
    os.makedirs("test_out", exist_ok=True)
    converter.save_xyz_format(coords, "test_out/test.xyz", 0)
    
    print("\n✅ TEST 6: save_csv_format()", flush=True)
    converter.save_csv_format(coords, "test_out/test.csv", 0)
    
    print("\n✅ TEST 7: visualize_structure()", flush=True)
    import matplotlib
    matplotlib.use('Agg')
    converter.visualize_structure(0, True, "test_out")
    
    print("\n✅ TEST 8: analyze_trajectory() [100 frames]", flush=True)
    orig_traj = converter.universe.trajectory
    converter.universe.trajectory = orig_traj[:100]
    converter.analyze_trajectory(True, "test_out")
    converter.universe.trajectory = orig_traj
    
    print("\n✅ TEST 9: calculate_radial_distribution() [50 frames]", flush=True)
    converter.universe.trajectory = orig_traj[:50]
    import numpy as np
    if hasattr(converter.universe.atoms, 'elements'):
        elem = np.unique(converter.universe.atoms.elements)[0]
        print(f"   Element: {elem}", flush=True)
        rdf = converter.calculate_radial_distribution(elem, 10.0, 30, True, "test_out")
    else:
        rdf = converter.calculate_radial_distribution(None, 10.0, 30, True, "test_out")
    converter.universe.trajectory = orig_traj
    
    print("\n✅ TEST 10: calculate_elemental_distribution() [30 frames]", flush=True)
    converter.universe.trajectory = orig_traj[:30]
    if hasattr(converter.universe.atoms, 'elements'):
        elems = list(np.unique(converter.universe.atoms.elements))[:2]
        print(f"   Elements: {elems}", flush=True)
        results = converter.calculate_elemental_distribution(elems, 8.0, 30, True, True, "test_out")
    converter.universe.trajectory = orig_traj
    
    print("\n✅ TEST 11: _plot_elemental_comparison()", flush=True)
    mock = {'T': {'radii': np.linspace(0,10,20), 'densities': np.random.rand(20)*0.01, 
                  'counts': np.random.rand(20)*5, 'raw_distances': np.random.rand(50)*10}}
    converter._plot_elemental_comparison(mock, "test_out")
    
    print("\n✅ TEST 12: _save_elemental_summary()", flush=True)
    converter._save_elemental_summary(mock, ['T'], "test_out")
    
    print("\n" + "=" * 70, flush=True)
    print("🎉 ALL 12 FUNCTIONS TESTED SUCCESSFULLY!", flush=True)
    print("=" * 70, flush=True)
    
    print("\nGenerated test files in test_out/:", flush=True)
    for f in os.listdir("test_out"):
        print(f"  • {f}", flush=True)
    
except Exception as e:
    print(f"\n❌ ERROR: {e}", flush=True)
    import traceback
    traceback.print_exc()
    sys.exit(1)
