import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from MODELOS.post import db, Post  # importación

class PostService:
    @staticmethod
    def crear_post(title, body, user_id):
        try:
            nuevo_post = Post(title=title, body=body, userId=user_id)
            db.session.add(nuevo_post)
            db.session.commit()
            return nuevo_post
        except Exception as e:
            print(f"Error creando post: {e}")
            return None

    @staticmethod
    def obtener_posts():
        try:
            posts = Post.query.all()
            return posts
        except Exception as e:
            print(f"Error obteniendo posts: {e}")
            return None

    @staticmethod
    def obtener_post_por_id(post_id):
        try:
            post = Post.query.get(post_id)
            return post
        except Exception as e:
            print(f"Error obteniendo post por ID: {e}")
            return None

    @staticmethod
    def actualizar_post(post_id, title, body, user_id):
        try:
            post = Post.query.get(post_id)
            if post:
                post.title = title
                post.body = body
                post.userId = user_id
                db.session.commit()
                return post
            else:
                return None
        except Exception as e:
            print(f"Error actualizando post: {e}")
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
                return False
        except Exception as e:
            print(f"Error eliminando post: {e}")
            return False
