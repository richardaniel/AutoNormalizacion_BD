import pandas as pd
import interface

from interface import create_interface, display_tables

def read_excel_tables(filename, sheet_name='Sheet1'):
    # Lee la hoja de Excel
    df = pd.read_excel(filename, sheet_name=sheet_name, header=None)
    
    tables = []
    roles_info = []  # Lista para almacenar la información de roles de las columnas
    start_row = 0
    while start_row < len(df):
        # Encuentra la próxima fila vacía
        end_row = start_row
        while end_row < len(df) and pd.notna(df.iloc[end_row, 0]):
            end_row += 1

        # Extrae la tabla
        table_df = df.iloc[start_row:end_row].reset_index(drop=True)
        if len(table_df) > 1:
            # La primera fila contiene roles (PK, FK, None) y la segunda fila contiene nombres de columnas
            roles = table_df.iloc[0].dropna().tolist()
            column_names = table_df.iloc[1].tolist()
            
            # Solo continuar si la segunda fila tiene nombres de columnas válidos
            if column_names:
                table_df.columns = column_names
                table_df = table_df[2:]
                table_df.reset_index(drop=True, inplace=True)
                
                # Elimina las columnas que solo contienen NaN
                table_df.dropna(axis=1, how='all', inplace=True)
                
                # Guarda la información de roles, solo si la primera fila de roles no está vacía
                if any(pd.notna(role) for role in roles):
                    column_roles = {col: role for col, role in zip(table_df.columns, roles)}
                    roles_info.append(column_roles)
                else:
                    roles_info.append({})  # Agrega un diccionario vacío para roles si no hay roles definidos
                
                tables.append(table_df)
        
        # Mueve la fila de inicio a la siguiente tabla
        start_row = end_row + 1
    
    return tables, roles_info

if __name__ == "__main__":
    tables, roles_info = read_excel_tables("formato.xlsx")
    interface.tables = tables  # Actualiza las tablas globales
    interface.roles_info = roles_info  # Actualiza la información de roles
    interface.table_names = [f"Tabla {i + 1}" for i in range(len(tables))]  # Inicializa los nombres de las tablas
    root = create_interface()
    display_tables(tables, roles_info)  # Mostrar las tablas en el panel derecho
    root.mainloop()
