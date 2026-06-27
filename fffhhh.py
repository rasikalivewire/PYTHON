with open(r"C:\Users\Livewire\Downloads\ps.txt") as t:
    d=t.read()
    print(d)
with open(r"C:\Users\Livewire\Downloads\ps.txt","w") as t:
    d=t.write("good afternoon")
    print(d)
with open(r"C:\Users\Livewire\Downloads\ps.txt") as t:
    d=t.read()
    print(d)
with open(r"C:\Users\Livewire\Downloads\ps.txt","a") as t:
    d=t.write(" how are you?")
    print(d)
with open(r"C:\Users\Livewire\Downloads\ps.txt") as t:
    d=t.read()
    print(d)
with open(r"C:\Users\Livewire\Downloads\hari.ps","x") as t:
    d=t.write("hello")
    print(d)