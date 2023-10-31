# -*- coding: utf-8 -*-

import getpass
from rbac import RBAC, RBACAuthorizationError

rbac = RBAC()

# Creación de roles
admin_role = rbac.create_role('Admin')
asistente_role = rbac.create_role('Asistente')
vendedor_role = rbac.create_role('Vendedor')

# Creación de dominios
venta = rbac.create_domain('Venta')
productos = rbac.create_domain('Productos')
usuario = rbac.create_domain('Usuario')

# Creación de permisos
crear_venta_permission = rbac.create_permission('Crear venta')
modificar_venta_permission = rbac.create_permission('Modificar venta')
eliminar_venta_permission = rbac.create_permission('Eliminar venta')
listar_productos_permission = rbac.create_permission('Listar productos')
agregar_productos_permission = rbac.create_permission('Agregar productos')
desactivar_productos_permission = rbac.create_permission('Desactivar productos')
agregar_usuario_permission = rbac.create_permission('Agregar usuario')

# Añadir permisos a los roles
admin_role.add_permission(crear_venta_permission, venta)
admin_role.add_permission(modificar_venta_permission, venta)
admin_role.add_permission(eliminar_venta_permission, venta)
admin_role.add_permission(listar_productos_permission, productos)
admin_role.add_permission(agregar_productos_permission, productos)
admin_role.add_permission(desactivar_productos_permission, productos)
admin_role.add_permission(agregar_usuario_permission, usuario)

asistente_role.add_permission(crear_venta_permission, venta)
asistente_role.add_permission(modificar_venta_permission, venta)
asistente_role.add_permission(listar_productos_permission, productos)
asistente_role.add_permission(agregar_productos_permission, productos)
asistente_role.add_permission(desactivar_productos_permission, productos)

vendedor_role.add_permission(listar_productos_permission, productos)

# Creación de usuarios y asignación de funciones
usuario_admin = rbac.create_subject('Admin')
usuario_admin.authorize(admin_role)

usuario_asistente = rbac.create_subject('Asistente')
usuario_asistente.authorize(asistente_role)

usuario_vendedor = rbac.create_subject('Vendedor')
usuario_vendedor.authorize(vendedor_role)

utilisateur = rbac.create_subject('User')
utilisateur.authorize(admin_role)

# Creación de acciones y funciones disponibles
acciones = {
    'Crear venta': crear_venta_permission,
    'Modificar venta': modificar_venta_permission,
    'Eliminar venta': eliminar_venta_permission,
    'Listar productos': listar_productos_permission,
    'Agregar productos': agregar_productos_permission,
    'Desactivar productos': desactivar_productos_permission,
    'Agregar usuario': agregar_usuario_permission
    }

funciones_dispo = {
    'Admin': {
        'permissions': [crear_venta_permission, modificar_venta_permission, eliminar_venta_permission, listar_productos_permission, agregar_productos_permission, desactivar_productos_permission, agregar_usuario_permission],
    },
    'Asistente': {
        'permissions': [crear_venta_permission, modificar_venta_permission, listar_productos_permission, agregar_productos_permission, desactivar_productos_permission],
    },
    'Vendedor': {
        'permissions': [listar_productos_permission]
    }
 }

permission_domain = {
    'Venta': {'permissions' : [crear_venta_permission, modificar_venta_permission, eliminar_venta_permission]},
    'Productos': {'permissions' : [listar_productos_permission, agregar_productos_permission, desactivar_productos_permission]},
    'Usuario': {'permissions' : [agregar_usuario_permission]}
}

# Base de datos de usuarios
usuarios = {
    "Admin": "Admin",
    "Asistente": "Asistente",
    "Vendedor": "Vendedor"
}

rbac.lock()


#######################################Interacción con el usuario#####################################

# Pedir al usuario que se conecte
# Bucle de conexión
while True:
    # Pedir al usuario que inicie sesión
    funcione_usuario = input("Nombre de usuario : ")
    contrasena = getpass.getpass("Contrase\u00f1a : ")

    # Compruebe los detalles de su conexión
    if funcione_usuario in usuarios and usuarios[funcione_usuario] == contrasena:
        print("Conexi\u00f3n correcta.")
        sujet_utilisateur = None
        if funcione_usuario == "Admin":
            sujet_utilisateur = usuario_admin
        elif funcione_usuario == "Asistente":
            sujet_utilisateur = usuario_asistente
        elif funcione_usuario == "Vendedor":
            sujet_utilisateur = usuario_vendedor
        else:
            sujet_utilisateur = utilisateur
        # El usuario está conectado, salir del bucle
        break
    else:
        print("\nNombre de usuario o contrase\u00f1a incorrectos. Por favor, intentelo de nuevo.\n")

print("\nDominios disponibles :")
for domain in [venta, productos, usuario]:
    print("-",domain.name)

while True:
    dominio_usuario = input("\nElija la zona en la que desea realizar la acci\u00f3n (s para salir): ")
    
    #Si l'utilisateur veut quitter la boucle
    if dominio_usuario == "s":
        break
    
    # Vérifiez si le domaine choisi par l'utilisateur existe dans la liste des domaines disponibles
    if dominio_usuario in [domain.name for domain in [venta, productos, usuario]]:
        dominio_elije = [domain for domain in [venta, productos, usuario] if domain.name == dominio_usuario][0]
        
        print("\nPosibles acciones sobre el terreno '{}' :".format(dominio_usuario))
        acciones_posible = funciones_dispo[funcione_usuario]['permissions']
        for permission in acciones_posible:
            if permission in permission_domain[dominio_elije.name]['permissions']:
                print("-",permission.name)

        
        # Compruebe si el usuario tiene alguna acción posible en esta área
        if any(permission in permission_domain[dominio_elije.name]['permissions'] for permission in acciones_posible):
            while True:
                accion_usuario = input("\nQu\u00e9 quieres hacer (s para salir): ")

                # Si el usuario desea salir del bucle
                if accion_usuario == "s":
                    break

                # Comprobar si la acción existe
                if accion_usuario in [permission.name for permission in acciones_posible] :
                    # Comprobar si el usuario tiene permiso para realizar la acción solicitada
                    permission_demandee = [permission for permission in acciones_posible if permission.name == accion_usuario][0]
                    try:
                        rbac.go(sujet_utilisateur, dominio_elije, permission_demandee)
                        print("\nEsta autorizado a realizar esta acci\u00f3n en el dominio '{}'.\n".format(dominio_usuario))
                    except RBACAuthorizationError:
                        print("\nNo est\u00e1 autorizado a realizar esta accion.\n")
                else:
                    print("\nEsta acci\u00f3n no existe.\n")

        else:
            print("\nNo puedes realizar ninguna acci\u00f3n en esta zona, asi que elige otra.")

