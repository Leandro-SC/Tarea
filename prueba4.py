import tkinter as tk
from tkinter import messagebox, filedialog
from sympy import symbols, diff, lambdify, solve
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import json
import os

# Definimos símbolos para sympy
t, x = symbols('t x')

class MRUVApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicación MRUV y Derivadas")

        # Variables
        self.x0 = tk.DoubleVar()
        self.v0 = tk.DoubleVar()
        self.a = tk.DoubleVar()
        self.time = tk.DoubleVar()
        self.selected_formula = tk.StringVar(value="position")
        self.history = []  # Historial de resultados

        self.setup_ui()

    def setup_ui(self):
        # Crear diseño
        frame_inputs = tk.Frame(self.root, padx=10, pady=10)
        frame_inputs.pack(side=tk.LEFT, fill=tk.Y)

        frame_results = tk.Frame(self.root, padx=10, pady=10)
        frame_results.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Selección de fórmula
        tk.Label(frame_inputs, text="Seleccionar fórmula:").pack(anchor="w")
        tk.Radiobutton(frame_inputs, text="Posición", variable=self.selected_formula, value="position", command=self.update_inputs).pack(anchor="w")
        tk.Radiobutton(frame_inputs, text="Velocidad", variable=self.selected_formula, value="velocity", command=self.update_inputs).pack(anchor="w")
        tk.Radiobutton(frame_inputs, text="Aceleración", variable=self.selected_formula, value="acceleration", command=self.update_inputs).pack(anchor="w")

        # Entradas dinámicas
        self.inputs_frame = tk.Frame(frame_inputs)
        self.inputs_frame.pack(anchor="w")

        self.update_inputs()

        # Botón para calcular
        tk.Button(frame_inputs, text="Calcular", command=self.calculate).pack(pady=10)

        # Botón para exportar gráficos
        tk.Button(frame_inputs, text="Exportar Gráfico", command=self.export_graph).pack(pady=5)

        # Botón para exportar historial
        tk.Button(frame_inputs, text="Exportar Historial", command=self.export_history).pack(pady=5)

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

    def update_inputs(self):
        for widget in self.inputs_frame.winfo_children():
            widget.destroy()

        if self.selected_formula.get() == "position":
            tk.Label(self.inputs_frame, text="Posición inicial (x0):").pack(anchor="w")
            tk.Entry(self.inputs_frame, textvariable=self.x0).pack(anchor="w")

            tk.Label(self.inputs_frame, text="Velocidad inicial (v0):").pack(anchor="w")
            tk.Entry(self.inputs_frame, textvariable=self.v0).pack(anchor="w")

            tk.Label(self.inputs_frame, text="Aceleración (a):").pack(anchor="w")
            tk.Entry(self.inputs_frame, textvariable=self.a).pack(anchor="w")

            tk.Label(self.inputs_frame, text="Tiempo (t):").pack(anchor="w")
            tk.Entry(self.inputs_frame, textvariable=self.time).pack(anchor="w")

        elif self.selected_formula.get() == "velocity":
            tk.Label(self.inputs_frame, text="Velocidad inicial (v0):").pack(anchor="w")
            tk.Entry(self.inputs_frame, textvariable=self.v0).pack(anchor="w")

            tk.Label(self.inputs_frame, text="Aceleración (a):").pack(anchor="w")
            tk.Entry(self.inputs_frame, textvariable=self.a).pack(anchor="w")

            tk.Label(self.inputs_frame, text="Tiempo (t):").pack(anchor="w")
            tk.Entry(self.inputs_frame, textvariable=self.time).pack(anchor="w")

        elif self.selected_formula.get() == "acceleration":
            tk.Label(self.inputs_frame, text="Aceleración constante (a):").pack(anchor="w")
            tk.Entry(self.inputs_frame, textvariable=self.a).pack(anchor="w")

    def calculate(self):
        try:
            result_entry = {}

            if self.selected_formula.get() == "position":
                x0 = self.x0.get()
                v0 = self.v0.get()
                a = self.a.get()
                t_val = self.time.get()

                position_eq = x0 + v0 * t + 0.5 * a * t**2
                velocity_eq = diff(position_eq, t)

                position_func = lambdify(t, position_eq)
                velocity_func = lambdify(t, velocity_eq)

                pos = position_func(t_val)
                vel = velocity_func(t_val)

                result_text = (
                    f"Fórmula de posición: s(t) = {position_eq}\n"
                    f"Fórmula de velocidad: v(t) = {velocity_eq}\n"
                    f"\nResultados:\n"
                    f"Posición en t={t_val}: {pos:.2f} m\n"
                    f"Velocidad en t={t_val}: {vel:.2f} m/s\n"
                )

                result_entry = {
                    "formula": "position",
                    "position_formula": str(position_eq),
                    "velocity_formula": str(velocity_eq),
                    "time": t_val,
                    "position": pos,
                    "velocity": vel
                }

                messagebox.showinfo("Resultados", result_text)

                self.plot_graph(position_eq, velocity_eq, highlight_t=t_val)

            elif self.selected_formula.get() == "velocity":
                v0 = self.v0.get()
                a = self.a.get()
                t_val = self.time.get()

                velocity_eq = v0 + a * t
                velocity_func = lambdify(t, velocity_eq)

                vel = velocity_func(t_val)

                result_text = (
                    f"Fórmula de velocidad: v(t) = {velocity_eq}\n"
                    f"\nResultados:\n"
                    f"Velocidad en t={t_val}: {vel:.2f} m/s\n"
                )

                result_entry = {
                    "formula": "velocity",
                    "velocity_formula": str(velocity_eq),
                    "time": t_val,
                    "velocity": vel
                }

                messagebox.showinfo("Resultados", result_text)

                self.plot_graph(None, velocity_eq, highlight_t=t_val)

            elif self.selected_formula.get() == "acceleration":
                a = self.a.get()

                result_text = f"La aceleración es constante y su valor es: {a:.2f} m/s²"

                result_entry = {
                    "formula": "acceleration",
                    "acceleration": a
                }

                messagebox.showinfo("Resultados", result_text)

            self.history.append(result_entry)
            self.save_history()

        except Exception as e:
            messagebox.showerror("Error", f"Entrada no válida: {e}")

    def plot_graph(self, position_eq=None, velocity_eq=None, highlight_t=None):
        try:
            self.ax.clear()

            # Graficar la ecuación de posición
            if position_eq:
                position_func = lambdify(t, position_eq)
                t_vals = [i * 0.1 for i in range(0, 101)]
                position_vals = [position_func(i) for i in t_vals]
                self.ax.plot(t_vals, position_vals, label="s(t): Posición", color="blue")

            # Graficar la ecuación de velocidad
            if velocity_eq:
                velocity_func = lambdify(t, velocity_eq)
                t_vals = [i * 0.1 for i in range(0, 101)]
                velocity_vals = [velocity_func(i) for i in t_vals]
                self.ax.plot(t_vals, velocity_vals, label="v(t): Velocidad", color="green")

            # Destacar un punto específico en los gráficos
            if highlight_t is not None:
                if position_eq:
                    position_at_t = lambdify(t, position_eq)(highlight_t)
                    self.ax.scatter(highlight_t, position_at_t, color="blue", label=f"s({highlight_t:.1f})")
                if velocity_eq:
                    velocity_at_t = lambdify(t, velocity_eq)(highlight_t)
                    self.ax.scatter(highlight_t, velocity_at_t, color="green", label=f"v({highlight_t:.1f})")

            # Configuración del gráfico
            self.ax.axhline(0, color='black', linewidth=0.5, linestyle="--")
            self.ax.axvline(0, color='black', linewidth=0.5, linestyle="--")
            self.ax.set_title("Gráfico MRUV")
            self.ax.set_xlabel("Tiempo (s)")
            self.ax.set_ylabel("Valor")
            self.ax.legend()
            self.ax.grid(True)

            # Dibujar el gráfico
            self.canvas.draw()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el gráfico: {e}")


    def export_graph(self):
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
            )
            if file_path:
                self.figure.savefig(file_path)
                messagebox.showinfo("Exportación exitosa", "El gráfico se ha exportado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar el gráfico: {e}")


    def export_history(self):
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(self.history, file, ensure_ascii=False, indent=4)
                messagebox.showinfo("Exportación exitosa", "El historial se ha exportado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar el historial: {e}")


    def save_history(self):
        try:
            with open("history.json", "w", encoding="utf-8") as file:
                json.dump(self.history, file, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el historial: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = MRUVApp(root)
    root.mainloop()




                                                                                                









































