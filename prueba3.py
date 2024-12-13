import tkinter as tk
from tkinter import messagebox, filedialog
from sympy import symbols, diff, lambdify
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import threading
import time

# Definimos símbolos para sympy
t = symbols('t')

class MRUVApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicación MRUV y Derivadas")
        
        # Variables de entrada
        self.x0 = tk.DoubleVar()
        self.v0 = tk.DoubleVar()
        self.a = tk.DoubleVar()
        self.t = tk.DoubleVar()
        self.selected_formula = tk.StringVar(value="Posición")

        self.setup_ui()

    def setup_ui(self):
        # Crear diseño
        frame_inputs = tk.Frame(self.root, padx=10, pady=10)
        frame_inputs.pack(side=tk.LEFT, fill=tk.Y)

        frame_results = tk.Frame(self.root, padx=10, pady=10)
        frame_results.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Selector de fórmula
        tk.Label(frame_inputs, text="Seleccionar fórmula:").pack(anchor="w")
        formulas = ["Posición", "Velocidad", "Aceleración"]
        tk.OptionMenu(frame_inputs, self.selected_formula, *formulas, command=self.update_inputs).pack(anchor="w")

        # Entradas de valores
        self.inputs_frame = tk.Frame(frame_inputs)
        self.inputs_frame.pack(anchor="w", pady=10)
        self.update_inputs("Posición")

        # Botón para calcular
        tk.Button(frame_inputs, text="Calcular", command=self.calculate).pack(pady=10)

        # Canvas para gráficos
        self.figure = plt.Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=frame_results)
        self.canvas.get_tk_widget().pack()

        # Simulador de animación
        self.simulator_frame = tk.Frame(frame_results)
        self.simulator_frame.pack()
        self.sim_canvas = tk.Canvas(self.simulator_frame, width=500, height=100, bg="white")
        self.sim_canvas.pack()
        self.car_image = ImageTk.PhotoImage(Image.open("car.png").resize((50, 30)))
        self.car = self.sim_canvas.create_image(0, 50, anchor=tk.NW, image=self.car_image)

        # Botón para exportar resultados
        tk.Button(frame_inputs, text="Exportar Gráfico", command=self.export_graph).pack(pady=5)

    def update_inputs(self, formula):
        for widget in self.inputs_frame.winfo_children():
            widget.destroy()

        if formula == "Posición":
            tk.Label(self.inputs_frame, text="Posición inicial (x0):").pack(anchor="w")
            tk.Entry(self.inputs_frame, textvariable=self.x0).pack(anchor="w")

            tk.Label(self.inputs_frame, text="Velocidad inicial (v0):").pack(anchor="w")
            tk.Entry(self.inputs_frame, textvariable=self.v0).pack(anchor="w")

            tk.Label(self.inputs_frame, text="Aceleración (a):").pack(anchor="w")
            tk.Entry(self.inputs_frame, textvariable=self.a).pack(anchor="w")

            tk.Label(self.inputs_frame, text="Tiempo (t):").pack(anchor="w")
            tk.Entry(self.inputs_frame, textvariable=self.t).pack(anchor="w")
        elif formula == "Velocidad":
            tk.Label(self.inputs_frame, text="Velocidad inicial (v0):").pack(anchor="w")
            tk.Entry(self.inputs_frame, textvariable=self.v0).pack(anchor="w")

            tk.Label(self.inputs_frame, text="Aceleración (a):").pack(anchor="w")
            tk.Entry(self.inputs_frame, textvariable=self.a).pack(anchor="w")

            tk.Label(self.inputs_frame, text="Tiempo (t):").pack(anchor="w")
            tk.Entry(self.inputs_frame, textvariable=self.t).pack(anchor="w")
        elif formula == "Aceleración":
            tk.Label(self.inputs_frame, text="Aceleración constante (a):").pack(anchor="w")
            tk.Entry(self.inputs_frame, textvariable=self.a).pack(anchor="w")

    def calculate(self):
        try:
            formula = self.selected_formula.get()

            if formula == "Posición":
                self.solve_position()
            elif formula == "Velocidad":
                self.solve_velocity()
            elif formula == "Aceleración":
                self.solve_acceleration()

        except Exception as e:
            messagebox.showerror("Error", f"Entrada no válida: {e}")

    def solve_position(self):
        try:
            x0 = self.x0.get()
            v0 = self.v0.get()
            a = self.a.get()
            t_val = self.t.get()

            position_eq = x0 + v0 * t + 0.5 * a * t**2
            velocity_eq = diff(position_eq, t)

            position_func = lambdify(t, position_eq)
            velocity_func = lambdify(t, velocity_eq)

            pos = position_func(t_val)
            vel = velocity_func(t_val)

            step_by_step = (
                f"Paso 1: Ecuación de posición -> s(t) = {position_eq}\n"
                f"Paso 2: Derivar s(t) para obtener v(t) -> v(t) = {velocity_eq}\n"
                f"Paso 3: Evaluar en t={t_val}\n"
                f"Posición: {pos:.2f} m, Velocidad: {vel:.2f} m/s"
            )

            self.plot_graph(position_eq, velocity_eq, highlight_t=t_val)
            messagebox.showinfo("Resultado: Posición", step_by_step)

        except Exception as e:
            messagebox.showerror("Error", f"Error en cálculo: {e}")

    def solve_velocity(self):
        try:
            v0 = self.v0.get()
            a = self.a.get()
            t_val = self.t.get()

            velocity_eq = v0 + a * t

            velocity_func = lambdify(t, velocity_eq)
            vel = velocity_func(t_val)

            step_by_step = (
                f"Paso 1: Ecuación de velocidad -> v(t) = {velocity_eq}\n"
                f"Paso 2: Evaluar en t={t_val}\n"
                f"Velocidad: {vel:.2f} m/s"
            )

            self.plot_graph(velocity_eq, diff(velocity_eq, t), highlight_t=t_val)
            messagebox.showinfo("Resultado: Velocidad", step_by_step)

        except Exception as e:
            messagebox.showerror("Error", f"Error en cálculo: {e}")

    def solve_acceleration(self):
        try:
            a = self.a.get()
            step_by_step = f"La aceleración es constante y su valor es {a:.2f} m/s²"
            messagebox.showinfo("Resultado: Aceleración", step_by_step)

        except Exception as e:
            messagebox.showerror("Error", f"Error en cálculo: {e}")
    def plot_graph(self, position_eq=None, velocity_eq=None, highlight_t=None):
        try:
            self.ax.clear()

            if position_eq:
                position_func = lambdify(t, position_eq)
                t_vals = [i * 0.1 for i in range(0, 51)]
                position_vals = [position_func(i) for i in t_vals]
                self.ax.plot(t_vals, position_vals, label="s(t): Posición", color="blue")

            if velocity_eq:
                velocity_func = lambdify(t, velocity_eq)
                t_vals = [i * 0.1 for i in range(0, 51)]
                velocity_vals = [velocity_func(i) for i in t_vals]
                self.ax.plot(t_vals, velocity_vals, label="v(t): Velocidad", color="red")

            if highlight_t is not None:
                if position_eq:
                    pos_highlight = position_func(highlight_t)
                    self.ax.scatter([highlight_t], [pos_highlight], color="blue", label=f"s({highlight_t})")
                if velocity_eq:
                    vel_highlight = velocity_func(highlight_t)
                    self.ax.scatter([highlight_t], [vel_highlight], color="red", label=f"v({highlight_t})")

            self.ax.axhline(0, color="black", linewidth=0.5, linestyle="--")
            self.ax.set_xlabel("Tiempo (t)")
            self.ax.set_ylabel("Magnitud")
            self.ax.legend()
            self.ax.grid()
            self.canvas.draw()

        except Exception as e:
            messagebox.showerror("Error", f"Error al graficar: {e}")

    def export_graph(self):
        try:
            filepath = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
            )
            if filepath:
                self.figure.savefig(filepath)
                messagebox.showinfo("Éxito", f"Gráfico exportado con éxito a: {filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar el gráfico: {e}")

    def animate_car(self, velocity):
        try:
            self.sim_canvas.coords(self.car, 0, 50)  # Reset car position
            distance = 0

            for _ in range(100):
                distance += velocity * 0.1  # Simular movimiento
                self.sim_canvas.coords(self.car, distance, 50)
                time.sleep(0.1)
        except Exception as e:
            print(f"Error en animación: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MRUVApp(root)
    root.mainloop()

