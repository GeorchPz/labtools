# LabTools

A comprehensive Python library for scientific data analysis with uncertainty propagation.

## Overview

LabTools is an integrated toolkit for handling experimental data in scientific laboratories. It provides a streamlined workflow for:

- Loading and processing data with uncertainties
- Performing various types of regression (linear, polynomial, and custom curves)
- Propagating uncertainties through mathematical expressions
- Visualizing data with proper error representation
- Exporting results to Excel and CSV formats

The package is designed with a focus on proper uncertainty handling throughout the entire data analysis process.

## Dependencies

- numpy
- pandas
- matplotlib
- scipy
- sympy
- openpyxl
- xlsxwriter

## Example Usage

The package includes an example that demonstrate its capabilities. One key example is the **Decay** module, which shows how to:

- Load data from radioactive decay experiments
- Apply linear and exponential curve fitting with uncertainty propagation
- Visualize decay curves with proper uncertainty bands
- Calculate half-life values with uncertainties

You can find this example in the `Decay.ipynb` notebook and the related files in the `decay` directory.

## Features

### Data Management

- Load from Excel, CSV and other formats
- Extract data with their associated uncertainties
- Export processed data with properly formatted uncertainties

### Analysis Capabilities

- **Linear Regression**: Weighted and unweighted regression with uncertainty analysis
- **Polynomial Regression**: Fit polynomials of any degree with proper error propagation
- **Custom Curve Fitting**: Orthogonal distance regression for arbitrary functions
- **Uncertainty Propagation**: Apply formulas to data with proper error propagation
- **Statistical Analysis**: Calculate means, standard deviations with uncertainty weighting

### Visualization

- Error bars on data points
- Uncertainty bands on regression curves
- Multiple regression comparison plots
- LaTeX-formatted labels and equations

## Documentation

### Core Class : `LabTools`

The main interface that unifies all functionality:

```python
lab = LabTools(
    foldername=None,        # Directory for data files (optional)
    filename=None,          # Input data file (without extension)
    variables=None,         # Variables in comma-separated format
    equations=None,         # Formula equations
    x_label=None,           # X-axis label for plots
    y_label=None,           # Y-axis label for plots 
    title=None              # Plot title
)
```

### Common Workflows

#### Linear Regression Analysis

```python
# Initialize with experiment details
lab = LabTools(
    filename="pendulum_data",
    x_label="Length (m)",
    y_label="Period² (s²)",
    title="Pendulum Period vs Length"
)

# Load and analyze data
lab.load_data()
lab.linear_regression()

# Display results
print(f"Slope: {lab.regression_results['coefficients'][1]} ± {lab.regression_results['errors'][1]}")
print(f"Correlation coefficient: {lab.regression_results['r']}")

# Visualize and save
lab.plot_regression()
```

#### Uncertainty Propagation

```python
# Calculate acceleration from force and mass with uncertainties
lab = LabTools(
    filename="force_measurements",
    variables="F,m",
    equations="a = F/m"
)

# Load data and apply formula
lab.load_data()
computed_df, summary = lab.apply_formula()

# Export results
lab.unload_data(new_filename="acceleration_results")
```

#### Custom Curve Fitting

```python
import numpy as np

# Define fitting function
def exponential_decay(params, x):
    amplitude, decay_constant = params
    return amplitude * np.exp(-decay_constant * x)

# Setup analysis
lab = LabTools(
    filename="decay_data",
    x_label="Time (s)",
    y_label="Activity (Bq)",
    title="Radioactive Decay"
)

# Load data and fit curve
lab.load_data()
lab.curve_regression(
    function=exponential_decay,
    initial_params=[100, 0.1]
)

# Visualize results
lab.plot_regression()
```

## License

MIT License