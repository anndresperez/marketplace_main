# Nombre del proyecto marketplace

# Signup y Login en Forms.py
```python
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Item

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': 'Tu usuario',
            'class': 'form-control'
        }
    ))

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'password',
            'class': 'form-control'
        }
    ))

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': 'Tu Usuario',
            'class': 'form-control'
        }
    ))

    email = forms.CharField(widget=forms.EmailInput(
        attrs={
            'placeholder': 'Tu Email',
            'class': 'form-control'
        }
    ))

    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Password',
            'class': 'form-control'
        }
    ))

    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Repite Password',
            'class': 'form-control'
        }
    ))
```

# Funciones en Views.py
```python
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout

from .models import Item, Category

from .forms import SignupForm

# Create your views here.
def home(request):
    items = Item.objects.filter(is_sold=False)
    categories = Category.objects.all()

    context = {
        'items': items,
        'categories': categories
    }
    return render(request, 'store/home.html', context)

def contact(request):
    context = {
        'msg': 'Quieres otros productos contactame!'
    }

    return render(request, 'store/contact.html', context)

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]
    context={
        'item': item,
        'related_items': related_items
    }

    return render(request, 'store/item.html', context)

def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()

    context = {
        'form': form
    }

    return render(request, 'store/signup.html', context)
```

# Login, Register urls.py
```python
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import contact, detail, register

from .forms import LoginForm

urlpatterns = [
    path('contact/', contact, name='contact'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='store/login.html', authentication_form=LoginForm)),
    path('detail/<int:pk>/', detail, name='detail'),
]
```
# Templates templates/store login, signup
```html
{% extends 'store/base.html' %}

{% block title %}Login| {% endblock %}

{% block content %}

<div class="row p-4">
    <div class="col-6 bg-light p-4">
        <h4 class="mb-6 text-center">Registro</h4>
        <hr>
        <form action="." method="POST">
            {% csrf_token %}
            <div class="form-floating mb-3">
                <h6>Username:</h6>
                {{form.username}}
            </div>
            <div class="form-floating mb-3">
                <h6>Password:</h6>
                {{form.password}}
            </div>
        </form>
    </div>
    {% if form.errors or form.non_field_errors %}
    <div class="mb-4 p-6 bg-danger">
        {% for field in form %}
            fiels.errors
        {% endfor %}
        {{ form.non_field_errors }}
    </div>
    {% endif %}
</div>
<button class="btn btn-primary mb-6">Login</button>


{% endblock %}

```
```html
{% extends 'store/base.html' %}

{% block title %}Registro| {% endblock %}

{% block content %}
<div class="row p-4">
    <div class="col-6 bg-light p-4">
        <h4 class="mb-6 text-center">Registro</h4>
        <hr>
        <form action="." method="POST">
            {% csrf_token %}
            <div class="form-floating mb-3">
                <h6>Username:</h6>
                {{form.username}}
            </div>
            <div class="form-floating mb-3">
                <h6>Email:</h6>
                {{form.email}}
            </div>
            <div class="form-floating mb-3">
                <h6>Password:</h6>
                {{form.password1}}
            </div>
            <div class="form-floating mb-3">
                <h6>Repite Password:</h6>
                {{form.password2}}
            </div>

            {% if form.errors or form.non_field_errors %}
                <div class="mb-4 p-6 bg-danger">
                    {% for field in form %}
                        fields.errors
                    {% endfor %}
                    {{ form.non_field_errors }}
                </div>
            {% endif %}

            <button class="btn btn-primary mb-6">Register</button>
        </form>
    </div>
</div>
{% endblock %}
```
# Funcionalidad para que el usuario agregue articulos en la aplicacion siempre y cuando tenga acceso a la aplicacion store

