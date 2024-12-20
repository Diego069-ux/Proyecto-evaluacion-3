import sys
import os

# Añadir la carpeta raíz al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from SERVICIOS.api_service import PostService

def crear_nuevo_post(title, body, userId):
    """
    Lógica de negocio para crear un nuevo post.
    """
    PostService.crear_post(title, body, userId)
    print("Post creado con éxito")

def obtener_posts():
    """
    Lógica de negocio para obtener todos los posts.
    """
    posts = PostService.obtener_posts()
    for post in posts:
        print(f"Post ID: {post.id}, Título: {post.title}, Usuario ID: {post.userId}")

def obtener_post_por_id(post_id):
    """
    Lógica de negocio para obtener un post por su ID.
    """
    post = PostService.obtener_post_por_id(post_id)
    if post:
        print(f"Post ID: {post.id}, Título: {post.title}, Usuario ID: {post.userId}")
    else:
        print("Post no encontrado.")

def actualizar_post(post_id, title, body, userId):
    """
    Lógica de negocio para actualizar un post existente.
    """
    PostService.actualizar_post(post_id, title, body, userId)
    print(f"Post con ID {post_id} actualizado con éxito")

def eliminar_post(post_id):
    """
    Lógica de negocio para eliminar un post.
    """
    PostService.eliminar_post(post_id)
    print(f"Post con ID {post_id} eliminado con éxito")
