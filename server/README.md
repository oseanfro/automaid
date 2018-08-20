This needs to contain ALL the incoming server files, *LOG, *MER, *vit,
*cmd files and the whole lot, and the main.py script will process it
all and distributed it over the processed directory incrementally.

Not useful to give one or two examples of these files, you have to
have the whole thing running to get this to work as advertised.

In my own work I keep my (copy) of the server somewhere, 

`$somewhere/server`

and then, in there, I make

`$somewhere/processed`

and then, since `main.py` is a bit explicit, I PHYSICALLY NEED TO COPY
the scripts directory from where I usually keep my other python
scripts, as by the environmental variable $YFILES,

`cp -r $YFILES/automaid/scripts $somewhere`

I then have a script $UFILES/servercopy which syncs the data from the
server and maintains a git repo of those files.

And then for processing, I change INTO the directory $somewhere,
where, since I usually am not in bash, I execute the sequence:

`bash`\
`source activate pymaid`\
`python scripts/main.py`\
`source deactivate`

after which I should find the processed files inside `$somewhere/processed`.



