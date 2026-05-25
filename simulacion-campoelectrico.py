import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Circle
import warnings
warnings.filterwarnings('ignore')

# Configuración global de gráficas
plt.rcParams['figure.dpi'] = 120
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12

print('✅ Librerías importadas correctamente.')
print(f'   NumPy  versión: {np.__version__}')
print(f'   Matplotlib versión: {plt.matplotlib.__version__}')

# Constante de Coulomb [N·m²/C²]
K_E = 8.99e9

# Término de regularización para evitar singularidades
EPSILON_SQ = 1e-9

# Número de puntos de la malla (resolución)
N_PUNTOS = 400

print('✅ Constantes definidas:')
print(f'   k_e = {K_E:.2e} N·m²/C²')
print(f'   ε²  = {EPSILON_SQ:.0e}  (regularización)')
print(f'   Resolución de malla: {N_PUNTOS} × {N_PUNTOS} puntos')

def ingresar_cargas():
    """
    Función interactiva para ingresar la configuración de cargas.
    Retorna:
        cargas : lista de dicts {'q': valor_en_C, 'q_nC': valor_en_nC, 'x': pos_x, 'y': pos_y}
        x_range: (x_min, x_max)
        y_range: (y_min, y_max)
    """
    print('=' * 55)
    print('  SIMULACIÓN DE CAMPO ELÉCTRICO Y EQUIPOTENCIALES')
    print('=' * 55)

    # --- Número de cargas ---
    while True:
        try:
            n = int(input('\n▶ Ingresa el número de cargas (1 a 8): '))
            if 1 <= n <= 8:
                break
            print('  ⚠️  Por favor ingresa un número entre 1 y 8.')
        except ValueError:
            print('  ⚠️  Entrada inválida. Usa un número entero.')

    cargas = []
    print(f'\n{"─"*55}')
    print('  Ingresa los datos de cada carga')
    print('  (Usa valores positivos o negativos en nanocoulombs)')
    print(f'{"─"*55}')

    for i in range(n):
        print(f'\n  🔵 Carga #{i+1}:')
        while True:
            try:
                q_nC = float(input(f'     Valor q_{i+1} [nC] (ej: 1.0, -2.5): '))
                break
            except ValueError:
                print('     ⚠️  Ingresa un número decimal.')
        while True:
            try:
                x_pos = float(input(f'     Posición x_{i+1}: '))
                break
            except ValueError:
                print('     ⚠️  Ingresa un número decimal.')
        while True:
            try:
                y_pos = float(input(f'     Posición y_{i+1}: '))
                break
            except ValueError:
                print('     ⚠️  Ingresa un número decimal.')

        cargas.append({
            'q':    q_nC * 1e-9,  # Convertir nC → C
            'q_nC': q_nC,         # Guardar en nC para etiquetas
            'x':    x_pos,
            'y':    y_pos
        })

    # --- Rango del plano ---
    print(f'\n{"─"*55}')
    print('  Define el rango del plano cartesiano:')
    print(f'{"─"*55}')
    while True:
        try:
            x_min = float(input('  x_mín (ej: -10): '))
            x_max = float(input('  x_máx (ej:  10): '))
            y_min = float(input('  y_mín (ej: -10): '))
            y_max = float(input('  y_máx (ej:  10): '))
            if x_max > x_min and y_max > y_min:
                break
            print('  ⚠️  El máximo debe ser mayor que el mínimo.')
        except ValueError:
            print('  ⚠️  Ingresa valores numéricos.')

    # --- Resumen ---
    print(f'\n{"="*55}')
    print('  ✅ CONFIGURACIÓN REGISTRADA')
    print(f'{"="*55}')
    print(f'  Cargas definidas: {n}')
    for c in cargas:
        signo = '+' if c['q_nC'] >= 0 else ''
        print(f'    q = {signo}{c["q_nC"]:.2f} nC  en  ({c["x"]:.2f}, {c["y"]:.2f})')
    print(f'  Rango x: [{x_min}, {x_max}]')
    print(f'  Rango y: [{y_min}, {y_max}]')
    print(f'{"="*55}\n')

    return cargas, (x_min, x_max), (y_min, y_max)


# --- Ejecutar entrada de datos ---
cargas, x_range, y_range = ingresar_cargas()

