import streamlit as st
import pandas as pd
import json
import os

# Archivo JSON para almacenar los productos
DATA_FILE = "productos.json"

def cargar_datos():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {}

def guardar_datos(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def registrar_producto(codigo, nombre, precio):
    data = cargar_datos()
    data[codigo] = {"nombre": nombre, "precio": precio}
    guardar_datos(data)

def actualizar_producto(codigo, nombre, precio):
    data = cargar_datos()
    if codigo in data:
        data[codigo] = {"nombre": nombre, "precio": precio}
        guardar_datos(data)
        return True
    return False

def eliminar_producto(codigo):
    data = cargar_datos()
    if codigo in data:
        del data[codigo]
        guardar_datos(data)
        return True
    return False

def consultar_todos():
    return cargar_datos()

def main():
    st.sidebar.title("Menú")
    
    # Panel Principal
    panel_principal = st.sidebar.selectbox("Panel Principal", ["Consulta de Precios"], key="panel_principal")
    submenu_opcion = st.sidebar.selectbox("Funciones Administrativas", ["", 
        "Registrar Producto", "Actualizar Producto", "Consultar Todos los Productos", 
        "Eliminar Producto", "Importar/Exportar Datos"
    ], key="submenu_opcion")
    
    # Mostrar total acumulado en el panel lateral
    if "total_acumulado" not in st.session_state:
        st.session_state.total_acumulado = 0.00
    
    if "productos_escaneados" not in st.session_state:
        st.session_state.productos_escaneados = []

    if panel_principal == "Consulta de Precios":
        st.title("Consulta de Precios")
        st.subheader("Escanea un producto para ver su precio")
        codigo = st.text_input("Código de barras", key="codigo_consulta")
        
        # Mostrar total acumulado debajo del campo de código de barras
       # st.subheader("Total acumulado")
        #st.markdown(f"### 💲 {st.session_state.total_acumulado:.2f}")
        
        if codigo:
            productos = cargar_datos()
            if codigo in productos:
                producto = productos[codigo]
                st.success(f"{producto['nombre']}: ${producto['precio']}")
                
                # Agregar el producto a la lista de productos escaneados
                st.session_state.productos_escaneados.append(producto)
                # Sumar el precio al total acumulado inmediatamente
                st.session_state.total_acumulado += producto['precio']
            else:
                st.error("Producto no encontrado")

        # Mostrar el total fuera de la tabla con un tamaño de fuente grande
        st.markdown(f"<h3 style='text-align: left; color: white;'>Total acumulado:<br><br> 💲 {st.session_state.total_acumulado:.2f}</h3>", unsafe_allow_html=True)
        
        # Mostrar la tabla de productos escaneados
        st.subheader("Productos escaneados")
        if st.session_state.productos_escaneados:
            # Crear un dataframe para mostrar los productos escaneados
            df_escaneados = pd.DataFrame(st.session_state.productos_escaneados)
            df_escaneados.set_index('nombre', inplace=True)  # Establecer 'nombre' como índice
            df_escaneados = df_escaneados[['precio']]  # Solo mostrar la columna de precio
            
            # Agregar una fila con la suma de los precios al final de la tabla
            suma_total = df_escaneados['precio'].sum()
            #df_escaneados.loc['Total', 'precio'] = suma_total

            st.dataframe(df_escaneados)
        
        # Mostrar el total fuera de la tabla con un tamaño de fuente grande
        #st.markdown(f"<h3 style='text-align: left; color: white;'>Total acumulado:<br><br> 💲 {st.session_state.total_acumulado:.2f}</h3>", unsafe_allow_html=True)
    
    if submenu_opcion == "Registrar Producto":
        st.title("Registrar Producto")
        codigo = st.text_input("Código de barras", key="codigo_registro")
        nombre = st.text_input("Nombre del producto", key="nombre_registro")
        precio = st.number_input("Precio", min_value=0.0, format="%.2f", key="precio_registro")
        
        if st.button("Registrar"):
            registrar_producto(codigo, nombre, precio)
            st.success("Producto registrado con éxito")
    
    elif submenu_opcion == "Actualizar Producto":
        st.title("Actualizar Producto")
        codigo = st.text_input("Código de barras", key="codigo_actualizar")
        nombre = st.text_input("Nuevo nombre del producto", key="nombre_actualizar")
        precio = st.number_input("Nuevo precio", min_value=0.0, format="%.2f", key="precio_actualizar")
        
        if st.button("Actualizar"):
            if actualizar_producto(codigo, nombre, precio):
                st.success("Producto actualizado")
            else:
                st.error("Producto no encontrado")
    
    elif submenu_opcion == "Consultar Todos los Productos":
        st.title("Lista de Productos")
        productos = consultar_todos()
        df = pd.DataFrame.from_dict(productos, orient='index')
        st.dataframe(df)
    
    elif submenu_opcion == "Eliminar Producto":
        st.title("Eliminar Producto")
        codigo = st.text_input("Código de barras", key="codigo_eliminar")
        if st.button("Eliminar"):
            if eliminar_producto(codigo):
                st.success("Producto eliminado")
            else:
                st.error("Producto no encontrado")
    
    elif submenu_opcion == "Importar/Exportar Datos":
        st.title("Importar / Exportar Datos")
        
        if st.button("Exportar Datos a JSON"):
            st.download_button(
                label="Descargar JSON", 
                data=json.dumps(cargar_datos(), indent=4), 
                file_name="productos.json",
                mime="application/json"
            )

if __name__ == "__main__":
    main()
