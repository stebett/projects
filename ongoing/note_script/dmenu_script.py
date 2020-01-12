import subprocess


def dmenu(prompt, inputs):
    inputsString = '\n'.join(i.replace('\n', ' ') for i in inputs)
    args = ['dmenu',
            '-i',
            '-p', prompt,
            '-l', '10',
            '-nb', '#3c3836',
            '-nf', '#ebdbb2',
            '-fn', 'Anonymous Pro:pixelsize=18:style=bold',
            '-sb', '#d3869b',
            '-sf', '#282828']

    result = subprocess.run(args, input=inputsString,
                            stdout=subprocess.PIPE,
                            universal_newlines=True)

    selected = result.stdout.strip().strip()

    return selected
