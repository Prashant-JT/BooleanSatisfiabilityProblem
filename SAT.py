from tkinter import *

root = Tk() # crea el root
root.title("Boolean satisfiability problem") # titulo de la ventana
root.resizable(0,0) # evita redimensionar
root.iconbitmap("icon.ico") # icono de la ventana
# root.geometry("650x350") # root se adapta al tamaño del frame, por lo que no hace falta darle tamaño

frame = Frame() # crea un frame
frame.pack() # empaqueta el frame en root
frame.config(width = "650", height = "350") # tamaño del frame

# Para que una ventana siga en ejcucion tiene que estar en un bucle infinito
root.mainloop()