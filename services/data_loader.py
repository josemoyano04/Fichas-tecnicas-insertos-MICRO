import pandas as pd
import math
import os
from dataclasses import dataclass
from typing import Tuple, Optional, Dict


@dataclass
class Inserto:
    codigo: str
    detalle: str
    imagen_inserto: str
    porta_herramientas: Tuple[str, ...]
    vc_m_min: str
    ft_mm_rpm: str
    ap_mm: str
    r_mm: str
    clasificacion_iso: Tuple[str, ...]
    imagen_tipo_mecanizado: str
    imagen_plano: str
    medidas_plano: Dict[str, str]

    def to_dict(self) -> dict:
        return {
            "codigo": self.codigo,
            "detalle": self.detalle,
            "imagen_inserto": self.imagen_inserto,
            "porta_herramientas": self.porta_herramientas,
            "vc_m_min": self.vc_m_min,
            "ft_mm_rpm": self.ft_mm_rpm,
            "ap_mm": self.ap_mm,
            "r_mm": self.r_mm,
            "clasificacion_iso": self.clasificacion_iso,
            "imagen_tipo_mecanizado": self.imagen_tipo_mecanizado,
            "imagen_plano": self.imagen_plano,
            "medidas_plano": self.medidas_plano,
        }


class DataLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = self.load_data()

    def load_data(self) -> pd.DataFrame:
        return pd.read_excel(header=1, io=self.file_path)

    def get_df(self) -> pd.DataFrame:
        return self.df

    def _clean_val(self, val, default: str = "-") -> str:
        if pd.isna(val) or val is None or (isinstance(val, float) and math.isnan(val)):
            return default
        cleaned = str(val).strip()
        return cleaned if cleaned else default

    def _parse_iso(self, val) -> Tuple[str, ...]:
        raw_str = self._clean_val(val, "")
        if not raw_str:
            return ()
        
        parts = [p.strip().upper() for p in raw_str.replace(" ", "").split(",") if p.strip()]
        valid_isos = ["P", "M", "K", "N", "S", "H"]
        
        iso_list = []
        for part in parts:
            for char in part:
                if char in valid_isos and char not in iso_list:
                    iso_list.append(char)
                    
        return tuple(iso_list)

    def _parse_porta_herramientas(self, val) -> Tuple[str, ...]:
        raw_str = self._clean_val(val, "")
        if not raw_str or raw_str == "-":
            return ()
        parts = [p.strip() for p in raw_str.split(",") if p.strip()]
        return tuple(parts)

    def _find_asset_image(self, folder_name: str, code: str) -> str:
        # Busca en assets/<folder_name>/<code/>.<ext>
        for ext in [".png", ".jpg", ".jpeg", ".svg", ".webp"]:
            local_path = f"assets/{folder_name}/{code}{ext}"
            if os.path.exists(local_path):
                return f"/{local_path}"
        return ""

    def _parse_medidas_plano(self, val) -> Dict[str, str]:
        raw_str = self._clean_val(val, "")
        if not raw_str or raw_str == "-":
            return {}
        
        medidas = {}
        # Normalizar separadores (saltos de línea o comas entre parejas) a ';'
        items = raw_str.replace("\n", ";").split(";")
        for item in items:
            if ":" in item:
                k, v = item.split(":", 1)
                k_clean = k.strip()
                v_clean = v.strip()
                if k_clean and v_clean:
                    medidas[k_clean] = v_clean
        return medidas

    def find_by_code(self, code: str) -> Optional[Inserto]:
        matches = self.df[self.df["CODIGO"] == code]
        if matches.empty:
            return None

        row = matches.iloc[0]

        codigo = self._clean_val(row.get("CODIGO"), code)
        detalle = self._clean_val(row.get("DETALLE"), "Inserto PCD")
        porta_herramientas = self._parse_porta_herramientas(row.get("PORTA HERRAMIENTAS COMPATIBLE"))
        vc_m_min = self._clean_val(row.get("Vc [m/mm]"), "-")
        ft_mm_rpm = self._clean_val(row.get("Ft [mm/rpm]"), "-")
        ap_mm = self._clean_val(row.get("Ap [mm]"), "-")
        
        # Buscar columna "Radio [mm]" o "Radio" o "R [mm]" en el Excel
        r_mm = "-"
        for col in row.index:
            col_upper = str(col).strip().upper()
            if "RADIO" in col_upper or col_upper.startswith("R [") or col_upper == "R":
                r_mm = self._clean_val(row.get(col), "-")
                break

        # Imágenes asociadas al inserto en sus respectivos subdirectorios dentro de assets/
        imagen_inserto = self._find_asset_image("insertos", codigo)
        imagen_tipo_mecanizado = self._find_asset_image("mecanizados", codigo)
        imagen_plano = self._find_asset_image("planos", codigo)

        # Buscar la columna ISO independientemente de caracteres especiales en el encabezado
        iso_raw = "-"
        for col in row.index:
            if "CLASIFICACI" in str(col).upper() and "ISO" in str(col).upper():
                iso_raw = row.get(col)
                break

        clasificacion_iso = self._parse_iso(iso_raw)

        # Buscar la columna 'Medidas Plano' o 'Cotas Plano' en el Excel
        medidas_raw = "-"
        for col in row.index:
            col_upper = str(col).strip().upper()
            if "COTAS" in col_upper or "MEDIDAS" in col_upper or ("PLANO" in col_upper and "IMAGEN" not in col_upper):
                medidas_raw = row.get(col)
                break

        medidas_plano = self._parse_medidas_plano(medidas_raw)

        return Inserto(
            codigo=codigo,
            detalle=detalle,
            imagen_inserto=imagen_inserto,
            porta_herramientas=porta_herramientas,
            vc_m_min=vc_m_min,
            ft_mm_rpm=ft_mm_rpm,
            ap_mm=ap_mm,
            r_mm=r_mm,
            clasificacion_iso=clasificacion_iso,
            imagen_tipo_mecanizado=imagen_tipo_mecanizado,
            imagen_plano=imagen_plano,
            medidas_plano=medidas_plano
        )


file_path = "./data/INSERTOS POLICRISTALINOS Y HORN.xlsx"
dataLoader = DataLoader(file_path)