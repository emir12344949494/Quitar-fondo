import os
from PIL import Image
from rembg import remove
import streamlit as st
from io import BytesIO

icono = Image.open("icono.ico")

st.set_page_config(
    page_title="Elimina fondo imágenes", 
    page_icon=icono
)


def archivo_cargado_guardado(uploaded_file):
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    file_path = os.path.join(upload_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path


def archivo_guardado2(input_img_file, formato_descarga):
    input_img_path = archivo_cargado_guardado(input_img_file)
    nombre_base = os.path.splitext(input_img_path)[0]
    output_img_path = f"{nombre_base}_rmbg.{formato_descarga.lower()}"

    try:
        image = Image.open(input_img_path)
        output = remove(image)

        buffer = BytesIO()
        output.save(buffer, format=formato_descarga.upper())
        buffer.seek(0)

        col1, col2 = st.columns(2)

        with col1:
            st.header("Antes")
            st.image(input_img_path, caption="Imagen Original")
            with open(input_img_path, "rb") as img_file:
                st.download_button(
                    label="⬇️ Descargar Imagen Original",
                    data=img_file,
                    file_name=os.path.basename(input_img_path),
                    mime="image/jpeg",
                )

        with col2:
            st.header("Después (sin fondo)")
            st.image(output, caption="Imagen Procesada (sin fondo)")
            st.download_button(
                label=f"⬇ Descargar sin fondo ({formato_descarga})",
                data=buffer,
                file_name=os.path.basename(output_img_path),
                mime=f"image/{formato_descarga.lower()}",
            )

        st.success("El fondo ha sido eliminado con éxito")

    except Exception as e:
        st.error(f"Error al eliminar el fondo: {e}")


def main():
    st.title("Eliminador de Fondo de Imágenes")
    uploaded_file = st.file_uploader("Carga una imagen", type=["jpg", "jpeg", "png", "svg"])


if __name__ == "__main__":
    main()
