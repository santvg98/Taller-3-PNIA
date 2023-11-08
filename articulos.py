'''
Clase que se encargará de facilitar la gestión de los artículos
'''

from datetime import datetime
import os

class Articulos:
    def __init__(self, programa,mysql):
        self.programa = programa
        self.mysql = mysql
        self.conexion = self.mysql.connect()
        self.cursor = self.conexion.cursor()

    def consultar(self):
        sql = "SELECT * FROM articulos WHERE activo=1"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conexion.commit()
        return resultado

    def agregar(self, articulo):
        sql = f"INSERT INTO articulos (id,nombre,precio,saldo,foto,activo)\
            VALUES ('{articulo[0]}','{articulo[1]}',{articulo[2]},{articulo[3]},\
            '{articulo[4]}',1)"
        self.cursor.execute(sql)
        self.conexion.commit()
    
    def modificar(self, articulo):
        sql = f"UPDATE articulos SET nombre='{articulo[1]}',\
            precio={articulo[2]},saldo={articulo[3]} WHERE id='{articulo[0]}'"
        self.cursor.execute(sql)
        self.conexion.commit()
        if articulo[4].filename != '':
            sql=f"SELECT foto FROM articulos WHERE id='{articulo[0]}'"
            self.cursor.execute(sql)
            resultado=self.cursor.fetchall()
            self.conexion.commit()
            os.remove(os.path.join(self.programa.config['CARPETAUP'],resultado[0][0]))
            ahora = datetime.now()
            tiempo = ahora.strftime("%Y%m%d%H%M%S")
            nom,ext = os.path.splitext(articulo[4].filename)
            nombreFoto = "A"+tiempo+ext
            articulo[4].save("uploads/"+nombreFoto)
            sql=f"UPDATE articulos SET foto='{nombreFoto}'"
            self.cursor.execute(sql)
            self.conexion.commit()

    def borrar(self, id):
        sql = f"UPDATE articulos SET activo=0 WHERE id={id}"
        self.cursor.execute(sql)
        self.conexion.commit()
    
    def buscar(self,id):
        sql = f"SELECT * FROM articulos WHERE id={id}"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conexion.commit()
        return resultado
'''
        if len(resultado)>0:
            return True
        else:
            return False
'''