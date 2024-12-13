import tkinter as tk
from tkinter import messagebox
from sympy import symbols, diff, lambdify, solve, integrate
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

        self.setup_ui()

    def setup_ui(self):
        # Crear diseño
        frame_inputs = tk.Frame(self.root, padx=10, pady=10)
        frame_inputs.pack(side=tk.LEFT, fill=tk.Y)

        frame_results = tk.Frame(self.root, padx=10, pady=10)
        frame_results.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Botones para problemas
        tk.Label(frame_inputs, text="Problemas predefinidos:").pack(anchor="w")
        tk.Button(frame_inputs, text="Problema 1: Velocidad en t=3", command=self.solve_problem1).pack(anchor="w")
        tk.Button(frame_inputs, text="Problema 2: Objeto detenido", command=self.solve_problem2).pack(anchor="w")
        tk.Button(frame_inputs, text="Problema 3: Altura máxima", command=self.solve_problem3).pack(anchor="w")
        tk.Button(frame_inputs, text="Problema 4: Aceleración constante", command=self.solve_problem4).pack(anchor="w")
        tk.Button(frame_inputs, text="Problema 5: Distancia total", command=self.solve_problem5).pack(anchor="w")

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

    def solve_problem1(self):
        # Problema 1: Velocidad en t=3
        try:
            position_eq = 5 * t**2 - 20 * t + 50
            velocity_eq = diff(position_eq, t)

            velocity_func = lambdify(t, velocity_eq)
            vel_at_3 = velocity_func(3)

            step_by_step = (
                f"Paso 1: Derivar la función de posición s(t) = {position_eq}\n"
                f"Resultado: v(t) = {velocity_eq}\n"
                f"Paso 2: Sustituir t=3 en v(t)\n"
                f"Velocidad en t=3: {vel_at_3} m/s"
            )

            result_text = (
                f"Función de posición: s(t) = {position_eq}\n"
                f"Función de velocidad: v(t) = {velocity_eq}\n"
                f"{step_by_step}"
            )

            self.plot_graph(position_eq, velocity_eq, highlight_t=3)
            messagebox.showinfo("Problema 1: Resultado", result_text)

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def solve_problem2(self):
        # Problema 2: Momento en que el objeto se detiene
        try:
            position_eq = -4.9 * t**2 + 19.6 * t
            velocity_eq = diff(position_eq, t)

            stop_time = solve(velocity_eq, t)

            step_by_step = (
                f"Paso 1: Derivar la función de posición s(t) = {position_eq}\n"
                f"Resultado: v(t) = {velocity_eq}\n"
                f"Paso 2: Resolver v(t) = 0\n"
                f"Tiempo en que el objeto se detiene: t = {stop_time} s"
            )

            result_text = (
                f"Función de posición: s(t) = {position_eq}\n"
                f"Función de velocidad: v(t) = {velocity_eq}\n"
                f"{step_by_step}"
            )

            self.plot_graph(position_eq, velocity_eq, highlight_t=stop_time[0])
            messagebox.showinfo("Problema 2: Resultado", result_text)

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def solve_problem3(self):
        # Problema 3: Máxima altura de un proyectil
        try:
            position_eq = -4.9 * t**2 + 30 * t + 10
            velocity_eq = diff(position_eq, t)

            max_height_time = solve(velocity_eq, t)[0]
            position_func = lambdify(t, position_eq)
            max_height = position_func(max_height_time)

            step_by_step = (
                f"Paso 1: Derivar la función de posición s(t) = {position_eq}\n"
                f"Resultado: v(t) = {velocity_eq}\n"
                f"Paso 2: Resolver v(t) = 0 para encontrar el tiempo de altura máxima\n"
                f"Tiempo: t = {max_height_time} s\n"
                f"Paso 3: Sustituir t en s(t) para calcular la altura máxima\n"
                f"Altura máxima: {max_height} m"
            )

            result_text = (
                f"Función de posición: s(t) = {position_eq}\n"
                f"Función de velocidad: v(t) = {velocity_eq}\n"
                f"{step_by_step}"
            )

            self.plot_graph(position_eq, velocity_eq, highlight_t=max_height_time)
            messagebox.showinfo("Problema 3: Resultado", result_text)

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def solve_problem4(self):
        # Problema 4: Aceleración constante
        try:
            velocity_eq = 8 * t - 16
            acceleration_eq = diff(velocity_eq, t)

            position_eq = integrate(velocity_eq, t) + 5

            step_by_step = (
                f"Paso 1: Derivar la función de velocidad v(t) = {velocity_eq}\n"
                f"Resultado: a(t) = {acceleration_eq}\n"
                f"Paso 2: Integrar v(t) para encontrar la posición s(t)\n"
                f"Función de posición: s(t) = {position_eq}"
            )

            result_text = (
                f"Función de velocidad: v(t) = {velocity_eq}\n"
                f"Aceleración: a(t) = {acceleration_eq} (constante)\n"
                f"Función de posición: s(t) = {position_eq}\n"
                f"{step_by_step}"
            )

            self.plot_graph(position_eq, velocity_eq)
            messagebox.showinfo("Problema 4: Resultado", result_text)

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def solve_problem5(self):
        # Problema 5: Distancia recorrida en un intervalo
        try:
            position_eq = 3 * t**2 - 12 * t + 20
            velocity_eq = diff(position_eq, t)

            critical_points = solve(velocity_eq, t)
            critical_points = [p for p in critical_points if 0 <= p <= 4]

            position_func = lambdify(t, position_eq)

            distance = 0
            last_point = 0
            for point in critical_points + [4]:
                distance += abs(position_func(point) - position_func(last_point))
                last_point = point

            step_by_step = (
                f"Paso 1: Derivar la función de posición s(t) = {position_eq}\n"
                f"Resultado: v(t) = {velocity_eq}\n"
                f"Paso 2: Encontrar los puntos críticos donde v(t) cambia de signo"
                f"Puntos críticos en [0, 4]: {critical_points}"
                f"Paso 3: Calcular las distancias absolutas entre los tramos:"
            )

            last_point = 0
            detailed_distances = []
            for point in critical_points + [4]:
                segment_distance = abs(position_func(point) - position_func(last_point))
                detailed_distances.append(
                    f"Distancia entre t={last_point} y t={point}: {segment_distance} m"
                )
                distance += segment_distance
                last_point = point

            step_by_step += "\n".join(detailed_distances)
            step_by_step += f"\n\nDistancia total recorrida: {distance} m"

            result_text = (
                f"Función de posición: s(t) = {position_eq}\n"
                f"Función de velocidad: v(t) = {velocity_eq}\n"
                f"{step_by_step}"
            )

            self.plot_graph(position_eq, velocity_eq)
            messagebox.showinfo("Problema 5: Resultado", result_text)

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def plot_graph(self, position_eq, velocity_eq, highlight_t=None):
        try:
            self.ax.clear()

            position_func = lambdify(t, position_eq)
            velocity_func = lambdify(t, velocity_eq)

            t_vals = [i * 0.1 for i in range(0, 51)]  # Intervalo de tiempo de 0 a 5 segundos
            position_vals = [position_func(i) for i in t_vals]
            velocity_vals = [velocity_func(i) for i in t_vals]

            self.ax.plot(t_vals, position_vals, label="s(t): Posición", color="blue")
            self.ax.plot(t_vals, velocity_vals, label="v(t): Velocidad", color="red")

            if highlight_t is not None:
                pos_highlight = position_func(highlight_t)
                vel_highlight = velocity_func(highlight_t)
                self.ax.scatter([highlight_t], [pos_highlight], color="blue", label=f"s({highlight_t})")
                self.ax.scatter([highlight_t], [vel_highlight], color="red", label=f"v({highlight_t})")

            self.ax.axhline(0, color="black", linewidth=0.5, linestyle="--")
            self.ax.set_xlabel("Tiempo (t)")
            self.ax.set_ylabel("Magnitud")
            self.ax.legend()
            self.ax.grid()
            self.canvas.draw()

        except Exception as e:
            messagebox.showerror("Error", f"Error al graficar: {e}")

# Crear la aplicación tkinter
if __name__ == "__main__":
    root = tk.Tk()
    app = MRUVApp(root)
    root.mainloop()