# forms.py
```python
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Item


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': 'Tu usuario',
            'class': 'form-control'
        }
    ))

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'password',
            'class': 'form-control'
        }
    ))


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': 'Tu Usuario',
            'class': 'form-control'
        }
    ))

    email = forms.CharField(widget=forms.EmailInput(
        attrs={
            'placeholder': 'Tu Email',
            'class': 'form-control'
        }
    ))

    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Password',
            'class': 'form-control'
        }
    ))

    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Repite Password',
            'class': 'form-control'
        }
    ))


class NewItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('category', 'name', 'description', 'price', 'image')

        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'height: 100px'
            }),
            'price': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
            }),
        }
```
# urls.py
```python
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import contact, detail, register, logout_user, add_item

from .forms import LoginForm

urlpatterns = [
    path('contact/', contact, name='contact'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='store/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', logout_user, name='logout'),
    path('add_item/', add_item, name='add_item'),
    path('detail/<int:pk>/', detail, name='detail'),
]
```
# views.py
```python
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from .models import Item, Category

from .forms import SignupForm, NewItemForm 

# Create your views here.
def home(request):
    items = Item.objects.filter(is_sold=False)
    categories = Category.objects.all()

    context = {
        'items': items,
        'categories': categories
    }
    return render(request, 'store/home.html', context)

def contact(request):
    context = {
        'msg': 'Quieres otros productos contactame!'
    }

    return render(request, 'store/contact.html', context)

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]
    context={
        'item': item,
        'related_items': related_items
    }

    return render(request, 'store/item.html', context)

def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()

    context = {
        'form': form
    }

    return render(request, 'store/signup.html', context)

def logout_user(request):
    logout(request)

    return redirect('home')


@login_required
def add_item(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            return redirect('detail', pk=item.id)
    else:
        form = NewItemForm()

    context = {
        'form': form,
        'title': 'New Item'
    }

    return render(request, 'store/form.html', context)
```
# nav.html
```html
<nav class="navbar navbar-expand-lg bg-dark" data-bs-theme="dark">
    <div class="container-fluid">
        <a href="{% url 'home' %}" class="navbar-brand">Marketplace</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-control="navBarNav" aria-expanded="false" aria-label="Toggle Navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ms-auto">
                <li class="nav-item">
                    <a href="" class="nav-link active">
                        Home
                    </a>
                </li>
                <li class="nav-item">
                    <a href="{% url 'contact' %}" class="nav-link active">
                        Contact
                    </a>
                </li>
               
                {% if request.user.is_authenticated %}
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'add_item'%}">Add Item</a>
                    </li>
                    <li class="nav-item">
                        <a href="{% url 'logout' %}" class="nav-link active">
                            Logout
                        </a>
                    </li>
                {% else %}
                    <li class="nav-item">
                        <a href="{% url 'login' %}" class="nav-link active">
                            Login
                        </a>
                    </li>
                    <li class="nav-item">
                        <a href="{% url 'register' %}" class="nav-link active">
                            Register
                        </a>
                    </li>
                {% endif %}


            </ul>
        </div>
    </div>


</nav>
```
# form.html
```html

{% extends 'store/base.html' %}

{% block title %} {{ title }} {% endblock %}

{% block content%}
    <h4 class="mb-4 mt-4">{{ title }}</h4>
    <hr>
    <form action="." method="POST" enctype="multipart/form-data">
        {% csrf_token %}
        <div>
        
            {{ form.as_p }}
        </div>

        {% if form.errors or form.non_field_errors %}
            <div class="mb-4 p-6 bg-danger">
                {% for field in form %}
                    {{ field.errors }}
                {% endfor %}

                {{ form.non_field_errors }}
            </div>
        {% endif %}

        <button class="btn btn-primary mb-6">Register</button>
    </form>
{% endblock%}
```
# CBTIS 116
## PLANTEL VICENTE GUERRERO
# CONSTRUYE APLICACIONES WEB
### JONÁS GATICA HUERTA
### JOSE LUIS GONZALEZ LOPEZ
### HUGO RIQUELME MARTINEZ GARCIA
### SAUL GAEL MORALES MARTINEZ
### YAEL ANDRES PÉREZ ARIAS
## 5AM PG
## MAESTRO
### JOSE CHRISTIAN ROMERO HERNANDEZ
# Práctica Evaluatoria Parcial 2
### 2 DE NOVIEMBRE 2025
---
### Introducción
Django es un framework de python que nos ayuda a crear páginas y aplicaciones web de una forma más rápida y organizada. En lugar de hacer todo desde cero, Django ya trae muchas funciones listas para usar, como el manejo de usuarios, la conexión con bases de datos y un panel de administración.
Usar Django es útil porque nos permite trabajar de manera más ordenada y evitar repetir código innecesariamente. Además, es bastante seguro y lo utilizan empresas grandes como Instagram, lo cual demuestra que es una herramienta confiable.
En resumen, Django nos facilita el trabajo, nos ahorra tiempo y nos permite crear aplicaciones web completas de una forma más sencilla.

---
### Comandos
A continuación, se hará una explicación breve acerca de cada uno de los comandos de Django utilizados dentro del proyecto:
- **cd "nombre":** Sirve para entrar a una carpeta desde la terminal.
- **dir:** Muestra todo lo que hay dentro de la carpeta en la que estamos.
- **md "nombre":** Crea una nueva carpeta con el nombre que pongas.
- **cls:** Limpia la pantalla de la terminal (solo borra lo que se ve).
- **code .:** Abre la carpeta actual en Visual Studio Code.
- **Ctrl + S:** Guarda los cambios del archivo que estás editando en Visual Studio Code.
- **python "nombre_del_archivo":** Ejecuta o corre un archivo de Python.
- **python -m venv venv:** Crea un ambiente virtual llamado "venv".
- **venv\Scripts\activate:** Activa el ambiente virtual.
- **pip install django:** Descarga e instala Django.
- **pip install pillow:** Instala una librería que sirve para trabajar con imágenes.
- **pip list:** Muestra una lista de todo lo que está instalado, incluido Django.
- **django-admin startproject "nombre":** Crea un nuevo proyecto de Django.
- **python manage.py runserver:** Inicia el servidor de Django y te da un link para verlo en el navegador.
- **python manage.py migrate:** Aplica configuraciones y crea tablas necesarias en la base de datos.
- **python manage.py createsuperuser:** Crea un usuario administrador para entrar al panel de administración.
- **python manage.py startapp store:** Crea una nueva aplicación dentro del proyecto Django.
- **python manage.py makemigrations:**  Prepara los cambios en la base de datos cuando modificas los modelos.
---
### Arquitectura MVT que utiliza Django
Django está creado para seguir un patrón de arquitectura conocido como MVT (Modal-View-Template), el cual es una variación de otro patrón llamado MVC (Model-View-Controller). Este patrón que sigue Django organiza la aplicación en tres secciones interconectadas para separar las distintas fases de su interacción con una página: la lógica de datos, la lógica de negocio y la presentación visual.

