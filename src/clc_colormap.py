import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

def get_clccolormap() -> ListedColormap:
    nothing = "#ffffff"
    dark_green = "#124a13"
    light_green = "#abe861"
    light_blue = "#6aa8de"
    dark_blue = "#3141eb"

    my_colors = [nothing, nothing] + [dark_green, dark_green, dark_green] + [light_green, light_green, light_green] + \
                [nothing, nothing] + [dark_blue, light_blue] + [nothing]*244
    my_cmap = ListedColormap(my_colors, "CLC_COLORMAP")
    return my_cmap
