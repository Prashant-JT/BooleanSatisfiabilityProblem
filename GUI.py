from tkinter import *

root = Tk() # crea el root
root.title("Problema de satisfacibilidad booleana") # titulo de la ventana
root.resizable(0,0) # evita redimensionar

frame = Frame() # crea un frame
frame.pack() # empaqueta el frame en root
frame.config(width = "650", height = "350") # tamaño del frame

label = Label(frame, text = "Introduzca una fórmula booleana", font = (12)) # texto
label.place(x = 50, y = 50) # posicion en el frame (pixeles respecto al borde izq, pixeles respecto al borde superior)

formula = StringVar() # va ser la string que esta en el textbox

entry = Entry(frame, textvariable = formula, width = "50") # textbox y le asigna una variable formula
entry.place(x = 52, y = 75) # posicion en el frame

def compute():
    label = Label(frame, text = formula.get(), font = (12)) # obtiene el texto del textbox
    label.place(x = 480, y = 280) # posicion en el frame (pixeles respecto al borde izq, pixeles respecto al borde superior)

button_compute = Button(frame, text = "Calcula", command = compute) # cuando se pulse el boton, llama al metodo compute
button_compute.place(x = 370, y = 70) # posicion en el frame

label2 = Label(frame, text = "Elija el método que desea ejecutar", font = (12)) # texto
label2.place(x = 50, y = 125) # posicion en el frame (pixeles respecto al borde izq, pixeles respecto al borde superior)

option = IntVar() # va sindicar si un radiobutton esta seleccionado o no

brute_force = Radiobutton(frame, text = "Fuerza bruta", variable = option, value = 1) # esta asociada a la variable option 
brute_force.place(x = 50, y = 150)

greedy = Radiobutton(frame, text = "Greedy", variable = option, value = 2) # esta asociada a la variable option  
greedy.place(x = 50, y = 170)

dpll = Radiobutton(frame, text = "DPLL", variable = option, value = 3) # esta asociada a la variable option  
dpll.place(x = 50, y = 190)

mip = Radiobutton(frame, text = "MIP", variable = option, value = 4) # esta asociada a la variable option  
mip.place(x = 50, y = 210)

cdcl = Radiobutton(frame, text = "CDCL", variable = option, value = 5) # esta asociada a la variable option  
cdcl.place(x = 50, y = 230)

label3 = Label(frame, text = "Tiempo de ejecución", font = (12)) # texto
label3.place(x = 50, y = 270) # posicion en el frame (pixeles respecto al borde izq, pixeles respecto al borde superior)

label4 = Label(frame, text = "0.000 seg", font = (12)) # texto
label4.place(x = 50, y = 290) # posicion en el frame (pixeles respecto al borde izq, pixeles respecto al borde superior)

# Para que una ventana siga en ejcucion tiene que estar en un bucle infinito
root.mainloop()
