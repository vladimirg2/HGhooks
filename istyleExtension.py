#!/usr/bin/python

# Mercurial extension to enable 'hg istyle'
# Will run istyle on added and modified files.


import re
import os
from mercurial import ui, hg

def ISTYLE(ui, repo, **opts):
    ui.status('repo.root: %s\n' % repo.root)
    fmod, fadd, frem, fdel, funk, fign, fcln = repo.status()
    files = [(f) for f in fmod] + \
            [(f) for f in fadd]
    ui.status('Formatting modified and added files ending in .h, .c  or .cpp:\n')
    for f in files:
        if f.endswith('.h') or f.endswith('.cpp') or f.endswith('.c'):
            filePath = repo.root + '/' + f
            os.system("istyle %s\n"  % filePath)


            
        
cmdtable = {
    # cmd name        function call
    "istyle": (ISTYLE,
               [('', '', None, 'no options')],
               "hg istyle will format uncommited .h, .cpp and .c files.")
}

