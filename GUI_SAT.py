from Functions.MultiSAT import *


def install(package):
    pip.main(['install', package])


try:
    from tkinter import *
except ImportError:
    print('tkinter is not installed, installing it now!')
    install('tkinter')

try:
    import numpy
except ImportError:
    print('numpy is not installed, installing it now!')
    install('numpy')


class GUI:

    def __init__(self, master):
        self.formula = StringVar()  # string que esta en el textbox
        self.clause_format = IntVar()  # el formato de las clausulas
        self.clause_format.set(1)  # por defecto formula personalizada
        self.algorithm = IntVar()  # indicar el algoritmo
        self.algorithm.set(5)  # por defecto CDCL

        self.master = master
        self.master.title("Problema de satisfacibilidad booleana")  # titulo de la ventana
        self.master.resizable(0, 0)  # evita redimensionar
        self.master.geometry("650x350")  # tamaño del master

        self.label1 = Label(master, text="Problema de satisfacibilidad booleana", font='Helvetica 10 bold')  # texto
        self.label1.place(x=200, y=20)  # posicion en el master (pixeles respecto al borde izq, pixeles respecto al borde superior)

        self.entry = Entry(master, textvariable=self.formula, width="50")  # textbox y le asigna una variable formula
        self.entry.place(x=52, y=75)  # posicion en el master

        self.button_compute = Button(master, text="Calcula", command=self.compute)  # cuando se pulse el boton, llama al metodo compute
        self.button_compute.place(x=370, y=72)  # posicion en el master

        self.label1 = Label(self.master, text="Introduzca una fórmula booleana. Formato: (a+!b+!c),(c+d+!a),(!d+b+a)")  # texto
        self.label1.place(x=52, y=50)  # posicion en el master (pixeles respecto al borde izq, pixeles respecto al borde superior)
        self.formula_p = Radiobutton(master, text="Fórmula personalizada", variable=self.clause_format, value=1, command=self.set_label)  # esta asociada a la variable format_clause
        self.formula_p.place(x=50, y=100)

        self.files = Radiobutton(master, text="Directorio | Fichero", variable=self.clause_format, value=2, command=self.set_label)  # esta asociada a la variable format_clause
        self.files.place(x=250, y=100)

        self.label2 = Label(master, text="Elija el algoritmo que desea ejecutar")  # texto
        self.label2.place(x=50, y=140)  # posicion en el master (pixeles respecto al borde izq, pixeles respecto al borde superior)

        self.brute_force = Radiobutton(master, text="Fuerza bruta", variable=self.algorithm, value=1)  # esta asociada a la variable algorithm
        self.brute_force.place(x=50, y=160)

        self.greedy = Radiobutton(master, text="Greedy/Búsqueda Local", variable=self.algorithm, value=2)  # esta asociada a la variable algorithm
        self.greedy.place(x=50, y=180)

        self.dpll = Radiobutton(master, text="DPLL", variable=self.algorithm, value=3)  # esta asociada a la variable algorithm
        self.dpll.place(x=50, y=200)

        self.cp = Radiobutton(master, text="Programación con restricciones", variable=self.algorithm, value=4)  # esta asociada a la variable algorithm
        self.cp.place(x=50, y=220)

        self.cdcl = Radiobutton(master, text="CDCL", variable=self.algorithm, value=5)  # esta asociada a la variable algorithm
        self.cdcl.place(x=50, y=240)

        self.label3 = Label(master, text="Tiempo de ejecución")  # texto
        self.label3.place(x=50, y=275)  # posicion en el master (pixeles respecto al borde izq, pixeles respecto al borde superior)

        self.label4 = Label(master, text="No disponible")  # texto
        self.label4.place(x=50, y=295)  # posicion en el master (pixeles respecto al borde izq, pixeles respecto al borde superior)

    def set_label(self):
        if self.clause_format.get() == 1:
            self.label1.config(text="Introduzca una fórmula booleana. Formato: (a+!b+!c)(c+d+!a)(!d+b+a)")
            self.label1.place(x=52,
                              y=50)  # posicion en el master (pixeles respecto al borde izq, pixeles respecto al borde superior)
        else:
            self.label1.config(text="Introduzca la ruta relativa del  directorio o fichero")
            self.label1.place(x=52,
                              y=50)  # posicion en el master (pixeles respecto al borde izq, pixeles respecto al borde superior)

    def get_clause(self):
        return self.formula.get()

    def get_clause_format(self):
        return self.clause_format.get()

    def get_algorithm(self):
        return self.algorithm.get()

    def compute(self):
        sat, time, result = main(self.get_clause_format(), self.get_clause(), self.get_algorithm())
        self.show_result(sat, time, result)

    def show_result(self, sat, time, result):
        if isinstance(result, dict):
            # unico fichero sat o formula personalizada
            if sat:
                label = Label(self.master, text="La fórmula introducida es satisfacible")  # texto
                label.place(x=390, y=295)  # posicion en el master (pixeles respecto al borde izq, pixeles respecto al borde superior)
                scroll = Scrollbar(self.master)
                scroll.place(x=600, y=180)
                textbox = Text(self.master, width=25, height=10, yscrollcommand=scroll.set)
                textbox.place(x=390, y=120)
                scroll.config(command=textbox.yview)  # enlaza scrollbar al textbox
                for key in result.keys():
                    textbox.insert(END, str(key) + " = " + str(result[key]))
                    textbox.insert(END, "\n")
                textbox.configure(state='disable')  # dehabilita la edicion
            else:
                label = Label(self.master, text="La fórmula introducida no es satisfacible")  # texto
                label.place(x=390, y=295)  # posicion en el master (pixeles respecto al borde izq, pixeles respecto al borde superior)
        else:
            if sat == False:
                # unico fichero y unsat
                label = Label(self.master, text="El fichero introducido no es satisfacible")  # texto
                label.place(x=390, y=295)  # posicion en el master (pixeles respecto al borde izq, pixeles respecto al borde superior)
            else:
                # directorio
                label = Label(self.master, text="El resultado se encuentra en el fichero")  # texto
                label.place(x=390, y=295)  # posicion en el master (pixeles respecto al borde izq, pixeles respecto al borde superior)
                label1 = Label(self.master, text=result)  # texto
                label1.place(x=390, y=310)  # posicion en el master (pixeles respecto al borde izq, pixeles respecto al borde superior)
        self.label4.config(text=str(time) + " segundos")  # actualiza el tiempo de ejecucion


if __name__ == "__main__":
    root = Tk()
    GUI = GUI(root)
    root.mainloop()  # para que una ventana siga en ejecucion tiene que estar en un bucle infinito
