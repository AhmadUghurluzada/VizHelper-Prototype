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
