import uuid


def generate_custom_identificador(prefix):
    if not prefix.isalpha() or len(prefix) != 3:
        raise ValueError("El prefijo deben ser las primeras 3 letras")

    random_uuid = uuid.uuid4().hex
    random_str = random_uuid[:3].upper()  # Obtener los primeros 5 caracteres hexadecimales en mayúsculas

    custom_identificador = f"{prefix}_{random_str}"

    return custom_identificador