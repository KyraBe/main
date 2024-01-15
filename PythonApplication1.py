# -*- coding: utf-8 -*-

import getpass
from rbac import RBAC, RBACAuthorizationError
import modifier_donnees
import hash_data
from datetime import datetime

rbac = RBAC()

# Creacion de roles
admin_role = rbac.create_role('Admin')
asistente_role = rbac.create_role('Asistente')
vendedor_role = rbac.create_role('Vendedor')

# Creacion de dominios
venta = rbac.create_domain('Venta')
productos = rbac.create_domain('Productos')
usuario = rbac.create_domain('Usuario')
cliente = rbac.create_domain('Cliente')

# Creacion de permisos
crear_venta_permission = rbac.create_permission('Crear venta')
modificar_venta_permission = rbac.create_permission('Modificar venta')
eliminar_venta_permission = rbac.create_permission('Eliminar venta')
listar_productos_permission = rbac.create_permission('Listar productos')
agregar_productos_permission = rbac.create_permission('Agregar productos')
desactivar_productos_permission = rbac.create_permission('Desactivar productos')
agregar_usuario_permission = rbac.create_permission('Agregar usuario')
crear_cliente_permission = rbac.create_permission('Crear cliente')
modificar_cliente_permission = rbac.create_permission('Modificar cliente')
eliminar_cliente_permission = rbac.create_permission('Eliminar cliente')

# Anadir permisos a los roles
admin_role.add_permission(crear_venta_permission, venta)
admin_role.add_permission(modificar_venta_permission, venta)
admin_role.add_permission(eliminar_venta_permission, venta)
admin_role.add_permission(listar_productos_permission, productos)
admin_role.add_permission(agregar_productos_permission, productos)
admin_role.add_permission(desactivar_productos_permission, productos)
admin_role.add_permission(agregar_usuario_permission, usuario)
admin_role.add_permission(crear_cliente_permission, cliente)
admin_role.add_permission(modificar_cliente_permission, cliente)
admin_role.add_permission(eliminar_cliente_permission, cliente)

asistente_role.add_permission(crear_venta_permission, venta)
asistente_role.add_permission(modificar_venta_permission, venta)
asistente_role.add_permission(listar_productos_permission, productos)
asistente_role.add_permission(agregar_productos_permission, productos)
asistente_role.add_permission(desactivar_productos_permission, productos)
asistente_role.add_permission(modificar_cliente_permission, cliente)
asistente_role.add_permission(eliminar_cliente_permission, cliente)

vendedor_role.add_permission(listar_productos_permission, productos)

# Creacion de usuarios y asignacion de funciones
usuario_admin = rbac.create_subject('Admin')
usuario_admin.authorize(admin_role)

usuario_asistente = rbac.create_subject('Asistente')
usuario_asistente.authorize(asistente_role)

usuario_vendedor = rbac.create_subject('Vendedor')
usuario_vendedor.authorize(vendedor_role)

utilisateur = rbac.create_subject('User')
utilisateur.authorize(admin_role)

# Creacion de acciones y funciones disponibles
acciones = {
    'Crear venta': crear_venta_permission,
    'Modificar venta': modificar_venta_permission,
    'Eliminar venta': eliminar_venta_permission,
    'Listar productos': listar_productos_permission,
    'Agregar productos': agregar_productos_permission,
    'Desactivar productos': desactivar_productos_permission,
    'Agregar usuario': agregar_usuario_permission,
    'Crear cliente': crear_cliente_permission,
    'Modificar cliente': modificar_cliente_permission,
    'Eliminar cliente': eliminar_cliente_permission
    }

funciones_dispo = {
    'Admin': {
        'permissions': [crear_venta_permission, modificar_venta_permission, eliminar_venta_permission, listar_productos_permission, agregar_productos_permission, desactivar_productos_permission, agregar_usuario_permission, crear_cliente_permission, modificar_cliente_permission, eliminar_cliente_permission]
    },
    'Asistente': {
        'permissions': [crear_venta_permission, modificar_venta_permission, listar_productos_permission, agregar_productos_permission, desactivar_productos_permission, crear_cliente_permission, modificar_cliente_permission ]
    },
    'Vendedor': {
        'permissions': [listar_productos_permission]
    }
 }

permission_domain = {
    'Venta': {'permissions' : [crear_venta_permission, modificar_venta_permission, eliminar_venta_permission]},
    'Productos': {'permissions' : [listar_productos_permission, agregar_productos_permission, desactivar_productos_permission]},
    'Usuario': {'permissions' : [agregar_usuario_permission]},
    'Cliente': {'permissions': [crear_cliente_permission, modificar_cliente_permission, eliminar_cliente_permission]}
}

