# -*- coding: utf-8 -*-
### Check if we need to redo the figure
import sys
import os.path as pth

# Get all parameters from the command line
__width = sys.argv[2]
__height = sys.argv[3]

__name_figure = sys.argv[1]
__name_file = f'{__name_figure}.py'
__dir_figure = pth.split(sys.argv[1])[0]
__last_edit = pth.getmtime(__name_file)
__meta_file = pth.join("pdf",__dir_figure,f".metadata_{pth.basename(__name_figure)}")

# If the meta file exists ...
if pth.exists(__meta_file) :
    with open(__meta_file,'r') as f:
        data = f.readline().split('\t')
    # ... and that the width, height and last_edit date are still the same ...
    if __width == data[0] and __height == data[1] and str(__last_edit) == data[2]:
        sys.exit(0) # Early return to LaTeX : no need to redo the generation

### If not, (re)do the figure
# Delayed matplotlib import to speed-up the process as much as possible in the case where regeneration is not needed
import matplotlib
import os

def ptstring_to_inches(text):
    ext = text[:-2]
    return float(ext)/72.27

import matplotlib.pyplot as plt

# Configuration of matplotlib to use the pgf backend
plt.rcParams.update({
    "text.usetex": True,     # Use an external TeX compiler for the math mode text
    "pgf.texsystem": "lualatex", #Use lualatex as the external compiler for the pgf backend
    "pgf.rcfonts": False ,   # Don't setup fonts from rc parameters
    "font.family": "serif", # Use a serif font for the text
    "pgf.preamble": "\n".join([r"\usepackage{amssymb}",r"\usepackage{amsmath}",r"\usepackage{xcolor}"]), #Compilation preamble. Add additional packages if needed
    })
matplotlib.use('pgf')
figure = plt.figure(figsize=(ptstring_to_inches(__width),ptstring_to_inches(__height)),dpi=600)
__activate_tight_layout = True

# Reading of the script file
__script = open(__name_file).read()
# If the script is in a sub-folder, change to the relevant folder to execute the script
if __dir_figure != '':
    __cwd = os.getcwd()
    os.chdir(__dir_figure)
    exec(__script,globals())
    os.chdir(__cwd)
else:
    exec(__script,globals())

# If no special layout was chosen automatically run tight_layout
if __activate_tight_layout:
    plt.tight_layout(pad=0.1)
    
# Generate the relevant path inside the pdf folder, don't raise an error if it already exists
os.makedirs(pth.split(__meta_file)[0],exist_ok=True)

# Export the figure to pdf, can take quite some time for complex figures
figure.set_size_inches(ptstring_to_inches(__width),ptstring_to_inches(__height))
plt.savefig(f'pdf/{__name_figure}.pdf', bbox_inches=None,transparent=True)

# Save the current figure paprameters into the meta file
with open(__meta_file,'w') as f:
    f.write(f"{__width}\t{__height}\t{__last_edit}")
