This needs to contain ALL the incoming server files, *LOG, *MER, *vit,
*cmd files and the whole lot, and the main.py script will process it
all and distributed it over the processed directory incrementally.

Not useful to give one or two examples of these files, you have to
have the whole thing running to get this to work as advertised.

In my own work I keep my (copy) of the server somewhere, 

`$somewhere/server`

and then, in there, I make

`$somewhere/processed`

and then I need to physically copy the scripts from where I usually
keep my pythons, which I keep there so I can keep it as a small git repo. 

`cp -r $YFILES/automaid/scripts $somewhere/scripts`

And then IN that directory, $somewhere, I execute the sequence:

`bash`\
`source activate pymaid`\
`python scripts/main.py`\
`source deactivate pymaid`

and then I should find the processed files inside `processed`.