El siguiente diagrama muestra cómo interactúan estas secciones:

![f1](https://raw.githubusercontent.com/anndresperez/marketplace_main/751a284784e81fd640927c4601cfc0e743e45745/XTRA/image%20(1).png)

Explicación del flujo de MVT:

1. Solicitud de usuario: Todo empieza cuando un usuario realiza una solicitud de a una URL especificada de tu aplicación Django (por ejemplo, mi_proyecto.com/store/items/)

2. Django URLs (URL Dispatcher): Django recibe esta solicitud y, gracias al archivo  urls.py del proyecto y las aplicaciones, identifica la URL solicitada. Su trabajo es redirigir  esta solicitud a Views correcta que sabe cómo manejar esa URL.

3. Vista (View - Lógica de Negocio): Views es el "cerebro" del proyecto. Es una función o clase de Python que recibe la solicitud, esta interactúa con  el modelo si necesita datos, por ejemplo, una lista de productos, la View se comunica con el Modelo para obtenerlos de la base de datos, al igual si se necesita guardar o actualizar datos también lo hace a través del Modelo.

4. Modelo (Model - Datos y Base de Datos): El Modelo es la capa que se comunica directamente con la base de datos. Define la estructura de los datos como qué campos tiene un producto, qué relaciones existen y proporciona los procesos para consultar, crear, actualizar y eliminar esos datos de forma segura. La View nunca interactúa directamente con la base de datos, siempre lo hace a través del Modelo.

5. Plantilla (Template - Presentación): La Plantilla es un archivo HTML que define cómo se verá la página web. Contiene el diseño de la página que no se mueve, pero también incluye "etiquetas" especiales de Django que permiten insertar más fácil  los datos que la View le ha dado. La Plantilla se encarga únicamente de la presentación, no de la lógica de negocio ni de la manipulación de datos.

6. Respuesta al Usuario: Finalmente, la View toma la Plantilla con los datos ya insertados y la envía de vuelta como una respuesta HTTP al Usuario, quien la ve en su navegador como una página web completa.

Models: Qué son los datos (Base de datos).
Views: Qué hacer con la solicitud y qué datos buscar/modificar (Lógica de Python).
Templates: Cómo mostrar los datos al usuario. (HTML más dinámico).

Esta separación de responsabilidades y funciones hace que las aplicaciones de Django sean organizadas, fáciles de mantener y pueden ser escalables.

---

### Archivos
A continuación se hará una explicación acerca de algunos archivos de suma importancia a la hora de trabajar con proyectos de Django:

- [ ] **SETTINGS.PY**

El archivo settings.py en un proyecto Django es prácticamente el cerebro de la aplicación, ahí es donde se configuran todas las opciones importantes para que el proyecto funcione de una buena forma. En este archivo se ponen cosas como qué base de datos se va a usar, por ejemplo, si es SQLite, PostgreSQL o MySQL, también se define donde se guardan los archivos estáticos como imágenes, CSS y JS., además, es donde se ajustan los detalles de seguridad, como la clave secreta y cómo se manejan las sesiones de los usuarios. También se indican las aplicaciones y herramientas que el proyecto va a usar, como el sistema de autenticación o el panel de administración, y si tiene que usar algún tipo de plantilla o diseño de página, otras cosas importantes como el idioma, la zona horaria y si el proyecto está en modo de desarrollo o ya en producción también se deciden ahí. Básicamente, settings.py es donde se le dice a Django cómo debe funcionar todo el proyecto.

- [ ] **URLS.PY**

El archivo urls.py en un proyecto de Django, es el que se encarga de definir las rutas de la aplicación web. Es como un mapa que conecta las URLs que el usuario ingresa en su navegador con las vistas correspondientes que generan las respuestas. Cuando un usuario hace una solicitud a una URL específica, Django consulta el archivo urls.py para ver cuál es la función o clase que debe manejar esa solicitud. Es un mecanismo que permite organizar y estructurar las diferentes páginas o endpoints de una aplicación web. Por ejemplo, si tienes una vista que muestra una página de inicio, en urls.py se especifica la ruta como inicio, home, etc y se asocia con una vista que devolverá la respuesta al usuario, como una página HTML. Además, puede agrupar las rutas en diferentes archivos urls.py (por ejemplo, uno por cada aplicación dentro de un proyecto), lo que facilita la organización y el mantenimiento del código.

- [ ] **VIEWS.PY**

En un proyecto Django, el archivo views.py cumple la función de controlar la
lógica que se ejecuta cuando un usuario realiza una solicitud a la aplicación web.
Es el intermediario entre lo que el usuario pide (por ejemplo, al ingresar a una
URL) y lo que el sistema responde (como mostrar una página o enviar datos).
Dentro de este archivo se definen las vistas, que son funciones o clases que
procesan la información necesaria, como consultar la base de datos, validar
formularios o aplicar reglas de negocio, y luego devuelven una respuesta
adecuada, normalmente en forma de una plantilla HTML renderizada. Las vistas se conectan con las URLs definidas en urls.py, y pueden interactuar con los modelos para acceder a los datos y con las plantillas para mostrar contenido visual.

- [ ] **MODELS.PY**

En un proyecto de Django, el archivo models.py es donde se definen los modelos, que básicamente son las clases que representan las tablas de la base de datos. Su funcionamiento es el siguiente:
1- Primero, cada clase dentro de models.py se convierte en una tabla de la base de datos.
2- Posteriormente, cada atributo de esa clase se convierte en una columna.
3- Y por último, Django se encarga de traducir esas clases a código SQL para
crear y manejar la base de datos.
Este archivo es de suma importancia porque los modelos son la forma en la que Django conecta el código con los datos. Básicamente, gracias a models.py se puede trabajar con la base de datos sin escribir consultas SQL directamente porque solo usas Python.

- [ ] **TEMPLATES/STORE**

En un proyecto Django, la carpeta templates/store cumple la función de almacenar las páginas HTML que se mostrarán al usuario. Estas plantillas son la parte visual de la aplicación, es decir, lo que el usuario ve cuando entra al sitio web.
Esta carpeta se utiliza para organizar las plantillas que pertenecen específicamente a la aplicación store, evitando confusiones con plantillas de otras aplicaciones. Dentro de este folder se guardan los archivos .html que serán llamados desde las vistas (views) para mostrar contenido en pantalla.
Las plantillas que están en templates/store pueden incluir elementos como texto, imágenes, botones, tablas o diseños completos. Además, pueden recibir datos enviados desde las vistas, lo que permite mostrar información dinámica, como productos, usuarios o mensajes.

---

### - URLS
```python
from django.urls import path


from .views import contact, detail


urlpatterns = [
    path('contact/', contact, name='contact' ),
    path('detail/<int:pk>/', detail, name='detail'),
]

```
### - SETTINGS
```python
Django settings for marketplace_main project.


Generated by 'django-admin startproject' using Django 5.2.7.


For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/


For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.2/ref/settings/
"""


from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent




# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-jkt$q-_q&#^(xvz**z*ummfb_d*w7_fb!t&wuo@4=zbirr1=r_'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = []




# Application definition


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
   
    'store',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'marketplace_main.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'marketplace_main.wsgi.application'




# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}




# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]




# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/


LANGUAGE_CODE = 'en-us'


TIME_ZONE = 'UTC'


USE_I18N = True


USE_TZ = True




# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/


STATIC_URL = 'static/'
MEDIA_URL='media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



```
### - MODELS
```python
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class category(models.Model):
    name = models.CharField(max_length=225)


    class Meta:
        ordering = ('name', )
        verbose_name_plural = 'categories'


    def __str__(self):
        return self.name
   
class item(models.Model):
    category = models.ForeignKey(category, related_name="items", on_delete=models.CASCADE)
    name = models.CharField(max_length=225)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    image = models.ImageField(upload_to="item_images", blank=True, null=True)
    is_sold = models.BooleanField(default=False)
    created_by = models.ForeignKey(User,related_name='items', on_delete = models.CASCADE)
    created_at =models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name

```
### - VIEWS
```python
from django.shortcuts import render
from .models import item, category
from django.shortcuts import get_object_or_404




# Create your views here.
def home(request):
    items = item.objects.filter(is_sold=False)
    categories=category.objects.all()




    context = {
        'items':items,
        'categories': categories
    }
    return render(request, 'store/home.html', context)


def contact(request):
    content = {
        'msg': 'Quieres otros productos contactame'
    }


    return render(request, 'store/contact.html', content)


def detail(request, pk):
    item_instance = get_object_or_404(item, pk=pk)


    related_items = item.objects.filter(
        category=item_instance.category,
        is_sold=False
    ).exclude(pk=pk)[:3]
    context = {
        'item': item_instance,
        'related_items': related_items
    }
    return render(request, 'store/item.html', context)

```

### TEMPLATES/STORE
### - BASE.HTML
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!--Bootstrap-->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js" integrity="sha384-FKyoEForCGlyvwx9Hj09JcYn3nv7wiPVlz7YYwJrWVcXK/BmnVDxM+D2scQbITxI" crossorigin="anonymous"></script>
    <title>{% block title %} {% endblock %} Market Place</title>
</head>
<body>
    {% include 'store/navigation.html' %}
    <section class ="container">
        {% block content %}


        {% endblock %}
    </section>


    <footer class="py-5 text-center text-body-secondary bg-body-tertiary">
        <p>Copyright (c) 2025 - marketplace by Morales Martinez Saul Gael</p>
    </footer>
</body>
</html>

```
### - CONTACT
```html
{% extends 'store/base.html' %}


{% block title %}Contact {% endblock %}


{% block content %}
<style>
    /* Fondo animado */
    @keyframes gradientBG {
      0% { background-position: 0% 50%; }
      50% { background-position: 100% 50%; }
      100% { background-position: 0% 50%; }
    }
 
    .contact-section {
      background: linear-gradient(135deg, #0d6efd, #6f42c1, #d63384);
      background-size: 400% 400%;
      animation: gradientBG 15s ease infinite;
      color: #fff;
      border-radius: 20px;
      padding: 60px 30px;
      margin: 60px 0; /* 🔹 evita que toque header o footer */
      box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
 
    .contact-card {
      background: rgba(255, 255, 255, 0.15);
      backdrop-filter: blur(15px);
      border-radius: 20px;
      overflow: hidden;
      box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    }
 
    .form-control {
      background: rgba(255, 255, 255, 0.2);
      border: none;
      color: #fff;
      border-radius: 10px;
    }
 
    .form-control::placeholder {
      color: rgba(255, 255, 255, 0.7);
    }
 
    .form-control:focus {
      background: rgba(255, 255, 255, 0.3);
      box-shadow: 0 0 0 0.25rem rgba(255,255,255,0.3);
    }
 
    .btn-custom {
      background: linear-gradient(135deg, #ff512f, #dd2476);
      border: none;
      color: #fff;
      border-radius: 50px;
      padding: 0.75rem;
      font-weight: 600;
      transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
 
    .btn-custom:hover {
      transform: scale(1.05);
      box-shadow: 0 0 15px rgba(255,255,255,0.5);
    }
 
    .social-icons a {
      color: #fff;
      font-size: 1.5rem;
      margin: 0 10px;
      transition: transform 0.3s, color 0.3s;
    }
 
    .social-icons a:hover {
      transform: scale(1.2);
      color: #ffd700;
    }
  </style>
 
  <div class="contact-section">
    <div class="container">
      <div class="contact-card p-4">
        <div class="row align-items-center">
          <div class="col-md-5 text-center mb-4 mb-md-0">
            <h2 class="fw-bold"><i class="bi bi-chat-dots-fill"></i> ¡Contáctanos!</h2>
            <p class="text-light opacity-75">
              ¿Tienes dudas, ideas o propuestas?  
              ¡Nos encantaría escucharte! 💬
            </p>
            <div class="social-icons mt-4">
              <a href="#"><i class="bi bi-instagram"></i></a>
              <a href="#"><i class="bi bi-twitter-x"></i></a>
              <a href="#"><i class="bi bi-linkedin"></i></a>
              <a href="#"><i class="bi bi-github"></i></a>
            </div>
          </div>
 
          <div class="col-md-7">
            <form>
              <div class="mb-3">
                <label class="form-label text-white-50">Nombre</label>
                <input type="text" class="form-control" placeholder="Tu nombre completo">
              </div>
              <div class="mb-3">
                <label class="form-label text-white-50">Correo electrónico</label>
                <input type="email" class="form-control" placeholder="tucorreo@ejemplo.com">
              </div>
              <div class="mb-3">
                <label class="form-label text-white-50">Asunto</label>
                <input type="text" class="form-control" placeholder="Motivo del mensaje">
              </div>
              <div class="mb-3">
                <label class="form-label text-white-50">Mensaje</label>
                <textarea class="form-control" rows="4" placeholder="Escribe tu mensaje aquí..."></textarea>
              </div>
              <button type="submit" class="btn btn-custom w-100">
                <i class="bi bi-send-fill me-2"></i>Enviar mensaje
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>




{% endblock %}



```
### - HOME
```html
{% extends 'store/base.html' %}


{% block title %}Home | {% endblock %}


{% block content %}
    <div class="mt-2 mb-4 px-4 py-2">
        <h1 class="text-center mb-4">Nuevos Productos</h1>
        <div class="container text-center">
            <div class="row justify-content-center">
                {% for item in items %}
                    <div class="col-xs-12 col-sm-6 col-lg-4 col-xl-3 mb-4">
                        <div class="card" style="width: 18rem;">
                            <img src="{{ item.image.url }}" alt="{{ item.name }}" class="card-img-top">
                            <div class="card-body">
                                <h5 class="card-title">{{ item.name }} - {{ item.price }}</h5>
                                <p class="card-text">{{ item.description }}</p>
                            </div>
                        </div>
                    </div>
                {% endfor %}
            </div>
        </div>
    </div>
{% endblock %}

```
### - ITEM
```html
{% extends 'store/base.html' %}


{% block title %}{{item.name}} | {% endblock %}


{% block content %}
<h1>item detail Page</h1>
{% endblock %}

```
### - NAVIGATION
```html
<nav class="navbar navbar-expand-lg bg-dark" data-bs-theme="dark">
    <div class="container-fluid">
        <a href="{% url 'home' %}" class="navbar-brand">Marketplace</a>
        <button class="navbar-toggle" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-control="navBarNav" aria-expanded="false" aria-label="Toggle Navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collage navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ms-auto">
                <li class="nav-item">
                    <a href="{% url 'home' %}" class="nav-link active">
                        Home
                    </a>
                </li>
                <li class="nav-item">
                    <a href="{% url 'contact' %}" class="nav-link active">
                        Contact
                    </a>
                </li>
                <li class="nav-item">
                    <a href="" class="nav-link active">
                        Login
                    </a>
                </li>
            </ul>
        </div>
    </div>


</nav>

```

---

### Ejecución del proyecto
![x1](https://github.com/anndresperez/marketplace_main/blob/main/XTRA/x1.png?raw=true)
![x2](https://github.com/anndresperez/marketplace_main/blob/main/XTRA/x2.png?raw=true)
![x3](https://github.com/anndresperez/marketplace_main/blob/main/XTRA/x3.png?raw=true)
![x4](https://github.com/anndresperez/marketplace_main/blob/main/XTRA/x4.png?raw=true)
![x5](https://github.com/anndresperez/marketplace_main/blob/main/XTRA/x5.png?raw=true)
![x6](https://github.com/anndresperez/marketplace_main/blob/main/XTRA/x6.png?raw=true)
![x7](https://github.com/anndresperez/marketplace_main/blob/main/XTRA/x7.png?raw=true)

---

### Actualizaciones
A continuación se hará una explicación acerca de las actualizaciones realizadas al proyecto de marketplace _main:

- [ ] **Forms.py (LoginForm, SignupForm, NewItemForm)**

El LoginForm contiene campos como username y password. Se usa para autenticar al usuario, asegurándose de que las credenciales sean correctas. Los campos son simples y el formulario valida que coincidan con los datos guardados en la base de datos. El SignupForm incluye username, email, password y confirm_password. Permite registrar a un nuevo usuario: primero valida que los campos no estén vacíos, luego comprueba que las contraseñas coincidan y finalmente crea el usuario en la base de datos si todo es correcto. El NewItemForm tiene campos como name, description, price e image. Se utiliza para agregar nuevos ítems a la base de datos; al enviarlo, los datos se guardan y se muestran en la aplicación. Además, facilita que la información ingresada cumpla con las reglas de la aplicación antes de almacenarla.

- [ ] **Views.py (login(), logout_user(), detail(), add_item())**

Las funciones login(), logout_user(), detail() y add_item() controlan cómo responde la aplicación a distintas acciones. login() verifica las credenciales y, si son correctas, inicia la sesión; si no, muestra un error. 
logout_user() cierra la sesión y redirige al inicio o login. 
detail() muestra la información de un ítem específico, usando su ID para obtenerlo de la base de datos y enviarla al template. add_item() permite crear un nuevo ítem: muestra el formulario si es GET y guarda los datos si es POST.
Estas funciones coordinan la interacción del usuario con la aplicación, validan los datos y aseguran que la información se muestre correctamente en la interfaz. También permiten controlar qué usuarios pueden acceder a ciertas acciones según su estado de sesión.

- [ ] **Decorador @login_required**

El decorador @login_required se usa para restringir el acceso a una vista únicamente a usuarios que hayan iniciado sesión. Cuando una función en views.py tiene este decorador, cualquier usuario no autenticado que intente acceder a esa vista será automáticamente redirigido a la página de login;es decir, @login_required obliga a que la vista sólo pueda ejecutarse si el usuario está autenticado; si no, lo manda a iniciar sesión antes de continuar.

- [ ] **Urls.py (Las rutas a cada acción nueva en views)**

En urls.py, las rutas funcionan como enlaces que conectan una URL específica con una función dentro de views.py. Cada vez que agregas una acción nueva en views (como login(), logout_user(), detail(), add_item()), debes crear una ruta que indique qué URL activa esa función. En otras palabras, las rutas en urls.py definen qué dirección del navegador corresponde a cada acción del sistema. Cuando el usuario visita una URL, Django revisa este archivo y ejecuta la función de views asociada.

- [ ] **Store/Templates (item.html, login.html, signup.html, navigation.html, form.html)**

Las plantillas en Store/Templates muestran la información al usuario y reciben datos desde las vistas. 
item.html muestra los detalles de un ítem (nombre, descripción, imagen, precio, etc.). 
login.html y signup.html muestran los formularios de inicio de sesión y registro, con validaciones y mensajes de error. 
navigation.html contiene la barra de navegación con enlaces según el estado del usuario.
form.html es una plantilla reutilizable para mostrar formularios de manera ordenada. En conjunto, estas plantillas organizan la interfaz y permiten al usuario interactuar con la aplicación.

---

### - FORMS.PY
```python
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


from .models import Item




class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': 'Tu usuario',
            'class': 'form-control'
        }
    ))


    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'password',
            'class': 'form-control'
        }
    ))




