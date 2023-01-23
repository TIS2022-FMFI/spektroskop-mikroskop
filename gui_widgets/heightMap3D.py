import plotly.graph_objects as go
import pandas as pd

zdata = pd.read_csv("test.txt")

print(zdata)
fig = go.Figure(data=[go.Surface(z=zdata.values)])

fig.update_layout(title='3d graf spektrometra', autosize=False,
                  width=1800, height=1000,
                  margin=dict(l=40, r=50, b=65, t=90))

fig.show()
