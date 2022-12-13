from matplotlib.widgets import Button
import matplotlib.pyplot as plt
from easygui import fileopenbox

fig = plt.figure("Kalibracia spektrometra", figsize=(10, 6), facecolor='#75bbfd')

figures = []


def select_file(x):
    file = fileopenbox(title='Vyberte kalibracny subor', filetypes=[['*.txt', 'Text File']])

    read_file(file)


def read_file(file, delimeter='\t'):
    if file is None: return

    with open(file, "r") as f:
        line = f.readline()

        while line != '':
            figure = list(map(lambda x: float(x.strip()), line.split(delimeter)))
            line = f.readline()
            figures.append(figure)

    print(figures)


btn = Button(plt.axes([0.74, 0.03, 0.25, 0.05]), label='Kalibrovat podla suboru', color='xkcd:sky blue')
btn.on_clicked(select_file)

plt.show()
