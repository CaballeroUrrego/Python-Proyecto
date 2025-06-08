import os
import subprocess
import tkinter as tk
from tkinter import messagebox

# Función para detectar de qué plataforma es el enlace (TikTok, Facebook, Instagram, YouTube)
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

# Función principal que se ejecuta al hacer clic en el botón "Descargar"
def descargar():
    # Obtener el enlace ingresado por el usuario
    link = entrada_enlace.get().strip()
    # Obtener el formato seleccionado (audio MP3 o video MP4)
    formato = formato_var.get()

    # Validar que el enlace comience con http/https
    if not link.startswith("http"):
        messagebox.showerror("Error", "❌ Enlace inválido.")
        return

    # Identificar la plataforma del enlace
    plataforma = detectar_plataforma(link)
    if plataforma == "desconocido":
        messagebox.showerror("Error", "❌ Plataforma no soportada.")
        return

    # Crear la carpeta 'descargas' si no existe
    carpeta_salida = "descargas"
    os.makedirs(carpeta_salida, exist_ok=True)

    # Opciones comunes para todas las descargas:
    # --no-playlist: Descarga solo el video, no listas de reproducción
    # -o: Ruta de salida con nombre del archivo
    opciones_comunes = [
        "--no-playlist",
        "-o", os.path.join(carpeta_salida, "%(title)s.%(ext)s")
    ]

    # Comando base usando yt-dlp
    comando = ["yt-dlp"]

    # Configurar parámetros según plataforma y formato seleccionado
    if plataforma == "tiktok":
        if formato == "musica":
            # Extraer solo audio en formato MP3
            comando += ["-x", "--audio-format", "mp3"]
        else:
            # Descargar el video en la mejor calidad disponible
            comando += ["-f", "best"]
    elif plataforma in ["facebook", "instagram", "youtube"]:
        if formato == "musica":
            # Extraer solo audio en formato MP3
            comando += ["-x", "--audio-format", "mp3"]
        else:
            # Combinar el mejor video con el mejor audio disponible
            comando += ["-f", "bestvideo+bestaudio/best"]
    else:
        messagebox.showerror("Error", "❌ Plataforma no soportada.")
        return

    # Añadir las opciones comunes y el enlace al comando final
    comando += opciones_comunes + [link]

    try:
        # Actualizar el estado de la descarga
        estado.set("⏳ Descargando...")
        ventana.update()
        
        # Ejecutar el comando de descarga
        subprocess.run(comando, check=True)
        
        # Actualizar estado a completado
        estado.set("✅ Descarga completada.")
        estado_label.config(fg="#00ff88")  # Color verde
    except subprocess.CalledProcessError as e:
        # Mostrar mensaje de error si falla la descarga
        estado.set("❌ Error en la descarga.")
        estado_label.config(fg="#ff4444")  # Color rojo
        messagebox.showerror("Error", str(e))

# Configuración de colores para la interfaz (modo oscuro)
fondo = "#121212"          # Color de fondo principal
texto_claro = "#e0e0e0"    # Color de texto claro
acento = "#00ff88"         # Color de acento (verde neón)
boton_color = "#1f1f1f"    # Color de botones
borde = "#333333"          # Color de bordes

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("🎬 Downloader")
ventana.geometry("360x740")  # Tamaño similar a un smartphone
ventana.configure(bg=fondo)
ventana.resizable(False, False)  # Ventana no redimensionable

# Título de la aplicación
tk.Label(ventana, text="Sebastian Urrego",
         font=("Helvetica", 16, "bold"), bg=fondo, fg=acento).pack(pady=15)

# Marco principal que contiene los controles
frame = tk.Frame(ventana, bg=borde, padx=15, pady=15, bd=0, relief="flat")
frame.pack(pady=10, padx=20, fill="both")

# Etiqueta y campo de entrada para el enlace
tk.Label(frame, text="🔗 Enlace del video:", font=("Arial", 11, "bold"),
         bg=borde, fg=texto_claro).pack(anchor="w", pady=5)
entrada_enlace = tk.Entry(frame, width=40, font=("Arial", 11),
                          bd=1, relief="sunken", bg="#222", fg=texto_claro,
                          insertbackground=texto_claro)
entrada_enlace.pack(pady=5, ipady=4)

# Variable para almacenar la selección de formato
formato_var = tk.StringVar(value="musica")

# Sección de selección de formato (MP3 o MP4)
tk.Label(frame, text="🎧 Formato:", font=("Arial", 11, "bold"),
         bg=borde, fg=texto_claro).pack(anchor="w", pady=5)

# Frame para contener los botones de opción
frame_botones = tk.Frame(frame, bg=borde)
frame_botones.pack(pady=5)

# Botones de opción para formato
tk.Radiobutton(frame_botones, text="Música (MP3)", variable=formato_var, value="musica",
               bg=borde, fg=texto_claro, selectcolor=fondo, font=("Arial", 10)).pack(side="left", padx=10)
tk.Radiobutton(frame_botones, text="Video (MP4)", variable=formato_var, value="video",
               bg=borde, fg=texto_claro, selectcolor=fondo, font=("Arial", 10)).pack(side="left", padx=10)

# Botón principal de descarga
tk.Button(frame, text="⬇ Descargar", command=descargar,
          bg=acento, fg="black", font=("Arial", 11, "bold"),
          padx=10, pady=6, relief="flat").pack(pady=15)

# Etiqueta para mostrar el estado de la descarga
estado = tk.StringVar()
estado_label = tk.Label(ventana, textvariable=estado, font=("Arial", 10, "italic"),
                        bg=fondo, fg=texto_claro)
estado_label.pack(pady=10)

# Iniciar el bucle principal de la aplicación
ventana.mainloop()