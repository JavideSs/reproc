#Base64 images are written to a text file, so they can be changed if the program is compiled

#exec() function is not recommended, code can be injected
#But being a local application without security there is no problem
exec(open("data/images/images_base64.txt", "r").read())