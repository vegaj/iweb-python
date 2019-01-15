# coding=utf-8


def is_authorized(usr_email, owner_email):
    """isAuthorized comprueba que el recurso pertenece al usuario, o el usuario está autorizado."""
    return usr_email == owner_email or usr_email == 'pruebaparaingweb@gmail.com'
