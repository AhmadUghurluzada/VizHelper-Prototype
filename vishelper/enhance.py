import matplotlib as mpl
import matplotlib.pyplot as plt
import statistics



# MAIN ENHANCE FUNCTION 

def enhance_plot(
    ax,
    interactive=False,
    user_profile=None,
    auto_legend=True,
    auto_label=True,
    openai_api_key=None,
    config=None,
):
    """
    Enhances a Matplotlib Axes object by applying readability, accessibility,
    design improvements, and advanced features.

    Parameters:
        ax : matplotlib.axes.Axes
            The Axes object to enhance.
        interactive : bool
            Enable hover interactivity (via mplcursors).
        user_profile : str or dict
            Special settings for certain users (e.g., 'colorblind',
            'visually_impaired').
        auto_legend : bool
            Automatically generate or improve legends.
        auto_label : bool
            Auto-label bar heights or line endpoints.
        openai_api_key : str
            If provided, use the OpenAI API for richer alt-text.
        config : dict
            A dictionary of configuration options. Default values include:
              - 'color_palette': list of colors
              - 'auto_label_fontsize': 9
              - 'misleading_yaxis_threshold': 0 (i.e., y_min must be <= 0)
              - 'auto_rotate_labels': True
    """
    default_config = {
        "color_palette": [
            "#377eb8",
            "#ff7f00",
            "#4daf4a",
            "#f781bf",
            "#a65628",
            "#984ea3",
            "#999999",
            "#e41a1c",
            "#dede00",
        ],
        "auto_label_fontsize": 9,
        "misleading_yaxis_threshold": 0,
        "auto_rotate_labels": True,
    }
    if config is None:
        config = default_config
    else:
        for key, value in default_config.items():
            config.setdefault(key, value)

    _apply_user_profile(ax, user_profile, config)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    _check_misleading(ax, config)
    _auto_label_rotation(ax, config)
    if auto_legend:
        _auto_legend(ax)
    if auto_label:
        _auto_label(ax, config)
    alt_text = generate_alt_text(
        ax, openai_api_key=openai_api_key, config=config
    )
    print("Alt text generated:", alt_text)
    ax.alt_text = alt_text
    if interactive:
        _enable_interactive(ax)
    ax.figure.tight_layout()
    print("Enhancing plot with advanced features complete!")



# USER PROFILE ADJUSTMENTS   

def _apply_user_profile(ax, user_profile, config):
    """
    Adjust settings based on the user profile.
    """
    if not user_profile:
        return
    if isinstance(user_profile, str):
        profile = user_profile.lower()
        if profile == "colorblind":
            _apply_colorblind_palette(ax, config)
        elif profile == "visually_impaired":
            plt.rcParams.update({"font.size": 14})
            _apply_colorblind_palette(ax, config)
        elif profile == "novice":
            pass
        else:
            _apply_colorblind_palette(ax, config)
    elif isinstance(user_profile, dict):
        if user_profile.get("colorblind", False):
            _apply_colorblind_palette(ax, config)
        if user_profile.get("large_font", False):
            plt.rcParams.update(
                {"font.size": user_profile.get("font_size", 14)}
            )




# MISLEADING DESIGN CHECKS 

def _check_misleading(ax, config):
    y_min, _ = ax.get_ylim()
    if y_min > config.get("misleading_yaxis_threshold", 0):
        print(
            "[Warning] Y-axis does not start at 0. This can exaggerate "
            "differences."
        )
    pie_patches = [
        p for p in ax.get_children() if isinstance(p, mpl.patches.Wedge)
    ]
    if pie_patches:
        total_angle = sum((w.theta2 - w.theta1) for w in pie_patches)
        if abs(total_angle - 360) > 5:
            print(
                f"[Warning] Pie chart wedges sum to {total_angle:.1f}°, "
                "which is off from 360°."
            )
        if len(pie_patches) > 10:
            print(
                "[Warning] Pie chart has many slices, which can be confusing."
            )




# AUTO LEGEND & AUTO-LABELING  

def _auto_legend(ax):
    handles, labels = ax.get_legend_handles_labels()
    if labels and not ax.get_legend():
        ax.legend()
        print("Auto-legend created.")


def _auto_label(ax, config):
    bars = [
        p
        for p in ax.get_children()
        if isinstance(p, mpl.patches.Rectangle) and p.get_width() != 0
    ]
    if bars:
        fontsize = config.get("auto_label_fontsize", 9)
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                x = bar.get_x() + bar.get_width() / 2
                y = height
                ax.text(
                    x,
                    y,
                    f"{height:.1f}",
                    ha="center",
                    va="bottom",
                    fontsize=fontsize,
                )
        print("Auto-labeled bar heights.")
    lines = ax.get_lines()
    for line in lines:
        label = line.get_label()
        if label and not label.startswith("_"):
            xdata, ydata = line.get_xdata(), line.get_ydata()
            ax.text(
                xdata[-1],
                ydata[-1],
                label,
                va="bottom",
                ha="left",
                fontsize=config.get("auto_label_fontsize", 9),
            )
    if lines:
        print("Auto-labeled line endpoints.")



# COLOR ACCESSIBILITY

