"""Funciones de validación de entrada del usuario."""
import re
import unicodedata

from app.domain.cedula_validator import validate_cedula as _validate_cedula


_NUMBER_WORDS = {
    "cero": 0, "un": 1, "uno": 1, "una": 1, "dos": 2, "tres": 3,
    "cuatro": 4, "cinco": 5, "seis": 6, "siete": 7, "ocho": 8, "nueve": 9,
    "diez": 10, "once": 11, "doce": 12, "trece": 13, "catorce": 14,
    "quince": 15, "dieciseis": 16, "diecisiete": 17, "dieciocho": 18,
    "diecinueve": 19, "veinte": 20, "veintiuno": 21, "veintidos": 22,
    "veintitres": 23, "veinticuatro": 24, "veinticinco": 25, "veintiseis": 26,
    "veintisiete": 27, "veintiocho": 28, "veintinueve": 29, "treinta": 30,
    "cuarenta": 40, "cincuenta": 50, "sesenta": 60, "setenta": 70,
    "ochenta": 80, "noventa": 90, "cien": 100, "ciento": 100,
    "doscientos": 200, "trescientos": 300, "cuatrocientos": 400,
    "quinientos": 500, "seiscientos": 600, "setecientos": 700,
    "ochocientos": 800, "novecientos": 900,
}


def parse_spanish_number(value: str) -> int:
    """Extrae un número entero escrito en español, hasta miles."""
    text = unicodedata.normalize("NFKD", value or "")
    text = "".join(char for char in text if not unicodedata.combining(char)).lower()
    tokens = re.findall(r"[a-z]+", text)
    allowed_context = {"y", "mil", "dolar", "dolares", "usd", "mes", "meses", "plazo", "plazos", "opcion", "numero"}
    if not tokens or any(token not in _NUMBER_WORDS and token not in allowed_context for token in tokens):
        raise ValueError("No se encontró un número escrito.")
    total = current = 0
    found = False
    for token in tokens:
        if token == "y":
            continue
        if token == "mil":
            total += max(current, 1) * 1000
            current = 0
            found = True
        elif token in _NUMBER_WORDS:
            current += _NUMBER_WORDS[token]
            found = True
    if not found:
        raise ValueError("No se encontró un número escrito.")
    return total + current


def validate_cedula(value: str) -> tuple[bool, str | None]:
    """Valida una cédula ecuatoriana (delega en el dominio, algoritmo módulo 10)."""
    if value is None:
        return False, "La cédula es obligatoria."
    return _validate_cedula(value)


def parse_numeric_value(value: str) -> float:
    """Convierte texto numérico a float, soportando coma decimal y separador de miles."""
    cleaned = value.strip().replace(" ", "")
    cleaned = cleaned.replace("$", "").replace("usd", "").replace("USD", "")
    if "," in cleaned:
        parts = cleaned.split(",")
        if len(parts) == 2 and len(parts[1]) in (1, 2):
            cleaned = parts[0].replace(".", "") + "." + parts[1]
        else:
            cleaned = cleaned.replace(",", "")
    elif "." in cleaned:
        integer_part, fractional_part = cleaned.rsplit(".", 1)
        if len(fractional_part) == 3 and integer_part.replace(".", "").isdigit():
            cleaned = cleaned.replace(".", "")
    try:
        return float(cleaned)
    except ValueError:
        return float(parse_spanish_number(value))


def parse_term_value(value: str) -> int:
    """Extrae el plazo en meses desde texto como '12', '12 meses' o 'en 12 plazos'."""
    cleaned = value.strip()
    try:
        return int(cleaned)
    except ValueError:
        pass
    match = re.search(r"(\d{1,2})", cleaned)
    if not match:
        return parse_spanish_number(value)
        raise ValueError("No se encontró un plazo numérico.")
    return int(match.group(1))


def validate_name(value: str) -> tuple[bool, str | None]:
    """Valida que el nombre tenga al menos 2 palabras o 5 caracteres."""
    cleaned = value.strip()
    if len(cleaned) < 5 and len(cleaned.split()) < 2:
        return False, "El nombre debe tener al menos 2 palabras o 5 caracteres."
    return True, None


def validate_amount(value: str) -> tuple[bool, str | None]:
    """Valida que el monto sea un número positivo."""
    try:
        amount = parse_numeric_value(value)
    except ValueError:
        return False, "El monto debe ser un número válido."

    if amount <= 0:
        return False, "El monto debe ser mayor a 0."

    return True, None


def validate_purpose(value: str) -> tuple[bool, str | None]:
    """Valida que el destino del crédito sea concreto (no saludos ni basura)."""
    import unicodedata

    cleaned = (value or "").strip()
    if len(cleaned) < 4:
        return False, "Indica brevemente para qué necesitas el crédito."

    text = unicodedata.normalize("NFKD", cleaned)
    text = "".join(char for char in text if not unicodedata.combining(char))
    text = text.lower().strip()

    rejected = {
        "hola",
        "hello",
        "hi",
        "ok",
        "okay",
        "si",
        "no",
        "gracias",
        "asesor",
        "humano",
        "menu",
        "cancelar",
        "reiniciar",
        "info",
        "informacion",
        "1",
        "2",
        "3",
        "0",
        "test",
        "prueba",
        "nada",
        "nose",
        "no se",
    }
    if text in rejected:
        return False, "Indica un destino concreto del crédito."

    purpose_keywords = {
        "estudio",
        "estudios",
        "negocio",
        "consumo",
        "emergencia",
        "vivienda",
        "casa",
        "vehiculo",
        "auto",
        "carro",
        "salud",
        "medico",
        "viaje",
        "deuda",
        "refinanci",
        "inversion",
        "capital",
        "trabajo",
        "empresa",
        "reparacion",
        "remodelacion",
        "educacion",
        "universidad",
        "matrimonio",
        "personal",
    }
    if any(keyword in text for keyword in purpose_keywords):
        return True, None

    # Texto libre razonable: letras suficientes y no solo saludo/basura.
    tokens = set(re.findall(r"[a-z0-9]+", text))
    if tokens and tokens <= rejected:
        return False, "Indica un destino concreto del crédito."
    if len(cleaned) >= 5 and re.search(r"[a-zA-ZáéíóúÁÉÍÓÚñÑ]", cleaned):
        return True, None
    return False, "Indica un destino concreto del crédito."


def validate_term(value: str) -> tuple[bool, str | None]:
    """Valida que el plazo sea un entero entre 3 y 36 meses."""
    try:
        term = parse_term_value(value)
    except ValueError:
        return False, "El plazo debe ser un número entero."

    if term < 3 or term > 36:
        return False, "El plazo debe estar entre 3 y 36 meses."

    return True, None


def validate_income(value: str) -> tuple[bool, str | None]:
    """Valida que el ingreso sea un número positivo."""
    try:
        income = parse_numeric_value(value)
    except ValueError:
        return False, "El ingreso debe ser un número válido."

    if income <= 0:
        return False, "El ingreso debe ser mayor a 0."

    return True, None


def validate_menu_option(value: str) -> tuple[bool, str | None]:
    """Valida que la opción del menú sea 1, 2 o 3."""
    cleaned = value.strip()
    if cleaned not in {"1", "2", "3"}:
        return False, "Selecciona una opción válida: 1, 2 o 3."
    return True, None


def validate_confirmation(value: str) -> tuple[bool, str | None]:
    """Valida que la confirmación sea 1 (Sí) o 2 (No)."""
    cleaned = value.strip()
    if cleaned not in {"1", "2"}:
        return False, "Selecciona una opción válida: 1 (Sí) o 2 (No)."
    return True, None
