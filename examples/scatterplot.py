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
