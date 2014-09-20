A quick and simple way to check force a style when using Mercurial.
The istyle extension runs the istyle script, which is just a call to astyle with an options file.
And the hooks check for modified but unstuled files.
If the style is wrong, the files are styled and the user must try to commit again.
Otherwise the commit is allowed.
The hooks also look for executable files, which should not be commited.
Requires astyle-1.24 which supports piped input.


