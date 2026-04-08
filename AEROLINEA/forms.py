from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Aeropuerto, Pasajero
from datetime import date


class RegistroForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, label='Nombre(s)')
    last_name = forms.CharField(max_length=100, label='Apellidos')
    email = forms.EmailField(label='Correo electrónico')
    telefono = forms.CharField(max_length=20, label='Teléfono', required=False)
    fecha_nacimiento = forms.DateField(
        label='Fecha de nacimiento',
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )

    class Meta:
        model = Usuario
        fields = ('username', 'first_name', 'last_name', 'email',
                  'telefono', 'fecha_nacimiento', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.telefono = self.cleaned_data.get('telefono', '')
        user.fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')
        user.rol = 'cliente'
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(label='Usuario o correo')
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')


class BusquedaVueloForm(forms.Form):
    TIPO_VIAJE_CHOICES = [('ida', 'Solo ida'), ('redondo', 'Vuelo redondo')]

    origen = forms.ModelChoiceField(
        queryset=Aeropuerto.objects.all(),
        label='Origen',
        empty_label='¿Desde dónde vuelas?'
    )
    destino = forms.ModelChoiceField(
        queryset=Aeropuerto.objects.all(),
        label='Destino',
        empty_label='¿A dónde vas?'
    )
    fecha_salida = forms.DateField(
        label='Fecha de salida',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    fecha_regreso = forms.DateField(
        label='Fecha de regreso',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    num_pasajeros = forms.IntegerField(
        label='Pasajeros',
        min_value=1,
        max_value=200,
        initial=1
    )
    tipo_viaje = forms.ChoiceField(
        choices=TIPO_VIAJE_CHOICES,
        label='Tipo de viaje',
        widget=forms.RadioSelect
    )

    def clean(self):
        cleaned = super().clean()
        origen = cleaned.get('origen')
        destino = cleaned.get('destino')
        fecha_salida = cleaned.get('fecha_salida')
        fecha_regreso = cleaned.get('fecha_regreso')
        tipo_viaje = cleaned.get('tipo_viaje')

        if origen and destino and origen == destino:
            raise forms.ValidationError('El origen y destino no pueden ser iguales.')

        if fecha_salida and fecha_salida < date.today():
            raise forms.ValidationError('La fecha de salida no puede ser en el pasado.')

        if tipo_viaje == 'redondo' and not fecha_regreso:
            raise forms.ValidationError('Debes seleccionar una fecha de regreso para vuelo redondo.')

        if fecha_salida and fecha_regreso and fecha_regreso <= fecha_salida:
            raise forms.ValidationError('La fecha de regreso debe ser posterior a la de salida.')

        return cleaned


class PasajeroForm(forms.Form):
    TIPO_CHOICES = [
        ('adulto', 'Adulto'),
        ('menor', 'Menor de edad'),
        ('tercera_edad', 'Tercera edad'),
        ('discapacidad', 'Persona con discapacidad'),
    ]
    nombre = forms.CharField(max_length=100, label='Nombre(s)')
    apellido_paterno = forms.CharField(max_length=100, label='Apellido paterno')
    apellido_materno = forms.CharField(max_length=100, label='Apellido materno', required=False)
    fecha_nacimiento = forms.DateField(
        label='Fecha de nacimiento',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    tipo = forms.ChoiceField(choices=TIPO_CHOICES, label='Tipo de pasajero')
    nacionalidad = forms.CharField(max_length=60, label='Nacionalidad', initial='Mexicana')
    necesidades_especiales = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2}),
        label='Necesidades especiales / condiciones',
        required=False
    )


class PagoForm(forms.Form):
    METODO_CHOICES = [
        ('tarjeta', 'Tarjeta de crédito / débito'),
        ('paypal', 'PayPal'),
    ]
    metodo = forms.ChoiceField(
        choices=METODO_CHOICES,
        label='Método de pago',
        widget=forms.RadioSelect
    )
    # Tarjeta
    nombre_titular = forms.CharField(max_length=100, label='Nombre del titular', required=False)
    numero_tarjeta = forms.CharField(max_length=19, label='Número de tarjeta', required=False)
    ultimos_4 = forms.CharField(max_length=4, required=False, widget=forms.HiddenInput)
    fecha_vencimiento = forms.CharField(max_length=5, label='MM/AA', required=False)
    cvv = forms.CharField(max_length=4, label='CVV', required=False)
    # PayPal
    paypal_email = forms.EmailField(label='Correo PayPal', required=False)

    def clean(self):
        cleaned = super().clean()
        metodo = cleaned.get('metodo')
        if metodo == 'tarjeta':
            num = cleaned.get('numero_tarjeta', '').replace(' ', '')
            if num:
                cleaned['ultimos_4'] = num[-4:]
        return cleaned


class ReservacionGrupalForm(forms.Form):
    nombre_grupo = forms.CharField(max_length=150, label='Nombre del grupo u organización')
    num_pasajeros = forms.IntegerField(min_value=9, label='Número de pasajeros')
    origen = forms.ModelChoiceField(queryset=Aeropuerto.objects.all(), label='Origen', empty_label='Seleccionar')
    destino = forms.ModelChoiceField(queryset=Aeropuerto.objects.all(), label='Destino', empty_label='Seleccionar')
    fecha_salida = forms.DateField(label='Fecha de salida', widget=forms.DateInput(attrs={'type': 'date'}))
    fecha_regreso = forms.DateField(label='Fecha de regreso (opcional)', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    notas = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), label='Información adicional / requerimientos', required=False)
    contacto_nombre = forms.CharField(max_length=100, label='Nombre del contacto')
    contacto_email = forms.EmailField(label='Correo de contacto')
    contacto_telefono = forms.CharField(max_length=20, label='Teléfono de contacto')

    #RESERVACION GRUPAL
    class ReservacionGrupalForm(forms.Form):
        nombre_contacto = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'style': 'width:100%;padding:.75rem 1rem;border:1.5px solid #C8A030;border-radius:8px;font-size:1rem;background:#FFFDF7;color:#3D1F00;box-sizing:border-box',
            'placeholder': 'Tu nombre completo'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'style': 'width:100%;padding:.75rem 1rem;border:1.5px solid #C8A030;border-radius:8px;font-size:1rem;background:#FFFDF7;color:#3D1F00;box-sizing:border-box',
            'placeholder': 'correo@ejemplo.com'
        })
    )
    telefono = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'style': 'width:100%;padding:.75rem 1rem;border:1.5px solid #C8A030;border-radius:8px;font-size:1rem;background:#FFFDF7;color:#3D1F00;box-sizing:border-box',
            'placeholder': '55 1234 5678'
        })
    )
    num_pasajeros = forms.IntegerField(
        min_value=9,
        widget=forms.NumberInput(attrs={
            'style': 'width:100%;padding:.75rem 1rem;border:1.5px solid #C8A030;border-radius:8px;font-size:1rem;background:#FFFDF7;color:#3D1F00;box-sizing:border-box',
        })
    )
    comentarios = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'style': 'width:100%;padding:.75rem 1rem;border:1.5px solid #C8A030;border-radius:8px;font-size:1rem;background:#FFFDF7;color:#3D1F00;box-sizing:border-box',
            'rows': 4,
            'placeholder': 'Destino, fecha tentativa, requerimientos especiales...'
        })
    )