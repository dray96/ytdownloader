# crear pequeño panel con tkinter
import time
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import pytube
import os
import threading

class Aplicacion():
    def __init__(self):
        self.raiz = Tk()
        self.raiz.title("YTDownloader v0.5 (BETA)")
        # cambiar color del fondo
        self.raiz.config(bg="#F43939")
        self.raiz.protocol("WM_DELETE_WINDOW", self.salir)
        self.raiz.resizable(0, 0)
        # cambiar tamaño de letra de la raiz
        self.raiz.option_add("*Font", "Arial 12")
        self.raiz.iconbitmap("ytd.ico")
        self.raiz.geometry("900x250")

        # obtener resolucion de la pantalla
        ancho_pantalla = self.raiz.winfo_screenwidth()
        alto_pantalla = self.raiz.winfo_screenheight()
        #print(f"Ancho: {ancho_pantalla} - Alto: {alto_pantalla}")
        n_ancho = (ancho_pantalla/2)/2
        n_alto = (alto_pantalla/2)/2
        self.raiz.geometry(f"+{n_ancho:.0f}+{n_alto:.0f}")

        self.crear_widgets()

        self.raiz.mainloop()

    def crear_widgets(self):
        self.etiqueta1 = Label(self.raiz, text="URL del video: ")
        self.etiqueta1.config(bg="#F43939")
        self.etiqueta1.config(fg="white")
        self.etiqueta1.grid(row=0, column=0, padx=10, pady=10)

        # URL DEL VIDEO
        self.url = StringVar()
        self.caja1 = Entry(self.raiz, textvariable=self.url, width=50)
        self.caja1.config(bg="#F43939")
        self.caja1.config(fg="white")
        self.caja1.grid(row=0, column=1, padx=10, pady=10)

        # BOTON DESCARGAR
        self.boton1 = Button(self.raiz, text="Descargar", command=threading.Thread(target=self.descargar).start)
        self.boton1.config(cursor="hand2")
        self.boton1.config(bg="#F43939")
        self.boton1.config(fg="white")
        self.boton1.config(width=20)
        self.boton1.grid(row=3, column=1, padx=10, pady=10)

        # BOTON BUSCAR RUTA DE DESCARGA
        self.boton2 = Button(self.raiz, text="Examinar", command=self.buscar)
        self.boton2.config(cursor="hand2")
        self.boton2.config(bg="#F43939")
        self.boton2.config(fg="white")
        self.boton2.config(width=20)
        self.boton2.grid(row=1, column=2, padx=10, pady=10)

        self.etiqueta2 = Label(self.raiz, text="Guardar en: ")
        self.etiqueta2.config(bg="#F43939")
        self.etiqueta2.config(fg="white")
        self.etiqueta2.grid(row=1, column=0, padx=10, pady=10)

        # RUTA DE DESCARGA
        ruta_descargas = open("config.txt", "r")
        ruta_descargas = ruta_descargas.read()
        print(ruta_descargas)


        self.ruta = StringVar()
        self.caja2 = Entry(self.raiz, textvariable=self.ruta, width=50)
        self.ruta.set(ruta_descargas)
        self.caja2.config(bg="#F43939")
        self.caja2.config(fg="white")
        self.caja2.config(state="readonly")
        self.caja2.config(readonlybackground="#F43939")
        self.caja2.grid(row=1, column=1, padx=10, pady=10)


        #label de version de la app
        self.informacion = Label(self.raiz, text="YTDownloader v0.5 (BETA)")
        self.informacion.config(bg="#F43939")
        self.informacion.config(fg="white")
        self.informacion.config(font=("Arial", 9))
        self.informacion.grid(row=3, column=0, padx=10, pady=10)


        # crear barra de progreso
        self.barra = ttk.Progressbar(self.raiz, orient=HORIZONTAL, length=200, mode="determinate")
        self.barra.grid(row=2, column=1, padx=10, pady=10)
        self.barra.grid_remove()


    def destruir_boton(self):
        # destruir el boton de descargar
        for widget in self.raiz.winfo_children():
            if widget == self.boton1:
                widget.destroy()
                print("Boton destruido")

        #self.crear_boton()
        #self.boton1.destroy()

        self.crear_boton()


    def crear_boton(self):
        self.boton1 = Button(self.raiz, text="Descargar", command=threading.Thread(target=self.descargar).start)
        self.boton1.config(cursor="hand2")
        self.boton1.config(bg="#F43939")
        self.boton1.config(fg="white")
        self.boton1.config(width=20)
        self.boton1.grid(row=3, column=1, padx=10, pady=10)

    def descargar(self):
        self.destruir_boton()


        if self.ruta.get() == "":
            messagebox.showwarning("ADVERTENCIA", "Debe seleccionar una ruta de descarga")
        elif self.url.get() == "":
            messagebox.showwarning("ADVERTENCIA", "No puede dejar el campo de URL vacio")
        else:
            try:
                video = pytube.YouTube(self.url.get())
                self.raiz.title(f"YTDownloader - Descargando '{video.title}' ")

                # label nombre del video
                self.video_descargar = Label(self.raiz, text="Descargando...")
                self.video_descargar.grid(row=2, column=0, padx=10, pady=10)
                self.video_descargar.config(bg="#F43939")
                self.video_descargar.config(fg="white")

                # obtener cantidad que se está descargando

                stream = video.streams.get_highest_resolution()

                ruta = stream.download(self.ruta.get())
                # actualizar progressbar con el valor de la descarga en porcentaje
                self.barra.grid()
                self.barra["value"] = 100
                # peso del archivo descargado en megabytes
                peso = os.path.getsize(ruta) / 1000000

                self.video_descargar.config(text=f"¡FINALIZADO!")

                # actualizar label de la barra de progreso
                self.labelpb = Label(self.raiz, text="")
                self.labelpb.config(bg="#F43939")
                self.labelpb.config(fg="white")
                self.labelpb.grid(row=3, column=2, padx=10, pady=10)
                self.labelpb.config(text=f"¡Descarga completada!")


                # limpiando panel
                self.caja1.delete(0, END)
                """self.caja2.config(state="normal")
                self.caja2.delete(0, END)"""
                self.caja2.config(state="readonly")
                self.raiz.title(f"YTDownloader - Descarga completa")
                self.raiz.after(5000, self.raiz.title, "YTDownloader v0.5 (BETA)")
                self.video_descargar.after(5000, self.video_descargar.destroy)
                self.labelpb.after(5000, self.labelpb.destroy)
                self.barra.after(5000, self.barra.grid_remove)
                messagebox.showinfo("Finalizado ✅", f"¡Descarga completada exitosamente! (Peso: {peso:.1f} mb)")
            except pytube.exceptions.RegexMatchError:
                messagebox.showerror("ERROR", "URL inválida, ingrese una URL de youtube correcta.")


    def buscar(self):
        ruta = filedialog.askdirectory()
        self.ruta.set(ruta)
        ruta_descargas = open("config.txt", "w")
        ruta_descargas.write(ruta)
        ruta_descargas.close()

    def salir(self):
        valor = messagebox.askquestion("YTDownloader", "¿Desea abandonar la aplicación?")
        if valor == "yes":
            self.raiz.destroy()

if __name__ == "__main__":
    mi_app = Aplicacion()



