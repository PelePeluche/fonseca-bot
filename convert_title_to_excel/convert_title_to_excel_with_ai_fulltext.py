import os
import pytesseract
from pdf2image import convert_from_path
import pandas as pd
import openai
from dotenv import load_dotenv
import json
import re

# Cargar la clave de OpenAI desde el archivo .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Campos básicos a extraer y guardar
basic_fields = ["Archivo", "Nombre", "CUIT", "Monto", "Domicilio", "Causa Nro.", "Orden", "Repartición"]

def read_pdf_with_ocr(pdf_path):
    """Extrae texto de un PDF usando OCR."""
    all_text = ""
    try:
        images = convert_from_path(pdf_path)
        for image in images:
            text = pytesseract.image_to_string(image, lang='spa')
            all_text += text + "\n"
    except Exception as e:
        print(f"Error al procesar OCR para {pdf_path}: {e}")
    return all_text

def extract_fields_with_ai_fulltext(text, filename):
    """Envía TODO el texto a GPT-4o vía OpenAI API y extrae los campos clave en JSON."""
    prompt = f"""
INSTRUCCIONES ESTRICTAS:
Responde SOLO en JSON, sin ningún comentario, explicación ni texto adicional.
Si algún campo no está, deja el valor vacío ("").
El formato debe ser EXACTAMENTE el siguiente:
{{
  "Archivo": "{filename}",
  "Nombre": "",
  "CUIT": "",
  "Monto": "",
  "Domicilio": "",
  "Causa Nro.": "",
  "Orden": "",
  "Repartición": ""
}}

IMPORTANTE sobre los campos:
- CUIT: Si el CUIT no aparece explícitamente, busca valores bajo etiquetas como NroDoc, Nro Doc, Documento, DNI, o similares, y colócalo en el campo CUIT si parece un número de identificación.
- Monto: Si hay más de un monto, elige el que NO incluya el gasto de franqueo o gastos de franqueo. Si hay un monto que incluye franqueo y otro que no, elige el que NO lo incluye. Si solo hay uno, usa ese.
- Monto: El valor debe estar estandarizado en formato argentino, es decir: sin puntos de mil, solo usar coma para los centavos, y siempre mostrar dos decimales (por ejemplo: 12345,67 o 1500,00). No usar puntos para separar miles bajo ninguna circunstancia.

TEXTO:
{text}
"""
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=400
        )
        raw = response.choices[0].message.content.strip()
        # Remueve bloque markdown si existe
        if raw.startswith("```"):
            raw = re.sub(r"^```[a-zA-Z]*\n?", "", raw)
            raw = re.sub(r"\n?```$", "", raw)
            raw = raw.strip()
        try:
            fields = json.loads(raw)
        except Exception:
            print(f"No se pudo extraer JSON puro de la respuesta (respuesta limpia):\n{raw}")
            fields = {k: "" for k in basic_fields}
            fields["Archivo"] = filename
        filtered_fields = {k: fields.get(k, "") for k in basic_fields}
        return filtered_fields
    except Exception as e:
        print(f"Error llamando a OpenAI: {e}")
        return {k: "" for k in basic_fields | {"Archivo": filename}}

def process_folder_with_ai_fulltext(folder_path, output_excel_path):
    """Procesa todos los PDFs en la carpeta, extrae datos usando IA y guarda en Excel (envía TODO el texto)."""
    data = []
    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
    pdf_files = sorted(pdf_files)  # Procesa todos los archivos
    for filename in pdf_files:
        pdf_path = os.path.join(folder_path, filename)
        print(f'Leyendo y procesando {filename}...')
        text = read_pdf_with_ocr(pdf_path)
        fields = extract_fields_with_ai_fulltext(text, filename)
        print(f"Campos extraídos para {filename}: {fields}")
        data.append(fields)

    # Guardar en Excel solo los campos básicos
    df = pd.DataFrame(data)
    df = df.reindex(columns=basic_fields)
    df.to_excel(output_excel_path, index=False)
    print(f"Datos guardados exitosamente en {output_excel_path}")

if __name__ == '__main__':
    folder_path = '/home/peluche/Escritorio/Ramiro Bot/fonseca-bot/titles/Títulos adjuntos causas 2021/'
    output_excel_path = 'Títulos adjuntos causas 2021.xlsx'
    process_folder_with_ai_fulltext(folder_path, output_excel_path)
