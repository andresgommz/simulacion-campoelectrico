# Simulación de Campo Eléctrico y Superficies Equipotenciales

<div align="center">

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-2.0-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.10-11557C?style=for-the-badge)
![Google Colab](https://img.shields.io/badge/Google_Colab-Ready-F9AB00?style=for-the-badge&logo=googlecolab&logoColor=white)

</div>

---

> Simulación interactiva del campo eléctrico y superficies equipotenciales generadas por múltiples cargas puntuales en el plano cartesiano, desarrollada como complemento computacional al laboratorio experimental de Electromagnetismo.

---

## Tabla de Contenidos

- [Descripción](#descripción)
- [Fundamento Teórico](#fundamento-teórico)
- [Características](#características)
- [Tecnologías](#tecnologías)
- [Instalación y Uso](#instalación-y-uso)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Resultados](#resultados)
- [Comparativa: Experimento vs. Simulación](#comparativa-experimento-vs-simulación)
- [Posibles Mejoras](#posibles-mejoras)
- [Referencias](#referencias)

---

## Descripción

**Curso:** Electromagnetismo  
**Tema:** Potencial eléctrico, campo eléctrico y superficies equipotenciales

En los laboratorios de física experimental, una práctica común consiste en medir voltajes en diferentes puntos de un plano conductor para trazar líneas equipotenciales. Esta simulación **reemplaza y complementa** ese proceso físico, permitiendo:

- Calcular el potencial eléctrico exacto en cualquier punto del plano.
- Visualizar superficies equipotenciales con alta resolución (malla 400×400).
- Representar el campo eléctrico vectorialmente mediante streamlines.
- Explorar cualquier configuración de cargas en segundos.

---

## Fundamento Teórico

### Potencial de una carga puntual

$$V = k_e \frac{q}{r}, \qquad k_e = 8.99 \times 10^9 \, \text{N·m}^2/\text{C}^2$$

### Superposición para N cargas

$$V_{\text{total}}(x, y) = \sum_{i=1}^{N} k_e \frac{q_i}{\sqrt{(x - x_i)^2 + (y - y_i)^2 + \varepsilon^2}}$$

> El término $\varepsilon^2 = 10^{-9}$ evita la singularidad numérica en la posición exacta de cada carga.

### Campo eléctrico analítico

$$E_x = k_e \sum_{i} \frac{q_i(x - x_i)}{r_i^3}, \qquad E_y = k_e \sum_{i} \frac{q_i(y - y_i)}{r_i^3}$$

$$\vec{E} = -\nabla V$$

---

## Características

- **Entrada interactiva:** define entre 1 y 8 cargas puntuales (valor en nC y posición).
- **Malla de alta resolución:** evaluación en 400×400 puntos (160,000 puntos).
- **Panel de 3 gráficas:**
  - Mapa de equipotenciales con líneas de contorno etiquetadas.
  - Streamplot del campo eléctrico coloreado por magnitud.
  - Vista combinada equipotenciales + líneas de campo.
- **Perfiles 1D:** corte del potencial a lo largo de los ejes *x* e *y*.
- **Exportación automática** de figuras en PNG (`campo_electrico.png`, `perfil_potencial.png`).
- **Verificación numérica:** comparación entre campo analítico y gradiente numérico.

---

## Tecnologías

| Librería | Versión | Uso |
|---|---|---|
| `numpy` | 2.0.2 | Cálculo vectorizado del potencial y campo |
| `matplotlib` | 3.10.0 | Visualización de equipotenciales y streamplot |
| Python | 3.x | Lenguaje base |
| Google Colab | — | Entorno de ejecución recomendado |

---

## Instalación y Uso

### Opción 1: Ejecución local

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/Vankzzz/simulacion-campoelectrico.git
   cd simulacion-campoelectrico
   ```

2. **Instala las dependencias:**
   ```bash
   pip install numpy matplotlib
   ```

3. **Abre el notebook:**
   ```bash
   jupyter notebook simulacion-campoelectrico.ipynb
   ```

4. **Ejecuta las celdas en orden** y sigue las instrucciones en la celda interactiva (Sección 4.3).

### Opción 2: Google Colab

Sube el archivo `simulacion-campoelectrico.ipynb` directamente a [Google Colab](https://colab.research.google.com/) y ejecuta las celdas en orden.

### Ejemplo de configuración

```
Ingresa el número de cargas: 2

Carga #1:
   Valor q_1 [nC]: 5
   Posición x_1: 1
   Posición y_1: 2

Carga #2:
   Valor q_2 [nC]: -5
   Posición x_2: 3
   Posición y_2: 2

Rango x: [0, 4]   |   Rango y: [0, 3]
```

---

## Estructura del Proyecto

```
simulacion-campoelectrico/
│
├── simulacion-campoelectrico.ipynb   # Notebook principal
├── README.md                         # Este archivo
├── campo_electrico.png               # Figura generada (panel de 3 gráficas)
└── perfil_potencial.png              # Figura generada (perfiles 1D)
```

---

## Resultados

El notebook genera automáticamente dos figuras con fondo oscuro:

### Panel principal — 3 visualizaciones

| Gráfica | Descripción |
|---|---|
| **Equipotenciales** | Mapa de color del potencial con curvas de nivel etiquetadas en voltios |
| **Líneas de campo** | Streamplot con dirección y magnitud del campo $\vec{E}$ |
| **Vista combinada** | Superposición de ambas, verificando la perpendicularidad |

### Interpretación física

- Las equipotenciales **más juntas** indican campo más intenso.
- Las líneas de campo **nacen** en cargas positivas y **terminan** en negativas.
- La perpendicularidad entre equipotenciales y líneas de campo confirma $\vec{E} = -\nabla V$.

---

## Comparativa: Experimento vs. Simulación

| Aspecto | Experimento real | Esta simulación |
|---|---|---|
| Medición del potencial | Voltímetro en puntos discretos | Malla continua 400×400 |
| Trazado de equipotenciales | A mano, con errores | Contour automático y preciso |
| Cambio de configuración | Rediseñar el montaje | Modificar parámetros en segundos |
| Visualización del campo | Indirecto | Streamplot vectorial directo |
| Error de medición | Errores experimentales reales | $\varepsilon^2 = 10^{-9}$ controlado |

---

## Posibles Mejoras

- [ ] Extensión a **3 dimensiones** con superficies isopotenciales.
- [ ] **Animaciones** de la trayectoria de una carga de prueba.
- [ ] **Distribuciones continuas** (líneas y superficies cargadas).
- [ ] **Interfaz interactiva** con `ipywidgets` (sliders en tiempo real).
- [ ] Importar **datos experimentales** reales para comparación directa.

---

## Referencias

- Griffiths, D. J. *Introduction to Electrodynamics*, 4th ed. Pearson, 2017.
- Serway, R. A. & Jewett, J. W. *Physics for Scientists and Engineers*, 9th ed. Cengage, 2014.
- [NumPy Documentation](https://numpy.org/doc/)
- [Matplotlib Documentation](https://matplotlib.org/)

---

<div align="center">

Desarrollado para el curso de **Electromagnetismo** · Universidad Andrés Bello

</div>
