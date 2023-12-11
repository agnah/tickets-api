import uuid


def generate_custom_identificador(prefix):
    if not prefix.isalpha() or len(prefix) in ['TI', 'TR']:
        raise ValueError("El prefijo debe ser de tipo 'TI' o 'TR'")

    random_uuid = uuid.uuid4().hex
    random_str = random_uuid[:8].upper()  # Obtener los primeros 5 caracteres hexadecimales en mayúsculas

    custom_identificador = f"{prefix}_{random_str}"

    return custom_identificador