def crear_malla(x_range, y_range, n_puntos=N_PUNTOS):
    """
    Crea la malla cartesiana de evaluación usando np.meshgrid.
    Args:
        x_range  : tupla (x_min, x_max)
        y_range  : tupla (y_min, y_max)
        n_puntos : resolución n × n
    Returns:
        X, Y     : matrices meshgrid
        x_arr, y_arr : vectores de coordenadas
    """
    x_arr = np.linspace(x_range[0], x_range[1], n_puntos)
    y_arr = np.linspace(y_range[0], y_range[1], n_puntos)
    X, Y  = np.meshgrid(x_arr, y_arr)
    return X, Y, x_arr, y_arr


X, Y, x_arr, y_arr = crear_malla(x_range, y_range)

print(f'✅ Malla creada: {X.shape[0]} × {X.shape[1]} puntos')
print(f'   Total de puntos evaluados: {X.size:,}')
print(f'   Resolución Δx ≈ {(x_range[1]-x_range[0])/N_PUNTOS:.4f} unidades')
print(f'   Resolución Δy ≈ {(y_range[1]-y_range[0])/N_PUNTOS:.4f} unidades')

def calcular_potencial(X, Y, cargas, k_e=K_E, eps_sq=EPSILON_SQ):
    """
    Calcula el potencial eléctrico total V(x,y) usando superposición.
    La operación es completamente vectorizada: sin bucles sobre puntos.
    """
    V = np.zeros_like(X, dtype=float)
    for carga in cargas:
        dx = X - carga['x']
        dy = Y - carga['y']
        r  = np.sqrt(dx**2 + dy**2 + eps_sq)  # distancia regularizada
        V += k_e * carga['q'] / r
    return V


V = calcular_potencial(X, Y, cargas)

print('✅ Potencial calculado exitosamente.')
print(f'   V_máx (percentil 98) ≈ {np.percentile(V, 98):.3e} V')
print(f'   V_mín (percentil  2) ≈ {np.percentile(V,  2):.3e} V')
print(f'   V en el origen (0,0) ≈ {calcular_potencial(np.array([[0.]]), np.array([[0.]]), cargas)[0,0]:.3e} V')

def calcular_campo_electrico(X, Y, cargas, k_e=K_E, eps_sq=EPSILON_SQ):
    """
    Calcula las componentes Ex, Ey del campo eléctrico analíticamente.
    Más preciso que el gradiente numérico, especialmente cerca de las cargas.
    """
    Ex = np.zeros_like(X, dtype=float)
    Ey = np.zeros_like(Y, dtype=float)
    for carga in cargas:
        dx      = X - carga['x']
        dy      = Y - carga['y']
        r_sq    = dx**2 + dy**2 + eps_sq
        r_cubed = r_sq ** 1.5
        factor  = k_e * carga['q'] / r_cubed
        Ex += factor * dx
        Ey += factor * dy
    return Ex, Ey


Ex, Ey = calcular_campo_electrico(X, Y, cargas)
E_mag  = np.sqrt(Ex**2 + Ey**2)

print('✅ Campo eléctrico calculado.')
print(f'   |E|_máx (percentil 98) ≈ {np.percentile(E_mag, 98):.3e} V/m')
print(f'   |E|_mín (percentil  5) ≈ {np.percentile(E_mag,  5):.3e} V/m')

# Verificación numérica
dy_step = (y_range[1] - y_range[0]) / N_PUNTOS
dx_step = (x_range[1] - x_range[0]) / N_PUNTOS
dV_dy, dV_dx = np.gradient(V, dy_step, dx_step)
Ex_num, Ey_num = -dV_dx, -dV_dy
error_rel = np.mean(np.abs(Ex - Ex_num)) / (np.mean(np.abs(Ex)) + 1e-30) * 100
print(f'\n   Verificación: error relativo E_x numérico vs analítico: {error_rel:.2f}%')

