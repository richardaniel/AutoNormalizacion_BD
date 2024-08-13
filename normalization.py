import pandas as pd

def is_non_atomic(value):
    """
    Verifica si el valor es una cadena con valores separados por comas.
    """
    return isinstance(value, str) and ',' in value

def convert_to_1fn(table_df):
    """
    Convierte una tabla a la Primera Forma Normal (1FN).
    La conversión implica descomponer columnas con valores no atómicos en filas separadas.
    """
    # Copia la tabla original para no modificar el DataFrame original
    normalized_df = table_df.copy()
    
    # Lista para almacenar las columnas con valores no atómicos
    non_atomic_cols = [col for col in normalized_df.columns if normalized_df[col].apply(is_non_atomic).any()]
    
    # Mientras haya columnas con valores no atómicos, sigue normalizando
    while non_atomic_cols:
        col = non_atomic_cols[0]
        
        # Descompone la columna con valores separados por comas en varias filas
        expanded_df = normalized_df.copy()
        expanded_df[col] = expanded_df[col].apply(lambda x: x.split(',') if is_non_atomic(x) else [x])
        expanded_df = expanded_df.explode(col)
        
        # Actualiza la lista de columnas no atómicas y la tabla normalizada
        normalized_df = expanded_df
        non_atomic_cols = [c for c in normalized_df.columns if normalized_df[c].apply(is_non_atomic).any()]

    return normalized_df

def check_and_convert_1fn(tables):
    """
    Revisa si las tablas están en 1FN y las convierte a 1FN si es necesario.
    """
    converted_tables = []
    for table_df in tables:
        converted_df = convert_to_1fn(table_df)
        converted_tables.append(converted_df)
    
    return converted_tables

def is_composite_key(roles):
    """
    Verifica si una clave primaria es compuesta.
    """
    return len([role for role in roles if role == 'PK']) > 1

def convert_to_2fn(tables, roles_info):
    """
    Convierte las tablas de 1FN a 2FN.
    """
    converted_tables = []

    for table_df, roles in zip(tables, roles_info):
        # Identificar columnas que forman la clave primaria
        primary_keys = [col for col, role in roles.items() if role == 'PK']
        
        if is_composite_key(roles.values()):
            # Identificar columnas con dependencias parciales
            partial_dependent_cols = []
            non_primary_cols = [col for col in table_df.columns if col not in primary_keys]
            
            for col in non_primary_cols:
                # Verificar dependencia parcial
                grouped = table_df.groupby(primary_keys).agg({col: 'nunique'})
                if grouped[col].nunique() > 1:
                    partial_dependent_cols.append(col)
            
            if partial_dependent_cols:
                # Crear nueva tabla para atributos dependientes
                detail_cols = primary_keys + partial_dependent_cols
                detail_table = table_df[detail_cols].drop_duplicates()
                
                # Crear nueva tabla para atributos no dependientes
                non_partial_cols = [col for col in non_primary_cols if col not in partial_dependent_cols]
                order_cols = primary_keys + non_partial_cols
                order_table = table_df[order_cols].drop_duplicates()
                
                converted_tables.append(order_table)
                converted_tables.append(detail_table)
            else:
                # La tabla ya está en 2FN
                converted_tables.append(table_df)
        else:
            # La tabla ya está en 2FN
            converted_tables.append(table_df)

    return converted_tables

def check_and_convert_2fn(tables, roles_info):
    """
    Revisa si las tablas están en 2FN y las convierte a 2FN si es necesario.
    """
    converted_tables = convert_to_2fn(tables, roles_info)
    return converted_tables

def check_and_convert_3fn(tables):
    """
    Revisa si las tablas están en 3FN y las convierte a 3FN si es necesario.
    """
    # Aquí deberías implementar la lógica para verificar y convertir tablas a 3FN
    # Por ahora, solo se devuelve la tabla sin cambios
    converted_tables = []
    for table_df in tables:
        # Lógica para 3FN (por definir)
        converted_tables.append(table_df)
    
    return converted_tables

