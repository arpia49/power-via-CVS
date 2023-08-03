"""Script that helps identifying the major differences between your power curve and a model.
"""

import csv
import tkinter as tk
from tkinter import filedialog, messagebox
import locale
import gettext

_ = gettext.gettext
current_locale = locale.getlocale(locale.LC_CTYPE)[0].split('_')[0].lower()

my_locale = gettext.translation('base', localedir='locales',
                                 languages=[current_locale])
my_locale.install()
_ = my_locale.gettext

def revisar_datos(csv_file, valor_max_segundos, num_lineas):
    """Check if csv format is ok and, then, extract the result.
    """

    with open(csv_file, 'r', encoding='utf-8-sig') as archivo:
        lector_csv = csv.reader(archivo)
        encabezados = [encabezado.strip() for encabezado in
                       next(lector_csv)]  # Remove blank spaces

        # Verificar que las columnas requeridas estén presentes en el archivo CSV
        if 'secs' not in encabezados or '42 days' not in encabezados or 'ECP' not in encabezados:
            messagebox.showerror((_("Error")),
                                 (_("El archivo CSV no tiene las columnas requeridas.")))
            return

        datos = []
        for fila in lector_csv:
            # Leer los datos de cada fila
            seconds = locale.atof(fila[encabezados.index('secs')])
            value = locale.atof(fila[encabezados.index('42 days')])
            model = locale.atof(fila[encabezados.index('ECP')])

            if seconds <= valor_max_segundos:
                # Calcular la diferencia en porcentaje
                diferencia_porcentaje = ((model - value) / value) * 100

                datos.append((seconds, value, model, diferencia_porcentaje))

        # Ordenar los datos por la diferencia en porcentaje de mayor a menor
        datos_ordenados = sorted(datos, key=lambda x: x[3], reverse=True)

        # Imprimir el número específico de líneas ordenadas
        for i in range(min(num_lineas, len(datos_ordenados))):
            seconds, value, model, diferencia_porcentaje = datos_ordenados[i]
            resultado_text.insert(tk.END,
                                  f"{seconds:.0f} segundos -> {value:.0f}W vs {model:.0f}W -> {diferencia_porcentaje:.2f}%\n")

def select_file():
    """Opens a new window to select the csv file.
    """
    csv_file = filedialog.askopenfilename(filetypes=[(_("Archivos CSV"), "*.csv")])
    archivo_entry.delete(0, tk.END)
    archivo_entry.insert(tk.END, csv_file)

def procesar():
    """Call for the processing retrieving the needed data from UI
    """
    csv_file = archivo_entry.get()
    valor_max_segundos = float(segundos_entry.get())
    num_lineas = int(lineas_entry.get())

    resultado_text.delete(1.0, tk.END)
    revisar_datos(csv_file, valor_max_segundos, num_lineas)

# Configurar el separador decimal como punto
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

# Crear la ventana principal
ventana = tk.Tk()
ventana.title(_("Revisar Datos CSV"))
ventana.geometry("400x300")

# Etiqueta y campo de texto para el archivo CSV
archivo_label = tk.Label(ventana, text=_("Archivo CSV:"))
archivo_label.pack()
archivo_entry = tk.Entry(ventana, width=40)
archivo_entry.pack()
archivo_boton = tk.Button(ventana, text=(_("Seleccionar")), command=select_file)
archivo_boton.pack()

# Etiqueta y campo de texto para el valor máximo de los segundos
segundos_label = tk.Label(ventana, text=_("Valor máximo de los segundos:"))
segundos_label.pack()
segundos_entry = tk.Entry(ventana)
segundos_entry.insert(0, "1800")
segundos_entry.pack()

# Etiqueta y campo de texto para el número de líneas a imprimir
lineas_label = tk.Label(ventana, text=_("Número de líneas a imprimir:"))
lineas_label.pack()
lineas_entry = tk.Entry(ventana)
lineas_entry.insert(0, "5")
lineas_entry.pack()

# Botón para procesar los datos
procesar_boton = tk.Button(ventana, text=(_("Procesar")), command=procesar)
procesar_boton.pack()

# Área de texto para mostrar los resultados
resultado_text = tk.Text(ventana, height=5, width=80)
resultado_text.pack()

# Iniciar el bucle principal de la interfaz gráfica
ventana.mainloop()
