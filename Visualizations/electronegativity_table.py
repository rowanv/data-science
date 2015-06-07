#Created an electronegativity table. 
#This is a variation of the Periodic Table example in the Bokeh library
#Check out the Periodic Table tutorial here: http://bokeh.pydata.org/en/latest/docs/gallery/periodic.html

from collections import OrderedDict

from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.sampledata import periodic_table



elements = periodic_table.elements[periodic_table.elements["group"] != "-"]

group_range = [str(x) for x in range(1,19)]
period_range = [str(x) for x in reversed(sorted(set(elements["period"])))]

def electroneg_to_discrete(e_val):
    if e_val < 1.5:
        return '0_to_1.5'
    elif e_val < 1.9:
        return '1.5_to_1.9'
    elif e_val < 2.9:
        return '2.0_to_2.9'
    elif e_val <= 4.0:
        return '3.0_to_4.0'
    else:
        return 'NaN'

electroneg_discrete = map(lambda x: electroneg_to_discrete(x), elements['electronegativity'])

                
colormap = {
    '0_to_1.5': '#ffffcc',
    '1.5_to_1.9' : '#a1dab4',
    '2.0_to_2.9': '#41b6c4',
    '3.0_to_4.0': '#225ea8',
    'NaN': '#bdbdbd'
    
    
}

source = ColumnDataSource(
    data = dict(
    group=[str(x) for x in elements["group"]],
    period=[str(y) for y in elements["period"]],
    symx=[str(x)+":0.1" for x in elements["group"]],
    name = elements["name"],
    numbery=[str(x)+":0.8" for x in elements["period"]],
    electronegativity = elements["electronegativity"],
    symbol = elements["symbol"],
    namey=[str(x)+":0.3" for x in elements["period"]],
    atomic_number = elements['atomic number'],
    type_color=[colormap[x] for x in electroneg_discrete],
    electronegativityy = [str(x)+':0.1' for x in elements['period']]))
    
output_file("electronegativity_table.html")


p = figure(title="Electronegativity", tools="resize,hover,save",
          x_range=group_range, y_range=period_range)
p.plot_width = 1200
p.toolbar_location = "left"

p.rect("group", "period", 0.9, 0.9, source=source,
      fill_alpha=0.6, color="type_color")

text_props = {
    "source": source,
    "angle": 0,
    "color": "black",
    "text_align": "left",
    "text_baseline": "middle"
}

p.text(x="symx", y="period", text="symbol",
    text_font_style="bold", text_font_size="15pt", **text_props)

p.text(x="symx", y = 'numbery', text='atomic_number', 
      text_font_size='9pt', **text_props)

p.text(x="symx", y="namey", text="name",
      text_font_size="6pt", **text_props)

p.grid.grid_line_color = None

hover = p.select(dict(type=HoverTool))
hover.tooltips = OrderedDict([
        ("name", "@name"),
        ("atomic number", "@atomic_number"),
        ("electronegativity", "@electronegativity")
    ])

show(p)