class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': 'Tu Usuario',
            'class': 'form-control'
        }
    ))


    email = forms.CharField(widget=forms.EmailInput(
        attrs={
            'placeholder': 'Tu Email',
            'class': 'form-control'
        }
    ))


    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Password',
            'class': 'form-control'
        }
    ))


    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Repite Password',
            'class': 'form-control'
        }
    ))




class NewItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('category', 'name', 'description', 'price', 'image')


        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'height: 100px'
            }),
            'price': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
            }),
        }

```
### - VIEWS.PY
```python
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


from .models import Item, Category


from .forms import SignupForm, NewItemForm


# Create your views here.
def home(request):
    items = Item.objects.filter(is_sold=False)
    categories = Category.objects.all()


    context = {
        'items': items,
        'categories': categories
    }
    return render(request, 'store/home.html', context)


def contact(request):
    context = {
        'msg': 'Quieres otros productos contactame!'
    }


    return render(request, 'store/contact.html', context)


def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]
    context={
        'item': item,
        'related_items': related_items
    }


    return render(request, 'store/item.html', context)


def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)


        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()


    context = {
        'form': form
    }


    return render(request, 'store/signup.html', context)


def logout_user(request):
    logout(request)


    return redirect('home')



```
### - DECORADOR
```python
@login_required
def add_item(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)


        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            return redirect('detail', pk=item.id)
    else:
        form = NewItemForm()


    context = {
        'form': form,
        'title': 'New Item'
    }


    return render(request, 'store/form.html', context)

