# File: config.py

import os

users = {
    "FONSECA": {
        "matricula": "1-27245",
        "password": os.getenv("FONSECA_PASSWORD", ""),
        "procurador": "FONSECA, MARIO ROBERTO",
        "numero_decreto": "187/2020",
        "fecha_decreto": "29/04/2020",
        "municipalidad_keyname_to_search": "municipalidad",
        "municipalidad_keyname_to_represent": "MUNICIPALIDAD DE CÓRDOBA",
    },
}

cookies = os.getenv("JUSTICIACORDOBA_COOKIES", "")
digital_firmados_titles_foldername= "Titulos Fonseca (24-12-2025)"
digital_firmados_iniciar_demanda_filename = "Titulos Fonseca (24-12-2025)_A.xlsx"