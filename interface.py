import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from normalization import check_and_convert_1fn, check_and_convert_2fn, check_and_convert_3fn

# Variables globales
tables = []
roles_info = []
table_names = []

def show_suboptions():
    if suboptions_frame.winfo_ismapped():
        suboptions_frame.pack_forget()
    else:
        suboptions_frame.pack()

def clear_right_panel():
    for widget in right_panel_content.winfo_children():
        widget.destroy()

def exit_application():
    root.quit()

def create_interface():
    global root, suboptions_frame, right_panel, right_panel_canvas, right_panel_scrollbar_y, right_panel_scrollbar_x, right_panel_content, bg_image_label, bg_image_tk

    # Crear la ventana principal
    root = tk.Tk()
    root.title("Interfaz Gráfica con Panel de Opciones")
    root.geometry("800x600")  # Tamaño de la ventana

    # Cargar la imagen de fondo
    try:
        bg_image = Image.open('/home/sh4rk/Desktop/ProyectoI/mesh-gradient.png')
        bg_image = bg_image.resize((240, 600), Image.LANCZOS)
        bg_image_tk = ImageTk.PhotoImage(bg_image)
    except IOError:
        messagebox.showerror("Error", "No se pudo cargar la imagen de fondo.")
        return

    # Crear el panel izquierdo (30% del ancho)
    left_panel = tk.Frame(root, width=240, height=600)
    left_panel.pack(side="left", fill="y")

    # Etiqueta para la imagen de fondo
    bg_image_label = tk.Label(left_panel, image=bg_image_tk)
    bg_image_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Frame para los botones dentro del panel izquierdo
    button_frame = tk.Frame(left_panel, bg="lightgray")
    button_frame.place(x=0, y=0, relwidth=1, relheight=1)

    # Botón de Opciones
    options_button = ttk.Button(button_frame, text="Opciones", command=show_suboptions)
    options_button.pack(pady=10, padx=10, fill="x")

    # Frame para las subopciones
    suboptions_frame = tk.Frame(button_frame, bg="lightgray")
    suboptions_frame.pack_forget()  # Inicialmente oculto

    # Subopciones
    suboption_1fn = ttk.Button(suboptions_frame, text="1FN", command=check_and_convert_1fn_action)
    suboption_1fn.pack(pady=5, padx=20, anchor="w")

    suboption_2fn = ttk.Button(suboptions_frame, text="2FN", command=check_and_convert_2fn_action)
    suboption_2fn.pack(pady=5, padx=20, anchor="w")

    suboption_3fn = ttk.Button(suboptions_frame, text="3FN", command=check_and_convert_3fn_action)
    suboption_3fn.pack(pady=5, padx=20, anchor="w")

    # Botón de Limpiar
    clear_button = ttk.Button(button_frame, text="Limpiar", command=clear_right_panel)
    clear_button.pack(pady=10, padx=10, fill="x")

    # Botón de Salir
    exit_button = ttk.Button(button_frame, text="Salir", command=exit_application)
    exit_button.pack(pady=10, padx=10, fill="x")

    # Crear el panel derecho (70% del ancho)
    right_panel = tk.Frame(root)
    right_panel.pack(side="right", fill="both", expand=True)

    # Crear un canvas para permitir el desplazamiento
    right_panel_canvas = tk.Canvas(right_panel)
    right_panel_canvas.pack(side="left", fill="both", expand=True)

    # Agregar una barra de desplazamiento vertical
    right_panel_scrollbar_y = ttk.Scrollbar(right_panel, orient="vertical", command=right_panel_canvas.yview)
    right_panel_scrollbar_y.pack(side="right", fill="y")

    # Agregar una barra de desplazamiento horizontal
    right_panel_scrollbar_x = ttk.Scrollbar(right_panel, orient="horizontal", command=right_panel_canvas.xview)
    right_panel_scrollbar_x.pack(side="bottom", fill="x")

    # Crear un frame para contener las tablas y agregarlo al canvas
    right_panel_content = tk.Frame(right_panel_canvas)
    right_panel_canvas.create_window((0, 0), window=right_panel_content, anchor="nw")
    right_panel_content.bind("<Configure>", lambda e: right_panel_canvas.configure(scrollregion=right_panel_canvas.bbox("all")))

    return root

