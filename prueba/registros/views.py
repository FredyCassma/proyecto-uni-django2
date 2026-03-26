from django.shortcuts import render
from .models import Alumnos, ComentarioContacto, Archivos
from .forms import ComentarioContactoForm,FormArchivos
from django.shortcuts import get_object_or_404
import datetime
from django.contrib import messages

def principal(request):  # ← cambiado a 'principal' para que coincida con urls.py
    alumnos = Alumnos.objects.all()  # ← indentación correcta
    return render(request, "registros/principal.html", {'alumnos': alumnos})
    # ← corregido: 'registros' (sin typo) y se pasa la variable alumnos

def registrar(request):
    if request.method == 'POST':
        form = ComentarioContactoForm(request.POST)
        if form.is_valid(): #Si los datos recibidos son correctos
            form.save() #Inserta
            comentarios = ComentarioContacto.objects.all()
            return render(request,"registros/comentarios.html",{'comentarios': comentarios})
    form = ComentarioContactoForm()
    #Si algo sale mal se reenvian al formulario los datos ingresados
    return render(request,'registros/contacto.html',{'form':form})

def contacto(request):
    return render(request,"registros/contacto.html")
    #Indicamos el lugar del render del resultado de la vista

def consulta(request):
    comentarios = ComentarioContacto.objects.all()
    return render(request, "registros/comentarios.html",{'comentarios':comentarios})

def consultar1(request):
    #con una sola condicion 
    alumnos=Alumnos.objects.filter(carrera="TI")
    return render(request, "registros/consultas.html",{'alumnos':alumnos})

def consultar2(request):
    #con una sola condicion 
    alumnos=Alumnos.objects.filter(carrera="TI").filter(turno="Matutino")
    return render(request, "registros/consultas.html",{'alumnos':alumnos})

def consultar3(request):
    #con una sola condicion 
    alumnos=Alumnos.objects.all().only("matricula", "nombre", "carrera", "turno", "imagen") #solo muestra estos campos
    return render(request, "registros/consultas.html",{'alumnos':alumnos})

def consultar4(request):
    #con una sola condicion 
    alumnos=Alumnos.objects.filter(turno__contains="Vesp")
    return render(request, "registros/consultas.html",{'alumnos':alumnos})

def consultar5(request):
    #con una sola condicion 
    alumnos=Alumnos.objects.filter(nombre__in=["Juan", "Ana"])
    return render(request, "registros/consultas.html",{'alumnos':alumnos})

def consultar6(request):
    fechaInicio=datetime.date(2026, 2, 1)
    fechaFin=datetime.date(2026, 3, 29)
    alumnos=Alumnos.objects.filter(creacion__range=(fechaInicio, fechaFin))
    return render(request, "registros/consultas.html",{'alumnos':alumnos})

def consultar7(request):
    #consultando entre modelos relacionados
    alumnos=Alumnos.objects.filter(comentario__coment__icontains="Holaaa")
    return render(request, "registros/consultas.html",{'alumnos':alumnos})

def eliminarComentarioContacto(request, id,
    confirmacion = 'registros/confirmarEliminacion.html'):
    comentario = get_object_or_404(ComentarioContacto, id=id)
    if request.method=='POST':
        comentario.delete()
        comentarios=ComentarioContacto.objects.all()
        return render(request,"registros/comentarios.html",
                {'comentarios':comentarios})
    return render(request,confirmacion,{'object':comentario})

def ConsultarComentarioIndividual(request, id):
    comentario=ComentarioContacto.objects.get(id=id)
    #get permite establecer un condicional a la consulta y recuperar objetos
    #del modelo que cumplen dichas condiciones
    #get se emplea cuando se sabe que solo hay un objeto que coincide con su consulta
    return render(request, "registros/formEditarComentario.html", 
                  {'comentario':comentario})
    #indicamos el lugar de la vista y enviamos la tabla de comentarios recuperados 

def editarComentarioContacto(request, id): 
    comentario = get_object_or_404(ComentarioContacto, id=id)
    form = ComentarioContactoForm(request.POST, instance=comentario)
    #Referenciamos que el elemento del formulario pertenece al comentario ya existente
    if form.is_valid():
        form.save()
        comentarios=ComentarioContacto.objects.all()
        return render(request,"registros/comentarios.html",
            {'comentarios': comentarios})
    return render(request, "registros/formEditarComentario.html",
                  {'comentario':comentario})

def archivos(request):
    if request.method == 'POST':
        form = FormArchivos(request.POST, request.FILES)
        if form.is_valid():
            titulo = request.POST['titulo']
            descripcion = request.POST['descripcion']
            archivo = request.FILES['archivo']
            insert = Archivos(titulo=titulo, descripcion= descripcion, archivo= archivo)
            insert.save()
            return render(request,"registros/archivos.html")
        else:
                messages.error(request,"Error al procesar el formulario")
    else:
        return render(request,"registros/archivos.html",{'archivo':Archivos})

def subirArchivos(request):
     return render(request,"registros/archivos.html")

def consultasSQL(request):
    alumnos=Alumnos.objects.raw('SELECT id, matricula, nombre, carrera,' \
    'turno, imagen FROM registros_alumnos WHERE carrera="TI" ORDER BY ' \
    'turno DESC')

    return render(request,"registros/consultas.html",
                {'alumnos': alumnos})