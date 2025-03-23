import streamlit as st #importar la libreria
from groq import Groq #? NUEVA IMPORTACIÓN

#configuración de la ventana de la web
st.set_page_config(page_title = "Mi chat de IA", page_icon= "🎁")
#Titulo de la pagina
st.title("Mi primera aplicación con Streamlit")
#Ingreso de dato del usuario
nombre = st.text_input("¿Cuál es tu nombre?")
#Creamos boton con funcionalidad
if st.button("Saludar") :
    st.write(f"¡Hola {nombre}! Gracias por venir a TercerMundo!!!")

MODELO = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768', 'deepseek-r1-distill-llama-70b']

#Nos conecta a la API, crear un usuario
def crear_usuario_groq():
    clave_secreta = st.secrets["CLAVE_API"] #Obteniendo la clave de nuestro archivo
    return Groq(api_key = clave_secreta) #Crea al usuario

#cliente = usuario de groq | modelo es la IA seleccionada | mensaje del usuario
def configurar_modelo(cliente, modelo, mensaje): 
    return cliente.chat.completions.create(
        model = modelo,
        messages = [{"role":"user", "content": mensaje}],
        stream = True
    ) #Esto nos devuelve la respuesta de la IA

# -> Simula un historial de mensajes
def inicializar_estado(): 
    #Si "mensajes" no esta en st.session_state
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = [] #Memoria de mensajes

def configurar_pagina():
    st.title("Mi chat de IA") #Titulo
    st.sidebar.title("Configuración") #Menu lateral
    elegirModelo = st.sidebar.selectbox(
        "Elegí un modulo", #titulo
        MODELO, #Opciones del menu
        index = 0 #valorDefecto
    )
    return elegirModelo

def actualizar_historial(rol, contenido, avatar):
    #Metodo append() Agraga datos a la lista 
    st.session_state.mensajes.append(
        {"role": rol, "content": contenido, "avatar" : avatar}
    )

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar = mensaje["avatar"]) :
            st.markdown(mensaje["content"])

#Sectror del chat en web
def area_chat():
    contenedorDelChat = st.container(height=400, border = True)
    with contenedorDelChat : mostrar_historial()

#! NUEVA FUNCIÓN - CLASE 9
def generar_respuesta(chat_completo):
    respuesta_completa = "" #variable vacia
    for frase in chat_completo:
        if frase.choices[0].delta.content: #Es si tiene contenido - NONE es vacio
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    
    return respuesta_completa #Lee cuando se termina el for

def main(): 
    #INVOCANDO FUNCIONES DEL CHATBOT
    modelo = configurar_pagina() #Llamamos a la función
    clienteUsuario = crear_usuario_groq() #Conectamos a la API a través de un usuario
    inicializar_estado() #llama a la función historial vacio
    area_chat() #pone en la web el contenedor del chat

    mensaje = st.chat_input("Escribí un mensaje...")

    #! NUEVA ESTRUCTURA DE CÓDIGO
    if mensaje:
        actualizar_historial("user", mensaje, "🧚‍♀️") #Mostramos el mensaje del usuario
        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje) #obteniendo la respuesta
        if chat_completo: #verificamos que tenga contenido
            with st.chat_message("assistant") :
                respuesta_completa = st.write_stream(generar_respuesta(chat_completo))
                actualizar_historial("assistant", respuesta_completa, "🤖")
                st.rerun() #Actualizar.

if __name__ == "__main__":
    main() #una función principal y siempre se invoca