def _apply_colorblind_palette(ax, config):
    palette = config.get("color_palette")
    color_index = 0
    for artist in ax.get_children():
        if (
            isinstance(artist, mpl.patches.Rectangle)
            and artist.get_x() != 0
        ):
            artist.set_facecolor(palette[color_index % len(palette)])
            color_index += 1
        elif isinstance(artist, mpl.lines.Line2D):
            artist.set_color(palette[color_index % len(palette)])
            color_index += 1



# AUTO-ROTATE X-AXIS LABELS
# if number of catgeories is more than 10, it rotates 90 and in between 5-10, it rototes 

def _auto_label_rotation(ax, config):
    if not config.get("auto_rotate_labels", False):
        return
    xticks = [tick.get_text() for tick in ax.get_xticklabels() if tick.get_text()]
    n_categories = len(xticks)
    if n_categories > 10:
        rotation = 90
    elif n_categories > 5:
        rotation = 45
    else:
        rotation = 0
    ax.tick_params(axis="x", which="major", labelrotation=rotation)
    print(
        f"Auto-rotating x-axis labels to {rotation}° for "
        f"{n_categories} categories."
    )



# ALT-TEXT GENERATION

def generate_alt_text(ax, openai_api_key=None, config=None):
    if config is None:
        config = {}
    if openai_api_key:
        alt = _generate_ai_alt_text(ax, openai_api_key, config)
        if alt:
            return alt
    return _generate_heuristic_alt_text(ax, config)



def _generate_heuristic_alt_text(ax, config):
    import matplotlib as mpl

    pie_wedges = [
        p for p in ax.get_children() if isinstance(p, mpl.patches.Wedge)
    ]
    if pie_wedges:
        return (
            "This is a pie chart displaying proportions of different "
            "categories."
        )
    bars = [
        p
        for p in ax.get_children()
        if isinstance(p, mpl.patches.Rectangle) and p.get_width() != 0
    ]
    if bars:
        xticks = ax.get_xticklabels()
        categories = [tick.get_text() for tick in xticks if tick.get_text()]
        if categories:
            return (
                "This is a bar chart displaying data for categories: "
                + ", ".join(categories)
                + "."
            )
        else:
            return "This is a bar chart displaying multiple data points."
    lines = ax.get_lines()
    if lines:
        trends = []
        for line in lines:
            ydata = line.get_ydata()
            if len(ydata) > 1:
                trend = ("increasing" if ydata[-1] > ydata[0]
                         else "decreasing")
                trends.append(trend)
        if trends:
            return (
                "This is a line chart showing a generally "
                + ", ".join(trends)
                + " trend over time."
            )
        return "This is a line chart showing trends over time."
    return "This is a visualization."



def _generate_ai_alt_text(ax, api_key, config):
    import openai
    openai.api_key = api_key
    chart_type = "unknown"
    info = ""
    bars = [
        p
        for p in ax.get_children()
        if isinstance(p, mpl.patches.Rectangle) and p.get_width() != 0
    ]
    if bars:
        chart_type = "bar"
        xticks = ax.get_xticklabels()
        categories = [tick.get_text() for tick in xticks if tick.get_text()]
        values = [bar.get_height() for bar in bars]
        if values:
            total = sum(values)
            avg = round(statistics.mean(values), 2)
            min_val = min(values)
            max_val = max(values)
            try:
                max_index = values.index(max_val)
                min_index = values.index(min_val)
                highest_cat = (
                    categories[max_index]
                    if max_index < len(categories)
                    else "Unknown"
                )
                lowest_cat = (
                    categories[min_index]
                    if min_index < len(categories)
                    else "Unknown"
                )
            except Exception:
                highest_cat, lowest_cat = "Unknown", "Unknown"
            info = (
                f"This bar chart has {len(categories)} categories: "
                f"{', '.join(categories)}. The highest value is {max_val} "
                f"for category '{highest_cat}', and the lowest is {min_val} "
                f"for '{lowest_cat}'. The total sum is {total} and the average "
                f"is {avg}. "
            )
    else:
        if any(isinstance(p, mpl.patches.Wedge)
               for p in ax.get_children()):
            chart_type = "pie"
            info = "This is a pie chart."
        elif ax.get_lines():
            chart_type = "line"
            trends = []
            for line in ax.get_lines():
                ydata = line.get_ydata()
                if len(ydata) > 1:
                    trend = (
                        "increasing" if ydata[-1] > ydata[0]
                        else "decreasing"
                    )
                    trends.append(trend)
            if trends:
                info = (
                    "This is a line chart showing a generally "
                    + ", ".join(trends)
                    + " trend over time."
                )
            else:
                info = "This is a line chart showing trends over time."
    prompt = (
        "You are an assistant that writes detailed, descriptive alt-text for "
        "charts. The chart is a " + chart_type + " chart. " + info +
        "Please provide a concise and informative alt-text description."
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.7,
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"[Error] OpenAI API call failed: {e}")
        return _generate_heuristic_alt_text(ax, config)



# ENABLE INTERACTIVE HOVER

def _enable_interactive(ax):
    try:
        import mplcursors
        mplcursors.cursor(ax, hover=True)
        print("Interactive features enabled.")
    except ImportError:
        print(
            "[Warning] mplcursors is not installed. Run 'pip install mplcursors' to "
            "enable interactivity."
        )
