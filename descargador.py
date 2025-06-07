import os
import subprocess
import tkinter as tk
from tkinter import messagebox

def descargar():
    link = entrada_enlace.get().strip()
    formato = formato_var.get()

    if not link.startswith("http"):
        messagebox.showerror("Error", "❌ Enlace inválido.")
        return

    carpeta_salida = "descargas"
    os.makedirs(carpeta_salida, exist_ok=True)

    opciones_comunes = [
        "--no-playlist",
        "-o", os.path.join(carpeta_salida, "%(title)s.%(ext)s")
    ]

    if formato == "musica":
        comando = [
            "yt-dlp", "-x", "--audio-format", "mp3"
        ] + opciones_comunes + [link]
    elif formato == "video":
        comando = [
            "yt-dlp", "-f", "bestvideo+bestaudio"
        ] + opciones_comunes + [link]
    else:
        messagebox.showerror("Error", "❌ Selecciona un formato válido.")
        return

    try:
        estado.set("⏳ Descargando...")
        ventana.update()
        subprocess.run(comando, check=True)
        estado.set("✅ Descarga completada en la carpeta 'descargas'.")
    except subprocess.CalledProcessError as e:
        estado.set("❌ Error en la descarga.")
        messagebox.showerror("Error", str(e))


# Interfaz gráfica con tkinter
ventana = tk.Tk()
ventana.title("Descargador de Música y Video")
ventana.geometry("450x250")
ventana.resizable(False, False)

tk.Label(ventana, text="🎬 Ingresa el enlace:", font=("Arial", 12)).pack(pady=10)
entrada_enlace = tk.Entry(ventana, width=50, font=("Arial", 11))
entrada_enlace.pack()

formato_var = tk.StringVar(value="musica")

tk.Label(ventana, text="🎵 Selecciona formato:", font=("Arial", 12)).pack(pady=10)
frame_botones = tk.Frame(ventana)
frame_botones.pack()

tk.Radiobutton(frame_botones, text="Música (MP3)", variable=formato_var, value="musica").pack(side="left", padx=10)
tk.Radiobutton(frame_botones, text="Video (MP4)", variable=formato_var, value="video").pack(side="left", padx=10)

tk.Button(ventana, text="⬇ Descargar", command=descargar, bg="green", fg="white", font=("Arial", 12)).pack(pady=15)

estado = tk.StringVar()
tk.Label(ventana, textvariable=estado, font=("Arial", 10), fg="blue").pack(pady=5)

ventana.mainloop()