# Base de datos de usuarios
usuarios = {
    "Admin": "Admin",
    "Asistente": "Asistente",
    "Vendedor": "Vendedor"
}

rbac.lock()


#######################################     Interaccion con el usuario      #####################################
print("----------------------------------------------------- Connexi\u00f3n ------------------------------------------------------")

# Bucle de conexion
while True:
    # Pedir al usuario que inicie sesion
    funcione_usuario = input("Nombre de usuario : ")
    contrasena = getpass.getpass("Contrase\u00f1a : ")
    date_heure = modifier_donnees.date_heure()
    obj = "Aplicaci\u00f3n"

    # Compruebe los detalles de su conexion
    if funcione_usuario in usuarios and usuarios[funcione_usuario] == contrasena:
        print("Conexi\u00f3n correcta. \n")
        sujet_utilisateur = None
        if funcione_usuario == "Admin":
            sujet_utilisateur = usuario_admin
        elif funcione_usuario == "Asistente":
            sujet_utilisateur = usuario_asistente
        elif funcione_usuario == "Vendedor":
            sujet_utilisateur = usuario_vendedor
        else:
            sujet_utilisateur = utilisateur

        #ajoute une ligne a Audit.txt
        nvl_ligne = "\n" + date_heure + " Conexi\u00f3n correcta " + obj + " " + funcione_usuario + "\n"
        with open('Audit.txt', 'a') as fichier:
            fichier.write(nvl_ligne)
        break
    else:
        print("\nNombre de usuario o contrase\u00f1a incorrectos. Por favor, intentelo de nuevo.\n")
        nvl_ligne = "\n" + date_heure + " Conexi\u00f3n denegada " + obj + "\n"
        with open('Audit.txt', 'a') as fichier:
            fichier.write(nvl_ligne)

print("-------------------------------------------------- Check integrity ---------------------------------------------------")
hash_data.check_integrity(funcione_usuario)

while True:
    print("\n------------------------------------------------------ Dominio -------------------------------------------------------")
    print("Dominios disponibles :")
    for index, domain in enumerate([venta, productos, usuario, cliente], start=1):
        print(f"{index}. {domain.name}")
    dominio_usuario = input("\nElija la zona en la que desea realizar la acci\u00f3n (s para salir): ")

    
    #Si l utilisateur veut quitter la boucle
    if dominio_usuario == "s":
        break

    # Verifiez si l entree est un nombre valide
    if not dominio_usuario.isdigit():
        print("\nPor favor, ingrese un n\u00famero v\u00e1lido.")
        continue

    index_dominio = int(dominio_usuario)
    
    # Verifiez si le domaine choisi par l utilisateur existe dans la liste des domaines disponibles
    if 1 <= index_dominio <= len([venta, productos, usuario, cliente]):
        # Obtenez le domaine correspondant a l indice
        dominio_elije = [domain for domain in [venta, productos, usuario, cliente]][index_dominio - 1]
        
        acciones_posible = funciones_dispo[funcione_usuario]['permissions']

        
        # Compruebe si el usuario tiene alguna accion posible en esta area
        if any(permission in permission_domain[dominio_elije.name]['permissions'] for permission in acciones_posible):
            while True:
                print("\n------------------------------------------------------- Acci\u00f3n -------------------------------------------------------")
                print("Posibles acciones sobre el terreno '{}' :".format(dominio_elije.name))
                for index, permission in enumerate(acciones_posible, start=1):
                    if permission in permission_domain[dominio_elije.name]['permissions']:
                        print(f"{index}. {permission.name}")


                accion_usuario = input("\nSeleccione el n\u00famero de la acci\u00f3n que desea realizar (s para salir): ")

                # Si el usuario desea salir del bucle
                if accion_usuario == "s":
                    break

                # Compruebe si la entrada es un numero valido
                if not accion_usuario.isdigit():
                    print("\nPor favor, ingrese un n\u00famero v\u00e1lido.")
                    continue

                # Convertir la entrada en un indice numerico
                index_usuario = int(accion_usuario)

                # Comprobar si la accion existe
                if 1 <= index_usuario <= len(acciones_posible):
                    # Comprobar si el usuario tiene permiso para realizar la accion solicitada
                    permission_demandee = acciones_posible[index_usuario - 1]
                    try:
                        rbac.go(sujet_utilisateur, dominio_elije, permission_demandee)
                        modifier_donnees.exec(permission_demandee.name, funcione_usuario)
                    except RBACAuthorizationError:
                        print("\nNo est\u00e1 autorizado a realizar esta accion.\n")
                else:
                    print("\nEsta acci\u00f3n no existe.\n")

        else:
            print("\nNo puedes realizar ninguna acci\u00f3n en esta zona, asi que elige otra.")

