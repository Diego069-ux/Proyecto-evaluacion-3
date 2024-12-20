import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from MODELOS.post import db, Post  

class PostService:
    @staticmethod
    def crear_post(title, body, user_id):
        try:
            nuevo_post = Post(title=title, body=body, user_id=user_id)  
            db.session.add(nuevo_post)
            db.session.commit()
            return nuevo_post
        except Exception as e:
            print(f"Error creando post: {str(e)}")  # Más detalle en el error
            return None

    @staticmethod
    def obtener_posts():
        try:
            posts = Post.query.all()
            if posts:  # Verifica si existen posts
                return posts
            else:
                return []  # Devuelve una lista vacía si no hay posts
        except Exception as e:
            print(f"Error obteniendo posts: {str(e)}")  # Detalles del error
            return []  # Devuelve una lista vacía en caso de error

    @staticmethod
    def obtener_post_por_id(post_id):
        try:
            post = Post.query.get(post_id)
            if post:  # Verifica si el post existe
                return post
            else:
                return None
        except Exception as e:
            print(f"Error obteniendo post por ID: {str(e)}")  # Detalles del error
            return None

    @staticmethod
    def actualizar_post(post_id, title, body, user_id):
        try:
            post = Post.query.get(post_id)
            if post:
                post.title = title
                post.body = body
                post.user_id = user_id  
                db.session.commit()
                return post
            else:
                return None  # Si el post no existe, retornar None
        except Exception as e:
            print(f"Error actualizando post: {str(e)}")  # Más detalles en el error
            return None

    @staticmethod
    def eliminar_post(post_id):
        try:
            post = Post.query.get(post_id)
            if post:
                db.session.delete(post)
                db.session.commit()
                return True
            else:
                return False  # Si el post no existe, retornar False
        except Exception as e:
            print(f"Error eliminando post: {str(e)}")  # Más detalles en el error
            return False
