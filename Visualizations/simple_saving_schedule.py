import pandas as pd

from bokeh.plotting import *
from bokeh.charts import Line, show


df = pd.read_csv('savings_schedule.csv', sep=',')
df = df.set_index(['Savings Rate'])

output_file("simple_saving_schedule.html")

p =  Line(df, title="Working Years", xlabel="Savings Rate (percent)", ylabel="Working Years Until Retirement",
         notebook=True)
show(p)