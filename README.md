# file_copy
A simple python script that copies files licensed under MIT.

It is used to copy contents of a folder to another folder using 
optionaly and expression to especify the files

## Help Message:
```
❯ py file_copy.py -h
usage: file_copy.py [-h] [-e EXPRESSION] [-c] [-d] [-i] loc_a loc_b

Verifyfiles verifies the files in 2 folders the files can have a pattern to be identified this program can also copy and
delete after the copy has done.

positional arguments:
  loc_a                 location a, from where the files are copied
  loc_b                 location b, where the files will be copied

optional arguments:
  -h, --help            show this help message and exit
  -e EXPRESSION, --expression EXPRESSION
                        expression that will be used to specify the files, can be used to especify the extesion of the file
  -c, --copy            copies files from loc_a to loc_b
  -d, --delete          deletes files from folder a that already have been copied correctly
  -i, --ignore          ignores warning when deleting files
```

## TLDR

Prints the difference in files in both folders:
`py file_copy.py ./a/ ./b/`

Copies files from a to b:
`py file_copy.py ./a/ ./b/ -c`

Copies files from a to b that contain in the title .txt:
`py file_copy.py ./a/ ./b/ -ce .txt`

Copies files from a to b that contain in the title .txt and then deletes the files that have been copied with the correct sizes:
`py file_copy.py ./a/ ./b/ -cde .txt`

Deletes the files in a that also exist in b with the same size and title, the i ignores the deletition warning:
`py file_copy.py ./a/ ./b/ -di`






