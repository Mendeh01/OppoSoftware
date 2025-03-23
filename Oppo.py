import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

def conectar_db():
    conn = sqlite3.connect("ventas.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    imei TEXT,
    modelo TEXT,
    vendedor TEXT,
    fecha TEXT)''')
    conn.commit()
    conn.close()

def mostrar_mensaje(tipo, titulo, mensaje):
    msg_box = tk.Toplevel(root)
    msg_box.title(titulo)
    msg_box.configure(bg="#2E2E2E")
    
    tk.Label(msg_box, text=mensaje, fg="white", bg="#2E2E2E").pack(padx=20, pady=10)
    tk.Button(msg_box, text="Aceptar", command=msg_box.destroy, bg="#3B3B3B", fg="white").pack(pady=10)
    
    msg_box.transient(root)
    msg_box.grab_set()
    root.wait_window(msg_box)

def registrar_venta():
    imei = entry_imei.get()
    modelo = entry_modelo.get()
    vendedor = entry_vendedor.get()
    fecha = datetime.now().strftime("%Y-%m-%d")
    
    if not imei or not modelo or not vendedor:
        mostrar_mensaje("warning", "Advertencia", "Todos los campos son obligatorios")
        return
    
    conn = sqlite3.connect("ventas.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ventas (imei, modelo, vendedor, fecha) VALUES (?, ?, ?, ?)",
    (imei, modelo, vendedor, fecha))
    conn.commit()
    conn.close()
    mostrar_mensaje("info", "Éxito", "Venta registrada correctamente")
    actualizar_lista()

def actualizar_lista():
    for row in tree.get_children():
        tree.delete(row)
    conn = sqlite3.connect("ventas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ventas")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)
    conn.close()

def editar_venta():
    selected_item = tree.selection()
    if not selected_item:
        mostrar_mensaje("warning", "Advertencia", "Selecciona una venta para editar")
        return
    
    item = tree.item(selected_item)
    id_venta = item['values'][0]
    imei_nuevo = entry_imei.get()
    modelo_nuevo = entry_modelo.get()
    vendedor_nuevo = entry_vendedor.get()
    
    if not imei_nuevo or not modelo_nuevo or not vendedor_nuevo:
        mostrar_mensaje("warning", "Advertencia", "Todos los campos son obligatorios")
        return
    
    conn = sqlite3.connect("ventas.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE ventas SET imei=?, modelo=?, vendedor=? WHERE id=?",
    (imei_nuevo, modelo_nuevo, vendedor_nuevo, id_venta))
    conn.commit()
    conn.close()
    mostrar_mensaje("info", "Éxito", "Venta editada correctamente")
    actualizar_lista()

def eliminar_venta():
    selected_item = tree.selection()
    if not selected_item:
        mostrar_mensaje("warning", "Advertencia", "Selecciona una venta para eliminar")
        return
    
    item = tree.item(selected_item)
    id_venta = item['values'][0]
    
    conn = sqlite3.connect("ventas.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ventas WHERE id=?", (id_venta,))
    conn.commit()
    conn.close()
    mostrar_mensaje("info", "Éxito", "Venta eliminada correctamente")
    actualizar_lista()

# Interfaz gráfica
root = tk.Tk()
root.title("Oppo Software")
root.configure(bg="#2E2E2E")

conectar_db()

frame = tk.Frame(root, bg="#2E2E2E")
frame.pack(pady=10)

tk.Label(frame, text="IMEI:", fg="white", bg="#2E2E2E").grid(row=0, column=0)
entry_imei = tk.Entry(frame, bg="#424242", fg="white", insertbackground="white")
entry_imei.grid(row=0, column=1)

tk.Label(frame, text="Modelo:", fg="white", bg="#2E2E2E").grid(row=1, column=0)
entry_modelo = tk.Entry(frame, bg="#424242", fg="white", insertbackground="white")
entry_modelo.grid(row=1, column=1)

tk.Label(frame, text="Vendedor:", fg="white", bg="#2E2E2E").grid(row=2, column=0)
entry_vendedor = tk.Entry(frame, bg="#424242", fg="white", insertbackground="white")
entry_vendedor.grid(row=2, column=1)

btn_registrar = tk.Button(frame, text="Registrar Venta", command=registrar_venta, bg="#3B3B3B", fg="white")
btn_registrar.grid(row=3, column=0, columnspan=2, pady=5)

btn_editar = tk.Button(frame, text="Editar Venta", command=editar_venta, bg="#3B3B3B", fg="white")
btn_editar.grid(row=4, column=0, columnspan=2, pady=5)

btn_eliminar = tk.Button(frame, text="Eliminar Venta", command=eliminar_venta, bg="#3B3B3B", fg="white")
btn_eliminar.grid(row=5, column=0, columnspan=2, pady=5)

# Tabla de ventas
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background="#2E2E2E", foreground="white", fieldbackground="#2E2E2E", borderwidth=0)
style.configure("Treeview.Heading", background="#3B3B3B", foreground="white", font=("Arial", 10, "bold"))
style.map("Treeview", background=[("selected", "#555555")])

tree = ttk.Treeview(root, columns=("ID", "IMEI", "Modelo", "Vendedor", "Fecha"), show="headings")
for col in ("ID", "IMEI", "Modelo", "Vendedor", "Fecha"):
    tree.heading(col, text=col)
    tree.column(col, width=100)
tree.pack(pady=10)

actualizar_lista()

root.mainloop()