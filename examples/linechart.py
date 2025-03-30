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
