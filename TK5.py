from tkinter import *
from tkinter import messagebox

users = {}

root = Tk()
root.title("Login System")
root.geometry("300x250")

def login():
    username = user_entry.get()
    password = pass_entry.get()

    if username in users and users[username] == password:
        messagebox.showinfo("Success", "Login Successful!")
    else:
        messagebox.showerror("Error", "Invalid Username or Password")

def open_signup():
    signup = Toplevel(root)
    signup.title("Sign Up")
    signup.geometry("300x250")

    Label(signup, text="Create Username").pack(pady=5)
    new_user = Entry(signup)
    new_user.pack()

    Label(signup, text="Create Password").pack(pady=5)
    new_pass = Entry(signup, show="*")
    new_pass.pack()

    def register():
        username = new_user.get()
        password = new_pass.get()

        if username == "" or password == "":
            messagebox.showerror("Error", "Fields cannot be empty")
            return

        if username in users:
            messagebox.showerror("Error", "Username already exists")
        else:
            users[username] = password
            messagebox.showinfo("Success", "Account Created")
            signup.destroy()

    Button(signup, text="Register",
           command=register).pack(pady=10)

Label(root, text="LOGIN",
      font=("Arial", 16, "bold")).pack(pady=10)

Label(root, text="Username").pack()
user_entry = Entry(root)
user_entry.pack()

Label(root, text="Password").pack()
pass_entry = Entry(root, show="*")
pass_entry.pack()

Button(root, text="Login",
       command=login).pack(pady=10)

Button(root, text="Sign Up",
       command=open_signup).pack()

root.mainloop()