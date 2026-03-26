from django.contrib import admin
from.models import Alumnos, Comentario, ComentarioContacto

# Register your models here.

class AdministrarModelo(admin.ModelAdmin):
    readonly_fields = ('creacion', 'actualizacion')
    list_display = ('matricula', 'nombre', 'carrera','turno')
    search_fields = ('matricula','nombre','carrera','turno')
    date_hierarchy = 'creacion'
    list_filter = ('carrera','turno')

    def get_readonly_fields(self, request, obj = None):
        if request.user.groups.filter(name="Usuarios").exists():
            return ('matricula','carrera','turno')
        else:
            return ('creacion','actualizacion')
    
    def get_readonly_fields(self, request, obj = None):
        #si el usuario pertenece al grupo de permisos "usuarios"
        if request.user.groups.filter(name="Usuarios2").exists():
            return ('matricula', 'turno') #todos los campos de solo lectura
        else:
            return ('creacion', 'actualizacion') #solo los campos de fecha de creación y actualización son de solo lectura
        
admin.site.register(Alumnos, AdministrarModelo)

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('id','alumno','coment','created')
    search_fields = ('alumno__nombre','coment')
    list_filter = ('alumno','created')
    date_hierarchy = 'created'
    readonly_fields = ('created',)

class AdministrarComentariosContacto(admin.ModelAdmin):
    list_display = ('id','mensaje')
    search_fields = ('id', 'created')
    date_hierarchy = 'created'
    readonly_fields = ('created','id')

admin.site.register(ComentarioContacto, AdministrarComentariosContacto)