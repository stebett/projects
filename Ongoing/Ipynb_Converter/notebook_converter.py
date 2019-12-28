# <begin code>
import re


# <end code>
# <begin code>
filepath = '/home/ginko/'

# <end code>
# <begin code>
nextline = False
kind = None
with open(filepath + 'Analysis.ipynb', 'r') as nb:
    with open(filepath + 'prova.ipynb', 'w+') as nf:
        for line in nb:
            if "cell_type" in line:

                if "code" in line:
                    kind = "code"
                elif "markdown" in line:
                    kind = "markdown"

                nf.write("# <begin " + kind + ">\n")

            if nextline is True:
                if len(re.findall(r'\s*[\]\}]\s+', line)) > 0:
                    # if there is only space characters and a ], close the cell
                    nf.write("# <end " + kind + ">\n")
                    nextline = False

                else:
                    towrite = re.findall(
                        r'(?<=\")(.*?)(?:\\n)?(?:\"(?:.(?!\"))*$)',
                        line)[0] + '\n'
                    if '\\"' in towrite:
                        towrite = towrite.replace('\\"', '"')

                    nf.write(towrite)

            if '"source": [' in line:
                nextline = True

# <end code>
