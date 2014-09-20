#!/usr/bin/python

# Mercurial hook to reject any unstyled commit,
# and prevent checking in of executable files.
# istyle is a simple wrapper around the Artistic style executable,
# and a custom style file.



import os
import stat
import re
from mercurial import ui, hg


def are_changes_properly_formatted(ui, repo, **kwargs):
    
    ui.status('Checking if added and modified source files are properly style formatted..\n')
    fmod, fadd, frem, fdel, funk, fign, fcln = repo.status()
    files = [(f) for f in fmod] + \
            [(f) for f in fadd]

    forbid = False
    executableForbid = False
    
    for f in files:
        filePath = repo.root + '/' + f
        
        status = os.stat(filePath)
        if bool(status.st_mode & stat.S_IXGRP) or bool(status.st_mode & stat.S_IXUSR) or bool(status.st_mode & stat.S_IXOTH):
            ui.status('Invalid Execute Flag for file   : %s\n' % filePath)
            executableForbid = True
        
        if f.endswith('.h') or f.endswith('.cpp') or f.endswith('.c'):
            os.system('cp %s ~/tmp/hg_commit_format_chk \n' % filePath)
            newFilePath = '~/tmp/hg_commit_format_chk'
            output = os.popen('istyle %s\n' % newFilePath, 'r')
            for lines in output:
                if lines.find('formatted') >= 0:
                    ui.status('Invalid Style Format within file: %s\n' % filePath)
                    forbid = True

    if forbid:
        ui.status('Commit Failed: Fix style format of offending files (use hg istyle)\n')
    elif executableForbid:
        ui.status('Commit Failed: Remove execute permission on offending file(s)\n')
    else:
        ui.status('All added and modified source files are correctly style formatted and none are executable.\n')
    
    return (forbid or executableForbid)

    
