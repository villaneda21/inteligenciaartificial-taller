"""
Módulo para procesar datos de ventas y generar reportes con IVA.
"""
import csv
import json
import logging
from dataclasses import dataclass
from pathlib import Path

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


def leer_csv(ruta: Path, tiene_header: bool = True) -> list[list[str]]:
    """Lee un archivo CSV y retorna sus filas."""
    with open(ruta, 'r', encoding='utf-8') as f:
        lector = csv.reader(f)
        if tiene_header:
            next(lector, None)
        return list(lector)


def calcular_monto_con_iva(monto: float, tasa_iva: float) -> float:
    """Aplica IVA al monto dado."""
    return round(monto * (1 + tasa_iva), 2)


def procesar_fila(fila: list[str], tasa_iva: float) -> dict | None:
    """Procesa una fila del CSV y retorna el objeto formateado."""
    if len(fila) < 2:
        logger.warning(f"Fila incompleta ignorada: {fila}")
        return None
    
    try:
        return {
            "id": fila[0],
            "monto_original": float(fila[1]),
            "monto_con_iva": calcular_monto_con_iva(float(fila[1]), tasa_iva)
        }
    except ValueError as e:
        logger.error(f"Error al procesar fila {fila}: {e}")
        return None


def generar_reporte(config: ConfigReporte) -> list[dict]:
    """Genera el reporte completo desde el CSV."""
    datos = leer_csv(config.archivo_entrada, config.tiene_header)
    
    resultados = []
    for fila in datos:
        obj = procesar_fila(fila, config.tasa_iva)
        if obj:
            resultados.append(obj)
    
    return resultados


def guardar_json(datos: list[dict], ruta: Path) -> None:
    """Guarda los datos en formato JSON."""
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)


def main() -> None:
    """Punto de entrada principal."""
    config = ConfigReporte(
        archivo_entrada=Path("datos.csv"),
        archivo_salida=Path("reporte.json"),
        tasa_iva=IVA_DEFAULT,
        tiene_header=True
    )
    
    try:
        reporte = generar_reporte(config)
        guardar_json(reporte, config.archivo_salida)
        logger.info(f"Reporte generado: {len(reporte)} registros procesados")
    except FileNotFoundError:
        logger.error(f"Archivo no encontrado: {config.archivo_entrada}")
    except PermissionError:
        logger.error("Sin permisos para leer/escribir archivos")


if __name__ == "__main__":
    main()