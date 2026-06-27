#file handling
with open(r"C:\Users\Livewire\Downloads\file.txt")as ra:
    d=ra.read()
    print(d)
with open(r"C:\Users\Livewire\Downloads\file.txt","w")as ra:
    d=ra.write("hello")
    print(d)
with open(r"C:\Users\Livewire\Downloads\file.txt", "r") as ra:
    print(ra.read())
with open(r"C:\Users\Livewire\Downloads\file.txt", "a") as ra:
    d=ra.write(" students")
with open(r"C:\Users\Livewire\Downloads\file.txt", "r") as ra:
    print(ra.read())
# try:
#     with open(r"C:\Users\Livewire\Downloads\file.txt", "x") as ra:
#         d=ra.write("new file")
# except file_exist_error:
#     print(fileexistserror)
'''with open(r"C:\Users\Livewire\Downloads\file.txt", "rb") as ra:
    print(ra.read())
with open(r"C:\Users\Livewire\Downloads\file.txt", "r+") as ra:
    print(ra.read())
    print(ra.read())
    print(ra.write("the end"))
with open(r"C:\Users\Livewire\Downloads\file.txt", "r") as ra:
    print(ra.read())'''

