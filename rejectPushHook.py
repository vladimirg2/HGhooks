#!/usr/bin/python

# Mercurial hook to reject any push with an unstyled tip


import os
import re
from mercurial import ui, hg


def reject_improperly_formatted_push(ui, repo, node, **kwargs):

    ui.status('Mercurial repo.root: %s\n' % repo.root)
    ui.status('The node being created is: %s \n' % node)


    fileSet = set()

    #Grab the tip's file context
    ctx = repo['tip']
    
    # Loop through each changeset being added to the repository
    for change_id in xrange(repo[node].rev(), len(repo)):
        ui.status('Style format checking will include changeset: %d\n' % change_id)
        for currentFile in repo[change_id].files():
            if currentFile.endswith('.h') or currentFile.endswith('.cpp') or currentFile.endswith('.c'):
                fileSet.add(currentFile)
                

    forbid = False
    for currentFile in fileSet:
        # Do not check the file if it is being deleted
        if currentFile not in ctx:
            continue;
        userHome = os.getenv('HOME')
        outFilePath = userHome + '/tmp/hg_push_format_chk'
        ff = open(outFilePath,'w')
        # Get the file context
        fctx = ctx[currentFile]
        # Save the contents of the current file to the temp file
        ff.write(fctx.data())
        # Close the temp file
        ff.close()
        output = os.popen('istyle %s\n' % '~/tmp/hg_push_format_chk', 'r')
        for lines in output:
            if lines.find('formatted') >= 0:
                ui.status("Invalid Style Format within file: %s\n" % currentFile)
                forbid = True

    
    if forbid:
        ui.status("Push/Pull Failed: Fix style format of offending files (using istyle and hg commit) and then retry push/pull.\n")
    else:
        ui.status("All added and modified files are correctly formatted.\n")
    
    return forbid