```
### - URLS.PY
```python
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import contact, detail, register, logout_user, add_item


from .forms import LoginForm


urlpatterns = [
    path('contact/', contact, name='contact'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='store/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', logout_user, name='logout'),
    path('add_item/', add_item, name='add_item'),
    path('detail/<int:pk>/', detail, name='detail'),
]

```
### TEMPLATES/STORE
### - ITEM.HTML
```html
{% extends 'store/base.html' %}


{% block title %}{{item.name}} | {% endblock %}


{% block content %}
<div class="container mt-4 mb-4">
    <div class="row">
        <div class="col-4">
            <img src="{{ item.image.url }}" alt=""
            class="rounded" width="100%">
        </div>
        <div class="col-8 p-4 rounded bg-light">
            <h1 class="mb-4 text-center">
                {{ item.name }}
            </h1>
            <hr>
            <h4><strong>Precio ${{ item.price }}</strong></h4>
            <h4><strong>Vendedor {{ item.created_by.username }}</strong></h4>
           
            {% if item.description %}
                <p>{{ item.description }}</p>
            {% endif %}


            <a href="" class="btn btn-dark">Contacta a el vendedor</a>
           
        </div>
    </div>
</div>
{% endblock %}

```
### - LOGIN.HTML
```html
{% extends 'store/base.html' %}