def visualizar_campo_completo(X, Y, V, Ex, Ey, cargas, x_range, y_range):
    """Genera el panel completo de tres visualizaciones."""

    # --- Preparación ---
    v_max   = np.percentile(np.abs(V), 97)
    V_vis   = np.clip(V, -v_max, v_max)
    E_mag   = np.sqrt(Ex**2 + Ey**2)
    E_log   = np.log1p(np.clip(E_mag, 0, np.percentile(E_mag, 99)))
    Ex_norm = Ex / (E_mag + 1e-30)          # dirección normalizada
    Ey_norm = Ey / (E_mag + 1e-30)
    niveles = np.linspace(-v_max * 0.95, v_max * 0.95, 30)
    colores = {True: '#FF4C4C', False: '#4CA8FF'}  # rojo=+, azul=-

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.patch.set_facecolor('#0D1117')
    for ax in axes:
        ax.set_facecolor('#0D1117')

    def estilizar_ax(ax, titulo):
        ax.set_xlim(x_range); ax.set_ylim(y_range)
        ax.set_xlabel('x', color='white', fontsize=11)
        ax.set_ylabel('y', color='white', fontsize=11)
        ax.set_title(titulo, color='white', fontsize=13, pad=10)
        ax.tick_params(colors='white')
        for s in ['bottom','left']:   ax.spines[s].set_color('white')
        for s in ['top','right']:     ax.spines[s].set_color('#0D1117')
        ax.grid(True, alpha=0.15, color='gray', linestyle='--', linewidth=0.5)

    def dibujar_cargas(ax):
        for c in cargas:
            es_pos = c['q'] >= 0
            color  = colores[es_pos]
            sym    = f"+{c['q_nC']:.1f}" if es_pos else f"{c['q_nC']:.1f}"
            ax.add_patch(Circle((c['x'], c['y']), 0.18, color=color, zorder=5))
            ax.text(c['x'], c['y'] + 0.35, f'{sym} nC',
                    ha='center', va='bottom', fontsize=8,
                    color=color, fontweight='bold', zorder=6)

    # ── Gráfica 1: Equipotenciales ──────────────────────────────
    ax1 = axes[0]
    cp  = ax1.contourf(X, Y, V_vis, levels=60, cmap='RdBu_r', alpha=0.85)
    cs  = ax1.contour(X, Y, V_vis, levels=niveles,
                      colors='white', linewidths=0.7, alpha=0.8)
    ax1.clabel(cs, inline=True, fontsize=6.5, fmt='%.1e', colors='white')
    cb1 = plt.colorbar(cp, ax=ax1, shrink=0.85, pad=0.02)
    cb1.set_label('Potencial V [V]', color='white', fontsize=10)
    cb1.ax.yaxis.set_tick_params(color='white', labelcolor='white')
    dibujar_cargas(ax1)
    estilizar_ax(ax1, 'Superficies Equipotenciales\n$V(x,y) = $ cte')

    # ── Gráfica 2: Campo eléctrico ──────────────────────────────
    ax2 = axes[1]
    ax2.contourf(X, Y, E_log, levels=40, cmap='inferno', alpha=0.7)
    strm = ax2.streamplot(X, Y, Ex_norm, Ey_norm,
                          color=E_log, cmap='cool',
                          linewidth=1.2, density=1.6,
                          arrowsize=1.2, arrowstyle='->')
    cb2 = plt.colorbar(strm.lines, ax=ax2, shrink=0.85, pad=0.02)
    cb2.set_label('log(1+|E|) [rel.]', color='white', fontsize=10)
    cb2.ax.yaxis.set_tick_params(color='white', labelcolor='white')
    dibujar_cargas(ax2)
    estilizar_ax(ax2, 'Líneas de Campo Eléctrico\n$\\vec{E} = -\\nabla V$')

    # ── Gráfica 3: Vista combinada ──────────────────────────────
    ax3 = axes[2]
    cp3 = ax3.contourf(X, Y, V_vis, levels=60, cmap='seismic', alpha=0.6)
    ax3.contour(X, Y, V_vis, levels=16,
                colors='yellow', linewidths=0.9, alpha=0.9)
    ax3.streamplot(X, Y, Ex_norm, Ey_norm,
                   color='white', linewidth=1.0,
                   density=1.2, arrowsize=1.1, arrowstyle='->')
    cb3 = plt.colorbar(cp3, ax=ax3, shrink=0.85, pad=0.02)
    cb3.set_label('Potencial V [V]', color='white', fontsize=10)
    cb3.ax.yaxis.set_tick_params(color='white', labelcolor='white')
    dibujar_cargas(ax3)
    estilizar_ax(ax3, 'Vista Combinada\nEquipotenciales + Campo $\\vec{E}$')

    # ── Leyenda global ──────────────────────────────────────────
    from matplotlib.patches import Patch
    leyenda = [
        Patch(facecolor='#FF4C4C', edgecolor='white', label='Carga positiva (+)'),
        Patch(facecolor='#4CA8FF', edgecolor='white', label='Carga negativa (−)'),
        plt.Line2D([0],[0], color='yellow', lw=1.5, label='Equipotenciales'),
        plt.Line2D([0],[0], color='white',  lw=1.2, label='Líneas de campo $\\vec{E}$'),
    ]
    fig.legend(handles=leyenda, loc='lower center', ncol=4,
               facecolor='#1C2128', edgecolor='gray',
               labelcolor='white', fontsize=9.5, framealpha=0.9,
               bbox_to_anchor=(0.5, -0.04))

    plt.suptitle('Campo Eléctrico y Superficies Equipotenciales — Cargas Puntuales —',
                 color='white', fontsize=15, fontweight='bold', y=1.02)
    plt.tight_layout(rect=[0, 0.04, 1, 1])
    plt.savefig('campo_electrico.png', dpi=150,
                bbox_inches='tight', facecolor='#0D1117')
    plt.show()
    print("\n✅ Figura guardada como 'campo_electrico.png'")


