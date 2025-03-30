# VizHelper

VizHelper is a lightweight Python module that enhances Matplotlib visualizations by applying user-centered design improvements. It declutters plots, applies a colorblind-friendly palette, auto-rotates x-axis labels, auto-generates legends and labels, produces descriptive alt-text (using heuristics or, optionally, the OpenAI API), and enables interactive hover tooltips.

VizHelper is designed for both novice and advanced users, making it easy to create accessible, readable, and well-formatted plots with minimal extra code.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
  - [Local Installation](#local-installation)
  - [Installing from PyPI](#installing-from-pypi)
- [Usage Examples](#usage-examples)
  - [Example 1: Bar Chart](#example-1-bar-chart)
  - [Example 2: Scatter Plot](#example-2-scatter-plot)
  - [Example 3: Line Chart](#example-3-line-chart)
- [Before and After Comparison](#before-and-after-comparison)
- [Detailed Functionality](#detailed-functionality)
  - [enhance_plot()](#enhance_plot)
  - [User Profiles](#user-profiles)
  - [Auto-Rotation of X-Axis Labels](#auto-rotation-of-x-axis-labels)
  - [Alt-Text Generation](#alt-text-generation)
  - [Interactivity](#interactivity)
- [Configuration Options](#configuration-options)
- [Future Work](#future-work)
- [Contact](#contact)

## Overview

VizHelper enhances Matplotlib plots by:
- **Decluttering:** Removing extra spines and adjusting tick parameters.
- **Accessibility:** Applying a colorblind-friendly palette by default.
- **Dynamic Label Rotation:** Automatically rotates x-axis labels based on the number of categories.
- **Auto-Legend & Auto-Labeling:** Generating legends and labeling data points (bar heights or line endpoints).
- **Alt-Text Generation:** Creating descriptive alt-text for plots using heuristics or (optionally) the OpenAI API.
- **Interactivity:** Enabling hover tooltips for interactive data inspection.
- **Configurable Settings:** Allowing users to customize default behaviors and user profiles.

## Features

- **Decluttering:**  
  Removes top and right spines to create a cleaner look.
  
- **Color Accessibility:**  
  Uses a colorblind-friendly palette to improve readability.

- **Dynamic Label Rotation:**  
  Automatically rotates x-axis labels (0°, 45°, or 90°) based on the number of categories.

- **Auto-Legend & Auto-Labeling:**  
  Automatically generates legends (if labels are provided) and auto-labels bars (displaying heights) or line endpoints.

- **Alt-Text Generation:**  
  - **Heuristic-based:** Provides basic, context-aware descriptions based on the plot type.  
  - **AI-powered (Optional):** Uses the OpenAI API for detailed alt-text if an API key is supplied.
  
- **Interactivity:**  
  Enables hover tooltips using mplcursors for additional data insights.

- **User Profiles & Customization:**  
  Supports user profiles such as `"colorblind"`, `"visually_impaired"`, and `"novice"`, with configuration options for further customization.

## Installation

### Local Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YourUsername/vizhelper.git
   
2. **Navigate to the project directory:**
    ```bash
    cd vizhelper

3. **Create and activate a virtual environment:**
    ```bash
    python -m venv env
    
    # On Windows:
    env\Scripts\activate
    
    # On macOS/Linux:
    source env/bin/activate

4. **Install the package in editable mode:**
    ```bash
    pip install -e .
    
    
### Installing from PyPI
Users can install VizHelper via pip:   
    
    pip install vizhelper


## Usage Examples
**Example 1: Bar Chart**  
This example demonstrates how to create a simple bar chart and enhance it with VizHelper.

    import pandas as pd
    import matplotlib.pyplot as plt
    from vizhelper.enhance import enhance_plot

    def main():
        # Load the dataset
        data = pd.read_csv("data/SampleSuperstore.csv")
        
        # Aggregate the sales by sub-category
        subcategory_sales = data.groupby("Sub-Category")["Sales"].sum()
        
        # Create a figure and Axes object
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # Plot the bar chart (we no longer set xticks rotation manually)
        subcategory_sales.plot(kind="bar", color="red", ax=ax)
        ax.set_title("Sales by Sub-Category")
        ax.set_xlabel("Sub-Category")
        ax.set_ylabel("Sales")
        
        # Enhance the plot with VizHelper (auto-rotation will apply if needed)
        enhance_plot(
            ax,
            interactive=True,
            user_profile="colorblind",
            auto_legend=False,
            auto_label=True,
            openai_api_key=None  # Replace with your key if desired
        )
        
        plt.show()

    if __name__ == "__main__":
        main()




**Example 2: Scatter Plot**  
This example shows how to create a simple scatter plot with synthetic data and apply VizHelper enhancements.

    import numpy as np
    import matplotlib.pyplot as plt
    from vizhelper.enhance import enhance_plot
    
    def main():
        # Generate synthetic data for the scatter plot
        np.random.seed(0)
        x = np.linspace(0, 10, 50)
        y = np.sin(x) + np.random.normal(0, 0.5, 50)
        
        # Create the scatter plot
        fig, ax = plt.subplots(figsize=(8, 6))
        scatter = ax.scatter(x, y, c=x, cmap="viridis", alpha=0.7)
        fig.colorbar(scatter, ax=ax, label="X Value")
        ax.set_title("Sample Scatter Plot")
        ax.set_xlabel("X Value")
        ax.set_ylabel("Y Value")
        
        # Enhance the plot with VizHelper (disable auto-labeling for scatter)
        enhance_plot(
            ax,
            interactive=True,
            user_profile="colorblind",
            auto_legend=False,
            auto_label=False,
            openai_api_key=None,
            config={"auto_rotate_labels": False},
        )
        
        plt.show()
    
    if __name__ == "__main__":
        main()
        
**Example 3: Line Chart**  
This example illustrates how to create a simple line chart using generated data and enhance it with VizHelper.

    import numpy as np
    import matplotlib.pyplot as plt
    from vizhelper.enhance import enhance_plot
    
    def main():
        # Generate synthetic data for a line chart
        x = np.arange(0, 12)
        y = np.random.randint(5, 20, size=12)
        
        # Create the line chart
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(x, y, marker="o", linestyle="-", label="Monthly Data")
        ax.set_title("Sample Line Chart")
        ax.set_xlabel("Month")
        ax.set_ylabel("Value")
        
        # Enhance the plot with VizHelper
        enhance_plot(
            ax,
            interactive=True,
            user_profile="colorblind",
            auto_legend=True,
            auto_label=True,
            openai_api_key=None,
        )
        
        plt.show()
    
    if __name__ == "__main__":
        main()



## Before and After Comparison
The following images demonstrate the difference between a default Matplotlib plot and the enhanced plot using VizHelper. The "after" image is result of Example 1 code shown above:

**Before Enhancement**:  
![before](screenshots/before.png)

**After Enhancement**:  
![after](screenshots/after.png)    

The result in terminal:
        
    Auto-rotating x-axis labels to 90° for 17 categories.
    Auto-labeled bar heights.
    Alt text generated: This is a bar chart displaying data for categories: Accessories, Appliances, Art, Binders, Bookcases, Chairs, Copiers, Envelopes, Fasteners, Furnishings, Labels, Machines, Paper, Phones, Storage, Supplies, Tables.
    Interactive features enabled.
    Enhancing plot with advanced features complete!
## Detailed Functionality

### 1. enhance_plot()
The enhance_plot() function is the primary interface to enhance a given Matplotlib Axes object. It performs the following enhancements:

 - **Decluttering**: Removes unnecessary spines.

 - **Accessibility**: Applies a colorblind-friendly palette.

 - **Dynamic Label Rotation**: Automatically rotates x-axis labels based on the number of categories.

 - **Auto-Legend & Auto-Labeling**: Generates legends and labels data points automatically.

 - **Alt-Text Generation**: Creates descriptive alt-text using heuristics or the OpenAI API (if an API key is provided).

 - **Interactivity**: Enables hover tooltips via mplcursors.

 - **Layout Management**: Adjusts layout with tight_layout().  
        

**Parameters**  
 - **ax**: The Matplotlib Axes to enhance.

 - **interactive**: Boolean flag to enable hover interactivity.

 - **user_profile**: Preset configurations (e.g., "colorblind", "visually_impaired", "novice").

 - **auto_legend**: Automatically add legends if labels exist.

 - **auto_label**: Automatically label bar heights or line endpoints.

 - **openai_api_key**: Optional key to use the OpenAI API for detailed alt-text.

 - **config**: A dictionary of configuration options:

    - "color_palette": List of color codes.

     - "auto_label_fontsize": Font size for auto labels (default: 9).

     - "misleading_yaxis_threshold": Threshold for y-axis (default: 0).

    - "auto_rotate_labels": Automatically rotate x-axis labels (default: True).


### 2. User Profiles
User profiles allow VizHelper to adjust aesthetics based on user needs:

- **"colorblind"**: Applies a colorblind-friendly palette.

- **"visually_impaired"**: Increases font sizes for better readability.

- **"novice"**: Currently does not serve anything, it will be developed in future

### 3. Auto-Rotation of X-Axis Labels
The helper function _auto_label_rotation() automatically rotates x-axis labels based on the number of non-empty labels:

 - More than 10 labels: 90° rotation.

 - More than 5 labels: 45° rotation.

 - Otherwise: 0° rotation. This ensures that labels remain readable without manual configuration.


### 4. Alt-Text Generation
VizHelper generates alt-text in two ways:

 -  **Alt-Text**: Provides a basic description based on the type of chart (bar, pie, or line).

 - **AI-Powered Alt-Text**: Uses the OpenAI API for a more detailed description if an API key is provided. If the API call fails, it falls back to the heuristic method.


### 5. Interactivity
Interactive hover tooltips are enabled using mplcursors, which allows users to inspect data points by hovering over them.


## Configuration Options
The config dictionary supports the following keys:

 - **color_palette**: List of color codes for the plot (default: a colorblind-friendly palette).

 - **auto_label_fontsize**: Font size for auto-generated labels (default: 9).

 - **misleading_yaxis_threshold**: Minimum y-axis value threshold (default: 0).

 - **auto_rotate_labels**: Boolean flag to automatically rotate x-axis labels (default: True).

## Future Work
 - Extend support to additional plot types (e.g., heatmaps, radar charts, 3D plots).

 - Enhance data introspection for richer alt-text descriptions.

 - Optimize performance for very large datasets.

 - Expand configuration options for more granular control.

 - Improve error handling and logging.

 - Develop more refined user profiles.



## Contact
For questions or support, please contact Ahmad Ughurluzada at ughurluzada@gmail.com.