{% block title %}Login| {% endblock %}


{% block content %}


<div class="row p-4 d-flex justify-content-center align-items-center">
    <div class="col-6 bg-light p-4">
        <h4 class="mb-6 text-center">Registro</h4>
        <hr>
        <form action="." method="POST">
            {% csrf_token %}
            <div class="form-floating mb-3">
                <h6>Username:</h6>
                {{form.username}}
            </div>
            <div class="form-floating mb-3">
                <h6>Password:</h6>
                {{form.password}}
            </div>




            {% if form.errors or form.non_field_errors %}
            <div class="mb-4 p-6 bg-danger text-white rounded">
                {% for field in form %}
                field.errors
                {% endfor %}
                {{ form.non_field_errors }}
            </div>
            {% endif %}
            <div class="d-flex justify-content-center align-items-center">
                <button class="btn btn-primary mb-6">Login</button>
            </div>
            <div class="d-flex justify-content-center align-items-center">
                <a href="{% url 'register' %}">¿No tienes cuenta? registrate aqui!</a>
            </div>
        </form>
    </div>
</div>






{% endblock %}

```
### - SIGNUP.HTML
```html
{% extends 'store/base.html' %}


{% block title %}Registro| {% endblock %}


{% block content %}
<div class="row p-4 d-flex justify-content-center align-items-center">
    <div class="col-6 bg-light p-4">
        <h4 class="mb-6 text-center">Registro</h4>
        <hr>
        <form action="." method="POST">
            {% csrf_token %}
            <div class="form-floating mb-3">
                <h6>Username:</h6>
                {{form.username}}
            </div>
            <div class="form-floating mb-3">
                <h6>Email:</h6>
                {{form.email}}
            </div>
            <div class="form-floating mb-3">
                <h6>Password:</h6>
                {{form.password1}}
            </div>
            <div class="form-floating mb-3">
                <h6>Repite Password:</h6>
                {{form.password2}}
            </div>


            {% if form.errors or form.non_field_errors %}
                <div class="mb-4 p-6 bg-danger rounded">
                    {% for field in form %}
                        <h5 class="text-white">
                            {{field.errors}}
                        </h5>
                       
                    {% endfor %}
                    {{ form.non_field_errors }}
                </div>
            {% endif %}


            <div class="d-flex justify-content-center align-items-center">
                <button class="btn btn-primary mb-6">Register</button>
            </div>
            <div class="d-flex justify-content-center align-items-center">
                <a href="{% url 'login' %}">¿Ya tienes cuenta? Accesa aqui!</a>
            </div>
        </form>
    </div>
