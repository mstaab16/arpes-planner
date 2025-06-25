# ARPES Planner

A web-based planning tool for Angle-Resolved Photoemission Spectroscopy (ARPES) experiments. This app helps researchers visualize and plan their ARPES measurements by calculating momentum coordinates for different analyzer angles and sample orientations.

## Public web version
Try it out at [arpes-planner.matthewstaab.com](https://arpes-planner.matthewstaab.com) if you don't want to install it locally.

## What is ARPES?

Angle-Resolved Photoemission Spectroscopy (ARPES) is a powerful technique used to study the electronic structure of materials. It measures the energy and momentum of electrons emitted from a sample when illuminated with photons, giving us direct insight into the band structure and Fermi surface.

## What can this app do?

![Example Demonstration](./assets/demo.gif)

- **Interactive 3D Visualization**: See momentum coordinates in both absolute and projected (first Brillouin zone) views
- **Real-time Updates**: Change parameters and watch the results update instantly
- **Full Parameter Control**: 
  - Photon energy, work function, and inner potential
  - Sample orientation and alignment offsets
  - Analyzer slit and deflector angle ranges
  - Crystal structure via reciprocal lattice vectors
- **Data Export**: Download your calculated coordinates as CSV files
- **Helpful Tooltips**: Hover over any parameter for a quick explanation

## When would you use this?

- **Planning experiments**: Figure out the best analyzer angles for specific momentum regions
- **Sample alignment**: Plan how to orient and align your sample
- **Understanding data**: See how analyzer angles relate to momentum space
- **Teaching**: Great for visualizing ARPES coordinate transformations

## Getting Started

1. **Install the requirements**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app**:
   ```bash
   python app.py
   ```

3. **Open your browser** to `http://localhost:8050`

## Key Parameters Explained

- **Photon Energy**: Energy of the photons hitting your sample (usually 10-100 eV)
- **Work Function**: Energy needed to pull electrons off the surface
- **Inner Potential**: Material property that affects electron final states
- **Sample Normal**: Direction of normal emission in crystal coordinates
- **Reciprocal Lattice Vectors**: Define your crystal structure (b1, b2, b3)

## What you'll see

The app creates two 3D plots:
- **Absolute Coordinates**: Raw momentum coordinates in Å⁻¹
- **Projected Coordinates**: Coordinates folded into the first Brillouin zone

Both plots show you how analyzer angles map to momentum space, making it much easier to plan your ARPES measurements.

## Made by

[Matthew Staab](https://github.com/mstaab16)

## License

Open source under the MIT License - feel free to use and modify!
