"""Extrae contornos de dibujos (imágenes/PDF) y los expresa como serie de Fourier.

Este script sigue el enfoque que compartiste: convertir el contorno en una señal compleja
(x + i*y), aplicar FFT y guardar los coeficientes.

Se puede usar para entrenar modelos que "entiendan" formas (p.ej. para clasificar contornos
como "caja" vs "tornillo" o para reconstruir contornos en otro sistema como AutoCAD).

Requisitos:
  pip install numpy opencv-python matplotlib
  pip install PyMuPDF  # sólo si se desea leer PDF directamente

Uso:
  python ml/contour_fourier.py --input manual.pdf --output out.json
  python ml/contour_fourier.py --input imagen.png --output out.json

El script genera:
  - archivo JSON con coeficientes de Fourier (ordenados por frecuencia)
  - opcionalmente, un PNG de la reconstrucción usando N términos

"""

import argparse
import json
import os

import numpy as np

try:
    import cv2
except ImportError as e:
    raise ImportError("Instale opencv-python: pip install opencv-python") from e


def read_image_from_pdf(path, dpi=200):
    """Extrae la primera página del PDF como imagen en escala de grises."""
    try:
        import fitz  # PyMuPDF
    except ImportError as e:
        raise ImportError("Instale PyMuPDF: pip install PyMuPDF") from e

    doc = fitz.open(path)
    if len(doc) == 0:
        raise ValueError("El PDF no contiene páginas")

    page = doc[0]
    mat = fitz.Matrix(dpi / 72.0, dpi / 72.0)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    arr = np.frombuffer(pix.samples, dtype=np.uint8)
    arr = arr.reshape(pix.height, pix.width, pix.n)
    if arr.ndim == 3:
        arr = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
    return arr


def extract_contour(img, resize_to=None, threshold=127):
    """Extrae el contorno más grande de la imagen en escala de grises."""
    if resize_to is not None:
        img = cv2.resize(img, resize_to, interpolation=cv2.INTER_AREA)

    _, binary = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    if not contours:
        raise ValueError("No se encontraron contornos en la imagen")

    cont = max(contours, key=cv2.contourArea)
    return cont[:, 0, :]


def contour_to_complex(coords, invert_y=True):
    """Convierte coordenadas Nx2 a vector complejo (x + i*y)."""
    x = coords[:, 0].astype(np.float64)
    y = coords[:, 1].astype(np.float64)
    if invert_y:
        y = -y
    return x + 1j * y


def compute_fourier(signal):
    N = len(signal)
    if N == 0:
        raise ValueError("No se puede calcular FFT de una señal vacía; verifique la extracción de contornos")
    return np.fft.fft(signal) / N


def save_fourier_json(path, freqs, coeffs):
    serial = [
        [float(freq), [float(c.real), float(c.imag)]]
        for freq, c in zip(freqs, coeffs)
    ]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(serial, f, indent=2)


def reconstruct_signal(freqs, coeffs, t_vals):
    return np.array([
        sum(c * np.exp(2j * np.pi * f * t) for f, c in zip(freqs, coeffs))
        for t in t_vals
    ])


def save_plot(original, reconstructed, out_path):
    import matplotlib.pyplot as plt

    plt.figure(figsize=(6, 6))
    plt.plot(original.real, original.imag, "b-", label="Original")
    plt.plot(reconstructed.real, reconstructed.imag, "r--", label="Reconstruida")
    plt.gca().set_aspect("equal")
    plt.axis("off")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()


def main():
    parser = argparse.ArgumentParser(description="Extrae contorno de dibujo y calcula serie de Fourier.")
    parser.add_argument("--input", required=True, help="Ruta a imagen (png/jpg) o PDF.")
    parser.add_argument("--output", required=True, help="JSON de salida con coeficientes de Fourier.")
    parser.add_argument("--resize", default="300x300", help="Tamaño de salida (anchoxalto) para normalizar.")
    parser.add_argument("--terms", type=int, default=100, help="Cantidad de términos a usar en la reconstrucción de prueba.")
    parser.add_argument("--plot", help="Guarda imagen comparativa del contorno y la reconstrucción.")
    args = parser.parse_args()

    inp = args.input
    if inp.lower().endswith(".pdf"):
        img = read_image_from_pdf(inp)
    else:
        # Use Python file read + imdecode to handle Unicode paths on Windows
        if not os.path.exists(inp):
            raise FileNotFoundError(f"No se pudo cargar la imagen: {inp}")
        with open(inp, "rb") as f:
            data = f.read()
        nparr = np.frombuffer(data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise FileNotFoundError(f"No se pudo cargar la imagen: {inp}")

    w, h = (int(x) for x in args.resize.split("x"))
    cont = extract_contour(img, resize_to=(w, h))
    signal = contour_to_complex(cont)

    if len(signal) == 0:
        raise ValueError("El contorno extraído está vacío. Verifique que la imagen PDF o PNG contiene un contorno detectable.")

    signal = signal - np.mean(signal)
    N = len(signal)
    fourier = compute_fourier(signal)
    freqs = np.fft.fftfreq(N)

    save_fourier_json(args.output, freqs, fourier)

    if args.plot:
        t_vals = np.linspace(0, 1, N, endpoint=False)
        recon = reconstruct_signal(freqs[:args.terms], fourier[:args.terms], t_vals)
        save_plot(signal, recon, args.plot)

    print(f"Guardado Fourier en: {args.output}")


if __name__ == "__main__":
    main()