visualizar_campo_completo(X, Y, V, Ex, Ey, cargas, x_range, y_range)

def graficar_perfil_potencial(V, x_range, y_range, cargas):
    """Perfil de V a lo largo de los ejes coordenados."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.patch.set_facecolor('#0D1117')
    colores = {True: '#FF4C4C', False: '#4CA8FF'}

    x_arr = np.linspace(x_range[0], x_range[1], N_PUNTOS)
    y_arr = np.linspace(y_range[0], y_range[1], N_PUNTOS)

    def estilo(ax, xlabel, ylabel, titulo):
        ax.set_facecolor('#0D1117')
        ax.set_xlabel(xlabel, color='white')
        ax.set_ylabel(ylabel, color='white')
        ax.set_title(titulo, color='white', fontsize=12)
        ax.tick_params(colors='white')
        ax.legend(facecolor='#1C2128', labelcolor='white', fontsize=9)
        for s in ['bottom','left']: ax.spines[s].set_color('white')
        for s in ['top','right']:   ax.spines[s].set_color('#0D1117')
        ax.grid(True, alpha=0.2, color='gray', linestyle='--')

    # Perfil y=0
    idx_y0 = N_PUNTOS // 2
    Vh     = np.clip(V[idx_y0, :], np.percentile(V,3), np.percentile(V,97))
    ax1    = axes[0]
    ax1.plot(x_arr, Vh, color='#00D4FF', lw=2, label='$V(x, 0)$')
    ax1.axhline(0, color='gray', lw=0.8, linestyle='--', alpha=0.6)
    ax1.fill_between(x_arr, Vh, 0, where=(Vh>0), alpha=0.25, color='#FF4C4C', label='V > 0')
    ax1.fill_between(x_arr, Vh, 0, where=(Vh<0), alpha=0.25, color='#4CA8FF', label='V < 0')
    for c in cargas:
        ax1.axvline(c['x'], color=colores[c['q']>=0], lw=1.2, ls=':', alpha=0.8)
    estilo(ax1, 'x', 'V [V]', 'Perfil de Potencial en $y = 0$')

    # Perfil x=0
    idx_x0 = N_PUNTOS // 2
    Vv     = np.clip(V[:, idx_x0], np.percentile(V,3), np.percentile(V,97))
    ax2    = axes[1]
    ax2.plot(Vv, y_arr, color='#FFD700', lw=2, label='$V(0, y)$')
    ax2.axvline(0, color='gray', lw=0.8, linestyle='--', alpha=0.6)
    ax2.fill_betweenx(y_arr, Vv, 0, where=(Vv>0), alpha=0.25, color='#FF4C4C', label='V > 0')
    ax2.fill_betweenx(y_arr, Vv, 0, where=(Vv<0), alpha=0.25, color='#4CA8FF', label='V < 0')
    for c in cargas:
        ax2.axhline(c['y'], color=colores[c['q']>=0], lw=1.2, ls=':', alpha=0.8)
    estilo(ax2, 'V [V]', 'y', 'Perfil de Potencial en $x = 0$')

    plt.suptitle('Perfiles Unidimensionales del Potencial Eléctrico',
                 color='white', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('perfil_potencial.png', dpi=150,
                bbox_inches='tight', facecolor='#0D1117')
    plt.show()
    print("\n✅ Figura guardada como 'perfil_potencial.png'")


graficar_perfil_potencial(V, x_range, y_range, cargas)

