"""
Módulo para procesar datos de ventas y generar reportes con IVA.
Incluye análisis estadístico de ventas.
"""
import csv
import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constantes configurables
IVA_DEFAULT = 0.19


@dataclass
class ConfigReporte:
    """Configuración para el procesamiento de reportes."""
    archivo_entrada: Path
    archivo_salida: Path
    tasa_iva: float = IVA_DEFAULT
    tiene_header: bool = True


@dataclass
class EstadisticasVentas:
    """Estadísticas calculadas del reporte de ventas."""
    total_registros: int = 0
    monto_total_sin_iva: float = 0.0
    monto_total_con_iva: float = 0.0
    monto_promedio: float = 0.0
    monto_minimo: float = 0.0
    monto_maximo: float = 0.0
    total_iva_recaudado: float = 0.0
    fecha_generacion: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict:
        """Convierte las estadísticas a diccionario."""
        return {
            "total_registros": self.total_registros,
            "monto_total_sin_iva": self.monto_total_sin_iva,
            "monto_total_con_iva": self.monto_total_con_iva,
            "monto_promedio": self.monto_promedio,
            "monto_minimo": self.monto_minimo,
            "monto_maximo": self.monto_maximo,
            "total_iva_recaudado": self.total_iva_recaudado,
            "fecha_generacion": self.fecha_generacion
        }


# =============================================================================
# MÓDULO DE LECTURA/ESCRITURA
# =============================================================================

def leer_csv(ruta: Path, tiene_header: bool = True) -> list[list[str]]:
    """Lee un archivo CSV y retorna sus filas."""
    with open(ruta, 'r', encoding='utf-8') as f:
        lector = csv.reader(f)
        if tiene_header:
            next(lector, None)
        return list(lector)


def guardar_json(datos: dict, ruta: Path) -> None:
    """Guarda los datos en formato JSON."""
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)


# =============================================================================
# MÓDULO DE CÁLCULOS
# =============================================================================

def calcular_monto_con_iva(monto: float, tasa_iva: float) -> float:
    """Aplica IVA al monto dado."""
    return round(monto * (1 + tasa_iva), 2)


def procesar_fila(fila: list[str], tasa_iva: float) -> dict | None:
    """Procesa una fila del CSV y retorna el objeto formateado."""
    if len(fila) < 2:
        logger.warning(f"Fila incompleta ignorada: {fila}")
        return None
    
    try:
        monto_original = float(fila[1])
        return {
            "id": fila[0],
            "monto_original": monto_original,
            "monto_con_iva": calcular_monto_con_iva(monto_original, tasa_iva)
        }
    except ValueError as e:
        logger.error(f"Error al procesar fila {fila}: {e}")
        return None


# =============================================================================
# MÓDULO DE ANÁLISIS ESTADÍSTICO (NUEVO)
# =============================================================================

def calcular_estadisticas(registros: list[dict], tasa_iva: float) -> EstadisticasVentas:
    """
    Calcula estadísticas agregadas de los registros de ventas.
    
    Args:
        registros: Lista de diccionarios con los datos procesados
        tasa_iva: Tasa de IVA aplicada
    
    Returns:
        EstadisticasVentas con todos los cálculos
    """
    if not registros:
        logger.warning("No hay registros para calcular estadísticas")
        return EstadisticasVentas()
    
    montos_originales = [r["monto_original"] for r in registros]
    montos_con_iva = [r["monto_con_iva"] for r in registros]
    
    total_sin_iva = sum(montos_originales)
    total_con_iva = sum(montos_con_iva)
    
    return EstadisticasVentas(
        total_registros=len(registros),
        monto_total_sin_iva=round(total_sin_iva, 2),
        monto_total_con_iva=round(total_con_iva, 2),
        monto_promedio=round(total_sin_iva / len(registros), 2),
        monto_minimo=min(montos_originales),
        monto_maximo=max(montos_originales),
        total_iva_recaudado=round(total_con_iva - total_sin_iva, 2)
    )


def generar_resumen_texto(stats: EstadisticasVentas) -> str:
    """Genera un resumen legible de las estadísticas."""
    return f"""
╔══════════════════════════════════════════════════╗
║           RESUMEN DE VENTAS                      ║
╠══════════════════════════════════════════════════╣
║  Registros procesados:  {stats.total_registros:>10}              ║
║  Monto total (sin IVA): ${stats.monto_total_sin_iva:>12,.2f}         ║
║  Monto total (con IVA): ${stats.monto_total_con_iva:>12,.2f}         ║
║  IVA total recaudado:   ${stats.total_iva_recaudado:>12,.2f}         ║
║  Promedio por venta:    ${stats.monto_promedio:>12,.2f}         ║
║  Venta mínima:          ${stats.monto_minimo:>12,.2f}         ║
║  Venta máxima:          ${stats.monto_maximo:>12,.2f}         ║
╠══════════════════════════════════════════════════╣
║  Generado: {stats.fecha_generacion[:19]:<26}       ║
╚══════════════════════════════════════════════════╝
"""


# =============================================================================
# MÓDULO DE GENERACIÓN DE REPORTES
# =============================================================================

def generar_reporte(config: ConfigReporte) -> list[dict]:
    """Genera el reporte completo desde el CSV."""
    datos = leer_csv(config.archivo_entrada, config.tiene_header)
    
    resultados = []
    for fila in datos:
        obj = procesar_fila(fila, config.tasa_iva)
        if obj:
            resultados.append(obj)
    
    return resultados


def generar_reporte_completo(config: ConfigReporte) -> dict:
    """
    Genera reporte completo con datos y estadísticas.
    
    Returns:
        Diccionario con registros y estadísticas
    """
    registros = generar_reporte(config)
    estadisticas = calcular_estadisticas(registros, config.tasa_iva)
    
    return {
        "metadata": {
            "archivo_origen": str(config.archivo_entrada),
            "tasa_iva_aplicada": config.tasa_iva,
            "fecha_generacion": estadisticas.fecha_generacion
        },
        "estadisticas": estadisticas.to_dict(),
        "registros": registros
    }


# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================

def main() -> None:
    """Punto de entrada principal."""
    config = ConfigReporte(
        archivo_entrada=Path("datos.csv"),
        archivo_salida=Path("reporte.json"),
        tasa_iva=IVA_DEFAULT,
        tiene_header=True
    )
    
    try:
        reporte = generar_reporte_completo(config)
        guardar_json(reporte, config.archivo_salida)
        
        # Mostrar resumen en consola
        stats = EstadisticasVentas(**reporte["estadisticas"])
        print(generar_resumen_texto(stats))
        
        logger.info(f"Reporte guardado en: {config.archivo_salida}")
        
    except FileNotFoundError:
        logger.error(f"Archivo no encontrado: {config.archivo_entrada}")
    except PermissionError:
        logger.error("Sin permisos para leer/escribir archivos")


if __name__ == "__main__":
    main()