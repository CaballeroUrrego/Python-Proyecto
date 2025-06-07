import os
import subprocess
import tkinter as tk
from tkinter import messagebox

def detectar_plataforma(link):
    if "tiktok.com" in link:
        return "tiktok"
    elif "facebook.com" in link or "fb.watch" in link:
        return "facebook"
    elif "instagram.com" in link:
        return "instagram"
    elif "youtube.com" in link or "youtu.be" in link:
        return "youtube"
    else:
        return "desconocido"

def descargar():
    link = entrada_enlace.get().strip()
    formato = formato_var.get()

    if not link.startswith("http"):
        messagebox.showerror("Error", "❌ Enlace inválido.")
        return

    plataforma = detectar_plataforma(link)
    if plataforma == "desconocido":
        messagebox.showerror("Error", "❌ Plataforma no soportada.")
        return

    carpeta_salida = "descargas"
    os.makedirs(carpeta_salida, exist_ok=True)

    opciones_comunes = [
        "--no-playlist",
        "-o", os.path.join(carpeta_salida, "%(title)s.%(ext)s")
    ]

    comando = ["yt-dlp"]

    if plataforma == "tiktok":
        if formato == "musica":
            comando += ["-x", "--audio-format", "mp3"]
        else:
            comando += ["-f", "best"]
    elif plataforma in ["facebook", "instagram", "youtube"]:
        if formato == "musica":
            comando += ["-x", "--audio-format", "mp3"]
        else:
            comando += ["-f", "bestvideo+bestaudio/best"]
    else:
        messagebox.showerror("Error", "❌ Plataforma no soportada.")
        return

    comando += opciones_comunes + [link]

    try:
        estado.set("⏳ Descargando...")
        ventana.update()
        subprocess.run(comando, check=True)
        estado.set("✅ Descarga completada.")
        estado_label.config(fg="#00ff88")
    except subprocess.CalledProcessError as e:
        estado.set("❌ Error en la descarga.")
        estado_label.config(fg="#ff4444")
        messagebox.showerror("Error", str(e))

# 🎨 MODO OSCURO - COLORES
fondo = "#121212"
texto_claro = "#e0e0e0"
acento = "#00ff88"
boton_color = "#1f1f1f"
borde = "#333333"

# 🌙 Interfaz gráfica estilo móvil
ventana = tk.Tk()
ventana.title("🎬 Downloader")
ventana.geometry("360x740")  # Tamaño tipo pantalla móvil
ventana.configure(bg=fondo)
ventana.resizable(False, False)

tk.Label(ventana, text="Sebastian Urrego",
         font=("Helvetica", 16, "bold"), bg=fondo, fg=acento).pack(pady=15)

frame = tk.Frame(ventana, bg=borde, padx=15, pady=15, bd=0, relief="flat")
frame.pack(pady=10, padx=20, fill="both")

tk.Label(frame, text="🔗 Enlace del video:", font=("Arial", 11, "bold"),
         bg=borde, fg=texto_claro).pack(anchor="w", pady=5)
entrada_enlace = tk.Entry(frame, width=40, font=("Arial", 11),
                          bd=1, relief="sunken", bg="#222", fg=texto_claro,
                          insertbackground=texto_claro)
entrada_enlace.pack(pady=5, ipady=4)

formato_var = tk.StringVar(value="musica")

tk.Label(frame, text="🎧 Formato:", font=("Arial", 11, "bold"),
         bg=borde, fg=texto_claro).pack(anchor="w", pady=5)

frame_botones = tk.Frame(frame, bg=borde)
frame_botones.pack(pady=5)

tk.Radiobutton(frame_botones, text="Música (MP3)", variable=formato_var, value="musica",
               bg=borde, fg=texto_claro, selectcolor=fondo, font=("Arial", 10)).pack(side="left", padx=10)
tk.Radiobutton(frame_botones, text="Video (MP4)", variable=formato_var, value="video",
               bg=borde, fg=texto_claro, selectcolor=fondo, font=("Arial", 10)).pack(side="left", padx=10)

tk.Button(frame, text="⬇ Descargar", command=descargar,
          bg=acento, fg="black", font=("Arial", 11, "bold"),
          padx=10, pady=6, relief="flat").pack(pady=15)

estado = tk.StringVar()
estado_label = tk.Label(ventana, textvariable=estado, font=("Arial", 10, "italic"),
                        bg=fondo, fg=texto_claro)
estado_label.pack(pady=10)

ventana.mainloop()
