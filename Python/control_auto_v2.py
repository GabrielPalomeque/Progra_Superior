import tkinter as tk
from tkinter import ttk, messagebox
import serial
import serial.tools.list_ports
import time

class AutoInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Panel de Control - Auto Robot")
        self.root.geometry("500x650") # Un poco más alto para el nuevo botón
        
        self.arduino = None
        self.conectado = False
        self.ultima_tecla = None
        self.modo_actual = "NINGUNO"

        # --- ESTILOS ---
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 11), padding=6)
        style.configure("Grande.TButton", font=("Arial", 12, "bold"))
        style.configure("Luz.TButton", font=("Arial", 11, "bold"), foreground="blue")

        # --- SECCIÓN 1: CONEXIÓN ---
        self.frame_conn = ttk.LabelFrame(self.root, text="1. Configuración de Conexión", padding=10)
        self.frame_conn.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(self.frame_conn, text="Puerto COM:").pack(side="left")
        self.combo_ports = ttk.Combobox(self.frame_conn, width=15, state="readonly")
        self.combo_ports.pack(side="left", padx=5)
        
        self.btn_refresh = ttk.Button(self.frame_conn, text="↻", width=3, command=self.listar_puertos)
        self.btn_refresh.pack(side="left")
        
        self.btn_connect = ttk.Button(self.frame_conn, text="Conectar", command=self.toggle_conexion)
        self.btn_connect.pack(side="left", padx=10)

        # --- SECCIÓN 2: MODO ---
        self.frame_mode = ttk.LabelFrame(self.root, text="2. Selección de Modo", padding=10)
        self.frame_mode.pack(fill="x", padx=10, pady=5)
        
        self.btn_serial = ttk.Button(self.frame_mode, text="MODO CABLEADO (USB) [T]", 
                                     command=lambda: self.set_modo('T'))
        self.btn_serial.pack(side="left", expand=True, fill="x", padx=2)
        
        self.btn_bt = ttk.Button(self.frame_mode, text="MODO BLUETOOTH [Y]", 
                                 command=lambda: self.set_modo('Y'))
        self.btn_bt.pack(side="left", expand=True, fill="x", padx=2)

        # --- SECCIÓN 3: CONTROLES ---
        self.frame_ctrl = ttk.LabelFrame(self.root, text="3. Mando de Control", padding=20)
        self.frame_ctrl.pack(expand=True, fill="both", padx=10, pady=5)

        # -- Botones de Dirección --
        self.btn_w = ttk.Button(self.frame_ctrl, text="▲\nAdelante (W)", style="Grande.TButton", 
                                command=lambda: self.enviar('W'))
        self.btn_w.grid(row=0, column=1, pady=10)

        self.btn_a = ttk.Button(self.frame_ctrl, text="◄\nIzq (A)", style="Grande.TButton", 
                                command=lambda: self.enviar('A'))
        self.btn_a.grid(row=1, column=0, padx=5)

        self.btn_s = ttk.Button(self.frame_ctrl, text="▼\nAtrás (S)", style="Grande.TButton", 
                                command=lambda: self.enviar('S'))
        self.btn_s.grid(row=1, column=1, padx=5)

        self.btn_d = ttk.Button(self.frame_ctrl, text="►\nDer (D)", style="Grande.TButton", 
                                command=lambda: self.enviar('D'))
        self.btn_d.grid(row=1, column=2, padx=5)

        ttk.Separator(self.frame_ctrl, orient='horizontal').grid(row=2, column=0, columnspan=3, pady=20, sticky='ew')

        # -- Botones de Luces y Freno --
        self.btn_e = ttk.Button(self.frame_ctrl, text="Guiñador Izq (E)", 
                                command=lambda: self.enviar('E'))
        self.btn_e.grid(row=3, column=0)

        self.btn_stop = ttk.Button(self.frame_ctrl, text="STOP (Espacio)", style="Grande.TButton", 
                                   command=lambda: self.enviar(' '))
        self.btn_stop.grid(row=3, column=1)

        self.btn_q = ttk.Button(self.frame_ctrl, text="Guiñador Der (Q)", 
                                command=lambda: self.enviar('Q'))
        self.btn_q.grid(row=3, column=2)

        # -- NUEVO BOTÓN PARA FAROLES --
        self.btn_r = ttk.Button(self.frame_ctrl, text="💡 FAROLES (R) 💡", style="Luz.TButton", 
                                command=lambda: self.enviar('R'))
        self.btn_r.grid(row=4, column=0, columnspan=3, pady=15, sticky="ew")

        # Barra de estado
        self.lbl_status = ttk.Label(self.root, text="Estado: Desconectado", relief="sunken", anchor="w")
        self.lbl_status.pack(side="bottom", fill="x")

        # Eventos de teclado
        self.root.bind('<KeyPress>', self.on_key_press)
        self.root.bind('<KeyRelease>', self.on_key_release)
        
        self.listar_puertos()

    def listar_puertos(self):
        ports = serial.tools.list_ports.comports()
        self.combo_ports['values'] = [p.device for p in ports]
        if ports: self.combo_ports.current(0)

    def toggle_conexion(self):
        if not self.conectado:
            try:
                port = self.combo_ports.get()
                self.arduino = serial.Serial(port, 9600, timeout=1)
                self.conectado = True
                self.btn_connect.config(text="Desconectar")
                self.lbl_status.config(text=f"Conectado a {port}. Seleccione MODO.")
                self.frame_conn.config(text=f"1. Conexión ({port}) - OK")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo conectar: {e}")
        else:
            if self.arduino: self.arduino.close()
            self.conectado = False
            self.btn_connect.config(text="Conectar")
            self.lbl_status.config(text="Desconectado")
            self.modo_actual = "NINGUNO"

    def set_modo(self, modo):
        if not self.conectado:
            messagebox.showwarning("Error", "Primero conecta el puerto.")
            return
        
        self.enviar(modo)
        if modo == 'T':
            self.modo_actual = "SERIAL"
            self.lbl_status.config(text="MODO: CABLEADO (USB). Listo para conducir.")
        elif modo == 'Y':
            self.modo_actual = "BLUETOOTH"
            msg = ("Modo Inalámbrico activado en Arduino.\n\n"
                   "PASOS PARA BLUETOOTH:\n"
                   "1. Desconecta este programa (botón Desconectar).\n"
                   "2. Desenchufa el cable USB del auto.\n"
                   "3. Conecta batería al auto.\n"
                   "4. En 'Puerto COM', busca el puerto de tu Bluetooth.\n"
                   "5. Dale a Conectar de nuevo.")
            messagebox.showinfo("Cambio a Bluetooth", msg)
            self.lbl_status.config(text="MODO: Esperando conexión Bluetooth...")

    def enviar(self, char):
        if self.conectado and self.arduino:
            try:
                self.arduino.write(char.encode())
                # print(f"Enviado: {char}") 
            except:
                self.lbl_status.config(text="Error enviando datos")

    def on_key_press(self, event):
        key = event.char.upper()
        # Permitir activar modo con teclado
        if key == 'Y' and self.modo_actual == "NINGUNO": self.set_modo('Y'); return
        if key == 'T' and self.modo_actual == "NINGUNO": self.set_modo('T'); return

        # Agregamos 'R' a las teclas permitidas
        if key in ['W', 'A', 'S', 'D', 'Q', 'E', 'R', ' ']:
            if self.ultima_tecla != key:
                self.enviar(key)
                self.ultima_tecla = key

    def on_key_release(self, event):
        key = event.char.upper()
        if key in ['W', 'A', 'S', 'D']: # Solo frenar si soltamos teclas de movimiento
            self.enviar(' ')
            self.ultima_tecla = None

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoInterface(root)
    root.mainloop()