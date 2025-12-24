import pandas as pd


def merge_reparticion():
    # 1. Nombres de archivo (ajusta si están en otra carpeta)
    archivo1 = "resultado_merged_2021.xlsx"  # Encabezados: Repartición, Orden, Año, ...
    archivo2 = "titles.xlsx"  # Encabezados: Archivo, Nombre o Razón Social, CUIT, Repartición, Orden, Año, ...
    archivo_salida = "Presenta título y aporte 2021.xlsx"

    # 2. Leer ambos Excel
    df1 = pd.read_excel(archivo1)
    df2 = pd.read_excel(archivo2)

    # 3. Diccionario de equivalencias para unificar reparticiones
    map_reparticion = {
        "INM": "Inmueble",
        "AUT": "Automotor",
        "CI": "Comercio e Industria",
    }

    # 4. Normalizar la Repartición en df1 a “Inmueble”, “Automotor” o “Comercio e Industria”
    df1["Reparticion_norm"] = df1["Tasa"].replace(map_reparticion)

    # 5. Merge basándonos en (Orden, Año, Reparticion_norm) vs. (Orden, Año, Repartición) en df2
    df_merged = df1.merge(
        df2,
        how="left",
        left_on=["N° de Orden", "Reparticion_norm"],
        right_on=["Orden", "Repartición"],
    )

    # 6. Quedarnos con columnas relevantes (ajusta según necesites)
    columnas_finales = [
        "Reparticion_norm",  # la vamos a renombrar luego
        "Orden",
        "Año",
        "expedienteSAC",
        "CARATULA",
        "Planilla/PDF",
        "Archivo",
        "Nombre o Razón Social",
        "CUIT",
        "Identificador",
        "Domicilio",
        "Matrícula",
        "Monto total",
        "Tipo de Persona",
    ]
    # Exportar todas las columnas resultantes del merge
    print("Columnas después del merge:", df_merged.columns.tolist())
    print("Primeras filas después del merge:")
    print(df_merged.head(10).to_string(index=False))

    # 7. Renombrar la columna "Reparticion_norm" a "Repartición" si existe
    if "Reparticion_norm" in df_merged.columns:
        df_merged.rename(columns={"Reparticion_norm": "Repartición"}, inplace=True)
    if "expedienteSAC" in df_merged.columns:
        df_merged.rename(columns={"expedienteSAC": "IdSAC"}, inplace=True)

    # 8. Guardar con formato básico (encabezado en negrita, ajuste ancho de columnas)
    #    utilizando XlsxWriter:
    with pd.ExcelWriter(archivo_salida, engine="xlsxwriter") as writer:
        df_merged.to_excel(writer, sheet_name="Sheet1", index=False)

        # Obtener workbook y worksheet
        workbook = writer.book
        worksheet = writer.sheets["Sheet1"]

        # Crear formato de encabezado en negrita
        header_format = workbook.add_format(
            {"bold": True, "text_wrap": True, "valign": "middle", "border": 1}
        )

        # Aplicar el formato a la fila de encabezados
        for col_num, value in enumerate(df_merged.columns.values):
            worksheet.write(0, col_num, value, header_format)

        # Ajustar ancho de columnas automáticamente (robusto a columnas vacías)
        for i, col in enumerate(df_merged.columns):
            try:
                col_data = df_merged[col].fillna("").astype(str)
                max_length = max([len(str(col))] + [len(x) for x in col_data])
                worksheet.set_column(i, i, max_length + 2)
            except Exception as e:
                print(f"Error ajustando ancho para columna {col}: {e}")

    print(f"Merge completado. Archivo generado: {archivo_salida}")


if __name__ == "__main__":
    merge_reparticion()