def display_tables(tables, roles_info):
    # Limpiar el panel derecho
    clear_right_panel()

    # Agregar un Treeview por cada tabla
    for idx, (table_df, roles) in enumerate(zip(tables, roles_info)):
        frame = tk.Frame(right_panel_content)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Agregar un título para la tabla
        title_frame = tk.Frame(frame)
        title_frame.pack(fill="x")

        table_label = tk.Label(title_frame, text=f"Tabla {idx + 1}:", font=("Arial", 14, "bold"))
        table_label.pack(side="left", pady=(0, 10))

        # Campo de entrada para el nombre de la tabla
        name_entry = tk.Entry(title_frame)
        name_entry.insert(0, table_names[idx])  # Valor por defecto
        name_entry.pack(side="left", padx=10)

        # Botón para guardar el nombre
        save_button = ttk.Button(title_frame, text="Guardar", command=lambda idx=idx, entry=name_entry: save_table_name(idx, entry))
        save_button.pack(side="left")

        # Crear Treeview
        columns = list(table_df.columns)
        tree = ttk.Treeview(frame, columns=columns, show="headings")

        # Configurar las columnas
        for col in columns:
            # Obtener el rol de la columna actual
            role = roles.get(col, None)
            header_text = col
            if role == 'PK':
                header_text += " (PK)"
            elif role == 'FK':
                header_text += " (FK)"
            
            tree.heading(col, text=header_text)
            tree.column(col, width=150, anchor="w")  # Ajuste del ancho de columna

        # Insertar los datos
        for _, row in table_df.iterrows():
            tree.insert("", "end", values=list(row))

        tree.pack(fill="both", expand=True)

    # Limpiar el panel derecho
    clear_right_panel()

    # Agregar un Treeview por cada tabla
    for idx, (table_df, roles) in enumerate(zip(tables, roles_info)):
        frame = tk.Frame(right_panel_content)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Agregar un título para la tabla
        title_frame = tk.Frame(frame)
        title_frame.pack(fill="x")

        table_label = tk.Label(title_frame, text=f"Tabla {idx + 1}:", font=("Arial", 14, "bold"))
        table_label.pack(side="left", pady=(0, 10))

        # Campo de entrada para el nombre de la tabla
        name_entry = tk.Entry(title_frame)
        name_entry.insert(0, table_names[idx])  # Valor por defecto
        name_entry.pack(side="left", padx=10)

        # Botón para guardar el nombre
        save_button = ttk.Button(title_frame, text="Guardar", command=lambda idx=idx, entry=name_entry: save_table_name(idx, entry))
        save_button.pack(side="left")

        # Crear Treeview
        tree = ttk.Treeview(frame, columns=list(table_df.columns), show="headings")

        # Configurar las columnas
        for col in table_df.columns:
            header_text = col
            if roles.get(col) == 'PK':
                header_text += " (PK)"
            elif roles.get(col) == 'FK':
                header_text += " (FK)"
            
            tree.heading(col, text=header_text)
            tree.column(col, width=100, anchor="w")

        # Insertar los datos
        for _, row in table_df.iterrows():
            tree.insert("", "end", values=list(row))

        tree.pack(fill="both", expand=True)

def check_and_convert_1fn_action():
    """
    Acción para verificar y convertir tablas a 1FN.
    """
    global tables
    global roles_info
    converted_tables = check_and_convert_1fn(tables)
    
    # Actualiza la lista de tablas global y redibuja la interfaz
    tables = converted_tables
    display_tables(tables, roles_info)
    
    # Mensaje de éxito
    messagebox.showinfo("1FN", "Las tablas han sido convertidas a 1FN.")

def check_and_convert_2fn_action():
    """
    Acción para verificar y convertir tablas a 2FN.
    """
    global tables
    global roles_info
    converted_tables = check_and_convert_2fn(tables, roles_info)  
    
    # Actualiza la lista de tablas global y redibuja la interfaz
    tables = converted_tables
    display_tables(tables, roles_info)
    
    # Mensaje de éxito
    messagebox.showinfo("2FN", "Las tablas han sido convertidas a 2FN.")


def check_and_convert_3fn_action():
    """
    Acción para verificar y convertir tablas a 3FN.
    """
    global tables
    global roles_info
    converted_tables = check_and_convert_3fn(tables)
    
    # Actualiza la lista de tablas global y redibuja la interfaz
    tables = converted_tables
    display_tables(tables, roles_info)
    
    # Mensaje de éxito
    messagebox.showinfo("3FN", "Las tablas han sido convertidas a 3FN.")

def save_table_name(idx, entry):
    global table_names
    table_names[idx] = entry.get()
    print(f"Nombre de la Tabla {idx + 1} actualizado a: {table_names[idx]}")
    entry.config(state="readonly")
    # Deshabilitar el botón de guardar
    save_button = entry.master.winfo_children()[2]
    save_button.config(state="disabled")

if __name__ == "__main__":
    create_interface().mainloop()