</div>
{% endblock %}

```
### - NAVIGATION.HTML
```html
<nav class="navbar navbar-expand-lg bg-dark" data-bs-theme="dark">
    <div class="container-fluid">
        <a href="{% url 'home' %}" class="navbar-brand">Marketplace</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-control="navBarNav" aria-expanded="false" aria-label="Toggle Navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ms-auto">
                <li class="nav-item">
                    <a href="" class="nav-link active">
                        Home
                    </a>
                </li>
                <li class="nav-item">
                    <a href="{% url 'contact' %}" class="nav-link active">
                        Contact
                    </a>
                </li>
               
                {% if request.user.is_authenticated %}
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'add_item'%}">Add Item</a>
                    </li>
                    <li class="nav-item">
                        <a href="{% url 'logout' %}" class="nav-link active">
                            Logout
                        </a>
                    </li>
                {% else %}
                    <li class="nav-item">
                        <a href="{% url 'login' %}" class="nav-link active">
                            Login
                        </a>
                    </li>
                    <li class="nav-item">
                        <a href="{% url 'register' %}" class="nav-link active">
                            Register
                        </a>
                    </li>
                {% endif %}




            </ul>
        </div>
    </div>




</nav>



```
### - FORM.HTML
```html
{% extends 'store/base.html' %}


