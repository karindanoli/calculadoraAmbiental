import os
import tempfile
import uuid


def save_uploaded_file(file_content, file_name):
    """
    Salva o arquivo que foi subido para um diretório temporário
    """

    _, file_extension = os.path.splitext(file_name)
    file_id = str(uuid.uuid4())
    file_path = os.path.join(tempfile.gettempdir(), f"{file_id}{file_extension}")

    with open(file_path, "wb") as file:
        file.write(file_content.getbuffer())

    return file_path
