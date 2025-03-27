import gc
import matplotlib.pyplot as plt

from . import analysis, data, plot, uncertainties

class LabTools:
    """
    Unified interface for laboratory data analysis tools.
    
    Provides integrated access to data loading, analysis, visualization,
    and export functionality for scientific data with uncertainties.
    """
    
    def __init__(
            self, 
            foldername=None, filename=None,
            variables=None, equations=None,
            x_label = None, y_label = None, title=None
            ):
        """
        Initialise LabTools with optional configurations.
        
        Parameters:
            filename (str): Input data file (without extensions)
            variables (str): Variables string for data extraction
            equations (str): Equation string for analysis
            title (str): Title for plots
        """
        # Set up directories
        data_directory = data.get_folder_path(foldername)
        
        self.data_directory = data_directory or data.DATA_DIR
        data.ensure_directory(data_directory)
        
        # Store filenames
        self.filename = filename
        self.new_filename = None
        
        # Data storage
        self.unprocessed_data   = None
        self.processed_data     = None

        if x_label is not None and y_label is not None:
            self.extracted_data = {
                'x': None,
                'y': None,
                'x_err': None,
                'y_err': None
            }
        else:
            self.extracted_data = {
                'values': None,
                'uncertainties': None
            }

        self.regression_results = {
            'coefficients' : None,
            'errors' : None,
        }

        # Plot's information
        self.title = title
        self.x_label = x_label
        self.y_label = y_label

        # Variables string for uncertainty propagation
        self.variables = variables

        # Equation(s) string(s) for uncertainty propagation or curve fitting
        if equations is not None and ',' in equations:
            self.equations = equations.split(',')
            self.equation  = None
        else:
            self.equations = equations
            self.equation  = equations
    
    # =========================================================================
    # DATA MANAGEMENT
    # =========================================================================
    
    def load_data(self, sheet_name=0, extension='.xlsx'):
        """
        Load data from file with optional sheet and extension specifications.
        
        Parameters:
            sheet_name (int, str): Sheet to load for Excel files
            extension (str): File extension (e.g. '.xlsx', '.csv')
            
        Returns:
            tuple: Unprocessed data and extracted data with uncertainties
        """
        # Load the appropriate file type
        if extension.lower() in ['.xlsx', '.xls']:
            df = data.load_excel(
                self.filename, sheet_name=sheet_name, extension=extension, directory=self.data_directory
                )
        elif extension.lower() in ['.csv', '.txt']:
            df = data.load_csv(
                self.filename, delimiter=',', extension=extension, directory=self.data_directory
                )
        else:
            raise ValueError(f"Unsupported file type: {extension}")
        self.unprocessed_data = df

        # If specific columns are requested, extract them with uncertainties
        if self.x_label and self.y_label:
            self.x_magnitude = self.x_label.split(' ')[0]
            self.y_magnitude = self.y_label.split(' ')[0]
            if '$' in self.x_magnitude or '$' in self.y_magnitude:
                self.x_magnitude = self.x_magnitude.replace('$','')
                self.y_magnitude = self.y_magnitude.replace('$','')
            
            (x, y), (x_err, y_err) = data.get_excel_data_and_uncertainties(
                f"{self.x_magnitude},{self.y_magnitude}", df
                )
            self.extracted_data = {
                'x': x,
                'y': y,
                'x_err': x_err,
                'y_err': y_err
            }
        
        else:
            values, uncertainties = data.get_excel_data_and_uncertainties(self.variables,df)
            self.extracted_data = {
                'values': values,
                'uncertainties': uncertainties
            }
    
    def unload_data(
            self, processed_data=None, new_filename=None, sheet_names=None,
            processed_mark='_ⓟ', extension='.xlsx'
            ):
        """
        Save data to file new processed file
        
        Parameters:
            processed_data (DataFrame): DataFrame to save
            new_filename (str): Filename to save the data to (optional)
            sheet_names (list): Names of sheets for each DataFrame (for Excel files)
            processed_mark (str): Suffix to add to the processed filename
            extension (str): File extension (e.g. '.xlsx', '.csv')
            
        Returns:
            str: Path to saved file
        """
        if processed_data is not None:
            self.processed_data = processed_data
        if new_filename is not None:
            self.new_filename = new_filename
        else:
            self.new_filename = self.filename + processed_mark
        
        # Save the appropriate file type
        if extension.lower() in ['.xlsx', '.xls']:
            self.results_path = data.unload_excel(
                self.new_filename, self.processed_data, sheet_names=sheet_names, 
                directory=self.data_directory, enhance=True
            )
        elif extension.lower() in ['.csv', '.txt']:
            self.results_path = data.unload_csv(
                self.new_filename, self.processed_data, delimiter=',',
                directory=self.data_directory
            )
        else:
            raise ValueError(f"Unsupported file type: {extension}") 
        
        return self.results_path
    
    # =========================================================================
    # ANALYSIS METHODS
    # =========================================================================
    
    def linear_regression(self):
        """
        Perform linear regression with uncertainty analysis.
        
        Returns:
            dict: Regression results with coefficients, uncertainties, and formula
        """
        vals = self.extracted_data
        self.regression_results =  analysis.linear_regression(
            vals['x'], vals['y'], vals['x_err'], vals['y_err']
        )
        
        self.regression_results['formula'] = analysis.linear_format_formula(
            self.regression_results['coefficients'],
            self.regression_results['errors'],
            self.x_magnitude, self.y_magnitude
            )
    
    def polynomial_regression(self, degree=3):
        """
        Perform polynomial regression with uncertainty analysis.
        
        Parameters:
            degree (int): Polynomial degree
            
        Returns:
            dict: Regression results with coefficients, uncertainties, and formula
        """
        vals = self.extracted_data
        self.regression_results = analysis.polynomial_regression(
            vals['x'], vals['y'], vals['x_err'], vals['y_err'], degree
        )
        self.regression_results['formula'] = analysis.polynomial_format_formula(
            self.regression_results['coefficients'],
            self.regression_results['errors'],
            self.x_magnitude, self.y_magnitude
            )
    
    def curve_regression(self, function, initial_params=None, fit_type=0):
        """
        Perform custom curve regression with uncertainty analysis.
        
        Parameters:
            function (callable): Function to fit, of form f(params, x) -> y
            initial_params (list): Initial parameter estimates
            fit_type (int): Type of fit (0=explicit ODR, 2=OLS)
            
        Returns:
            dict: Regression results with parameters, uncertainties, and formula
        """
        vals = self.extracted_data
        self.regression_results = analysis.curve_regression(
            vals['x'], vals['y'], vals['x_err'], vals['y_err'],
            function, initial_params, fit_type
        )
        self.regression_results['formula'] = None
        # analysis.curve_format_formula(
        #     self.regression_results['parameters'],
        #     self.regression_results['errors'],
        #     self.variables, self.equation
        #     )

        print(self.regression_results)
    
    def apply_formula(self, dependency='Independent'):
        """
        Apply multiple formulas to the loaded data and calculate values with uncertainties.
        
        Parameters:
            equations (str, list): List of formula equations or comma-separated equations
            dependency (str, list): 'Dependent' or 'Independent' variables
                
        Returns:
            tuple: (computed_dataframe, summary_dataframe)
        """
        if self.unprocessed_data is None:
            raise ValueError("No data loaded. Call load_data() first.")
        
        # Apply formulas to the dataframe
        computed_df, summary_df = analysis.apply_formulas_to_dataframe(
            self.unprocessed_data, 
            self.variables, 
            self.equations, 
            dependency
        )
        
        # Store the computed data
        self.processed_data = computed_df
    
        return computed_df, summary_df
    
    def calculate_statistics(self, variable, values, uncertainties, expected_value=None):
        """
        Calculate statistics for data with uncertainties.
        
        Parameters:
            variable (str): Variable name
            values (array-like): Data values
            uncertainties (array-like): Data uncertainties
            expected_value (float): Expected value (optional)
            
        Returns:
            dict: Statistics including mean, standard deviation, and relative uncertainties
        """
        return analysis.calculate_statistics(variable, values, uncertainties, expected_value)
    
    # =========================================================================
    # VISUALIZATION METHODS
    # =========================================================================
    
    def plot_regression(self, save=True, close=True):
        """
        Plot regression results.
        
        Parameters:
            save (bool): Whether to save the plot
            
        Returns:
            tuple: Matplotlib figure and axis objects
        """
        vals = self.extracted_data

        if 'r' in self.regression_results:
            fig, ax = plot.plot_linear_regression(
                vals['x'], vals['y'], vals['x_err'], vals['y_err'],
                self.regression_results,
                self.x_label, self.y_label, self.title,
                save, directory=self.data_directory
            )
        
        elif 'poly_model' in self.regression_results:
            fig, ax = plot.plot_polynomial_regression(
                vals['x'], vals['y'], vals['x_err'], vals['y_err'],
                self.regression_results,
                self.x_label, self.y_label, self.title,
                save, directory=self.data_directory
            )
        
        elif 'function' in self.regression_results:
            fig, ax = plot.plot_curve_regression(
                vals['x'], vals['y'], vals['x_err'], vals['y_err'],
                self.regression_results,
                self.x_label, self.y_label, self.title,
                save, directory=self.data_directory
            )
        
        else:
            raise ValueError("Regression results not found")
        
        if close:
            plt.show()
            plt.close(fig)
        else:
            self.fig, self.ax = fig, ax
    
    def plot_multiple_regressions(
            self, datasets, legend_title=None, subtitles=None, 
            log_xscale=False, log_yscale=False,
            save=True, close=True
            ):
        """
        Plot multiple datasets together.
        
        Parameters:
            datasets (list): List of (x, y, x_err, y_err) tuples
            legend_title (str): Title for the legend (optional)
            subtitles (list): Labels for each dataset (optional)
            log_xscale (bool): Whether to use log scale for x-axis
            log_yscale (bool): Whether to use log scale for y-axis
            
        Returns:
            tuple: Matplotlib figure and axis objects
        """
        fig, ax = plot.plot_multiple_regressions(
            datasets, self.title, legend_title, subtitles, 
            self.x_label, self.y_label, log_xscale, log_yscale,
            save, directory=self.data_directory
        )
        
        if close:
            plt.show()
            plt.close(fig)
        else:
            self.fig, self.ax = fig, ax
    
    # =========================================================================
    # UTILITY METHODS
    # =========================================================================

    def propagate_uncertainty(self, values, uncerts, dependency='Independent'):
        """
        Calculate results with uncertainty propagation.
        
        Parameters:
            dependency (str): 'Dependent' or 'Independent' variables
            
        Returns:
            tuple: Result values and uncertainties
        """
        
        if '=' in self.equation:
            _, expression = self.equation.replace(' ', '').split('=')
        else:
            expression = self.equation

        # Access dictionary values properly instead of unpacking
        
        if isinstance(values, (int, float)):
            values = [[values]]
            uncerts = [[uncerts]]
            result, uncertainty = uncertainties.propagate_uncertainty(
                self.variables, expression, values, uncerts, dependency
                )
            # return result[0], uncertainty[0]
            return result, uncertainty
        else:
            return uncertainties.propagate_uncertainty(
                self.variables, expression, values, uncerts, dependency
                )
    
    def get_latex_equations(self, dependency='Independent', print_latex=False):
        """
        Generate LaTeX representations of formula and uncertainty.
        
        Parameters:
            dependency (str): 'Dependent' or 'Independent' variables
            print_latex (bool): Whether to print the LaTeX code
            
        Returns:
            tuple: Result name, formula LaTeX, and uncertainty LaTeX
        """
        return uncertainties.get_latex_equations(
            self.variables, self.equation, dependency, print_latex
            )
    
    def rounder(self, value, uncertainty):
        """
        Round value with its uncertainty.
        
        Parameters:
            value (float or iterable): Value(s) to round
            uncertainty (float or iterable): Uncertainty(ies) to round
            
        Returns:
            str or list: Formatted string "value ± uncertainty"
        """
        return uncertainties.rounder(value, uncertainty)
    
    # =========================================================================
    # MEMORY MANAGEMENT
    # =========================================================================

    def cleanup(self):
        """
        Release memory by clearing large data objects and collecting garbage.
        Call this method when you're done with a LabTools instance.
        """
        # Clear large data structures
        self.unprocessed_data = None
        self.processed_data = None
        self.extracted_data = None
        self.regression_results = None
        
        # Force garbage collection
        gc.collect()
    
    def __enter__(self):
        """Enter the context manager."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context manager and clean up resources."""
        self.cleanup()