{% block title %} {{ title }} {% endblock %}


{% block content%}
    <h4 class="mb-4 mt-4">{{ title }}</h4>
    <hr>
    <form action="." method="POST" enctype="multipart/form-data">
        {% csrf_token %}
        <div>
       
            {{ form.as_p }}
        </div>


        {% if form.errors or form.non_field_errors %}
            <div class="mb-4 p-6 bg-danger">
                {% for field in form %}
                    {{ field.errors }}
                {% endfor %}


                {{ form.non_field_errors }}
            </div>
        {% endif %}


        <button class="btn btn-primary mb-6">Register</button>
    </form>
{% endblock%}

```

---

### Ejecución del proyecto
![y1](https://github.com/anndresperez/marketplace_main/blob/main/XTRA/y1.png?raw=true)
![y2](https://github.com/anndresperez/marketplace_main/blob/main/XTRA/y2.png?raw=true)
![y3](https://github.com/anndresperez/marketplace_main/blob/main/XTRA/y3.png?raw=true)
![y4](https://github.com/anndresperez/marketplace_main/blob/main/XTRA/y4.png?raw=true)
![y5](https://github.com/anndresperez/marketplace_main/blob/main/XTRA/y5.png?raw=true)
![y6](https://github.com/anndresperez/marketplace_main/blob/main/XTRA/y6.png?raw=true)
![y7](https://github.com/anndresperez/marketplace_main/blob/main/XTRA/y7.png?raw=true)

---

### Conclusión
Luego de haber realizado este proyecto creo que nos quedamos muy satisfechos con todo lo que logramos ver en este parcial, logramos aprender diversas cosas acerca de la creacion de paginas y el funcionamiento de estas, logramos aprender bastante de el cmd y de los comandos que este nos permite utilizar, de igual manera herramientas como el django o el pillow nos sorprendieron como podían realizar cambios en nuestra terminal.
El cambio de el parcial anterior a este fue bastante marcado, ya que a pesar de que las clases no tuvieron una gran dificultad si fue una experiencia más activa en comparación con el parcial pasado, lo cual fuera de ser algo frustrante nos permitió desarrollar mejor nuestras habilidades y hacernos cuestionarnos si anteriormente contábamos con las habilidades o con los conocimientos suficientes, por eso fue que la experiencia de este nuevo curso fue algo bastante refrescante y divertido, contando con un avance bastante continuo pero que de igual forma bastante divertido de seguir.

Para finalizar queremos agradecer al docente por permitirnos ser parte del curso y brindarnos la guía suficiente para llevar a cabo el proyecto y las prácticas correspondientes de igual forma reconocer el propio renacimiento del equipo y seguir preparándonos para los futuros obstáculos a superar.


---





