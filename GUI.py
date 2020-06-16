from tkinter import *

class GUI:

    def __init__(self, master):
        self.formula = StringVar() # string que esta en el textbox
        self.format_clause = IntVar() # el formato de las clausulas
        self.algorithm = IntVar() # indicar el algoritmo 
        
        self.master = master
        self.master.title("Problema de satisfacibilidad booleana") # titulo de la ventana
        self.master.resizable(0,0) # evita redimensionar
        self.master.config(width = "650", height = "350") # tamaño del master
        
        self.label0 = Label(master, text = "Problema de satisfacibilidad booleana", font = 'Helvetica 10 bold') # texto
        self.label0.place(x = 220, y = 15) # posicion en el master (pixeles respecto al borde izq, pixeles respecto al borde superior)

        self.label1 = Label(master, text = "Introduzca una fórmula booleana o directorio o nombre de fichero") # texto
        self.label1.place(x = 50, y = 50) # posicion en el master (pixeles respecto al borde izq, pixeles respecto al borde superior)
    
        self.entry = Entry(master, textvariable = self.formula, width = "50") # textbox y le asigna una variable formula
        self.entry.place(x = 52, y = 75) # posicion en el master

        self.button_compute = Button(master, text = "Calcula", command = self.compute) # cuando se pulse el boton, llama al metodo compute
        self.button_compute.place(x = 370, y = 70) # posicion en el master

        self.formula_p = Radiobutton(master, text = "Fórmula personalizada", variable = self.format_clause, value = 1) # esta asociada a la variable format_clause 
        self.formula_p.place(x = 50, y = 100)

        self.files = Radiobutton(master, text = "Directorio | Fichero", variable = self.format_clause, value = 2) # esta asociada a la variable format_clause 
        self.files.place(x = 250, y = 100)

        self.label2 = Label(master, text = "Elija el método que desea ejecutar") # texto
        self.label2.place(x = 50, y = 140) # posicion en el master (pixeles respecto al borde izq, pixeles respecto al borde superior)

        self.brute_force = Radiobutton(master, text = "Fuerza bruta", variable = self.algorithm, value = 1) # esta asociada a la variable algorithm 
        self.brute_force.place(x = 50, y = 160)

        self.greedy = Radiobutton(master, text = "Greedy/Búsqueda Local", variable = self.algorithm, value = 2) # esta asociada a la variable algorithm  
        self.greedy.place(x = 50, y = 180)

        self.dpll = Radiobutton(master, text = "DPLL", variable = self.algorithm, value = 3) # esta asociada a la variable algorithm  
        self.dpll.place(x = 50, y = 200)

        self.cp = Radiobutton(master, text = "Programación con restricciones", variable = self.algorithm, value = 4) # esta asociada a la variable algorithm  
        self.cp.place(x = 50, y = 220)

        self.cdcl = Radiobutton(master, text = "CDCL", variable = self.algorithm, value = 5) # esta asociada a la variable algorithm  
        self.cdcl.place(x = 50, y = 240)

        self.label3 = Label(master, text = "Tiempo de ejecución") # texto
        self.label3.place(x = 50, y = 275) # posicion en el master (pixeles respecto al borde izq, pixeles respecto al borde superior)

        self.label4 = Label(master, text = "0.000 seg") # texto
        self.label4.place(x = 50, y = 295) # posicion en el master (pixeles respecto al borde izq, pixeles respecto al borde superior)

        self.label5 = Label(master, text = "La fórmula introducida es ") # texto
        self.label5.place(x = 300, y = 295) # posicion en el master (pixeles respecto al borde izq, pixeles respecto al borde superior)

    def compute(self):
        print(self.formula.get())
        label = Label(self.master, text = self.formula.get(), font = (12)) # obtiene el texto del textbox
        label.place(x = 480, y = 280) # posicion en el master (pixeles respecto al borde izq, pixeles respecto al borde superior)
        #return self.formula.get()

if __name__ == "__main__":
    root = Tk()
    GUI = GUI(root)
    root.mainloop() # Para que una ventana siga en ejcucion tiene que estar en un bucle infinito