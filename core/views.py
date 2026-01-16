from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, DeviceForm, RuleForm, UsageSessionForm
from .models import Profile, Device, Rule, UsageSession
from .service import format_mac, NetworkdiscoveryService
from datetime import timedelta
from django.utils import timezone


@login_required
def dashboard(request):
    sessoes = UsageSession.objects.filter(status="Ativo")
    sessoesDados = []

    for sessao in sessoes:
        regra = Rule.objects.get(usuario=sessao.usuario)

        fim_sessao = sessao.start_time + timedelta(minutes=regra.tempo)
        print(fim_sessao)
        sessoesDados.append({
            "usuario": sessao.usuario,
            "device": sessao.device,
            "fim_sessao": fim_sessao.isoformat(),
        })

    return render(request, 'dashboard.html', {'sessoes':sessoesDados})



# CRUD inicail do Profile
@login_required
def view_profiles(request):
    profiles = Profile.objects.all()
    return render(request, 'profiles.html', {'profiles': profiles})

@login_required
def view_profile(request, id):
    profile = Profile.objects.get(pk=id)
    rule = Rule.objects.get(usuario = profile)
    return render(request, 'profile.html', {'profile': profile, 'rule':rule})

@login_required
def create_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.save()
            profile = Profile.objects.last()
            rule = Rule.objects.create(
                tempo=0,
                usuario=profile
            )
            rule.save()
            return redirect('profiles')
    else:
        form = form = ProfileForm()

    return render(request, 'profile_create.html',{'form':form})         

@login_required
def delete_profile(request, id):
    Profile.objects.delete(pk=id)
    return render(request)

@login_required
def add_time(request, id):
    if request.method == "POST":
        form = RuleForm(request.POST)
        rule = Rule.objects.get(usuario_id=id)
        if form.is_valid():
            rule.tempo += int(form.data['tempo'])
            rule.save()
            return redirect('profile',id)
    else:
        form = RuleForm()
    return render(request, 'add_time.html', {'form':form, 'id':id})



# CRUD inicial do Device
@login_required
def create_device(request):
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            device = form.save(commit=False)
            device.macAddress = format_mac(device.macAddress)
            device.save()
            return redirect('devices')
    else:
        form = DeviceForm()
        dispositivos_rede = NetworkdiscoveryService()
        for d in dispositivos_rede:
            if Device.objects.filter(macAddress=format_mac(d['mac'])):
                dispositivos_rede.remove(d)
            

    return render(
        request,'device_create.html',{'form': form,'dispositivos_rede': dispositivos_rede})
   
@login_required
def view_devices(request):
    devices = Device.objects.all()
    return render(request,'devices.html',{"devices":devices})

@login_required
def view_device(request, id):
    device = get_object_or_404(Device, pk=id)
    return render(request, 'device.html',{"device":device})

@login_required
def delete_device(request, id):
    Device.objects.delete(pk=id)
    return render(request)



# CRUD inicial do Usage Session
@login_required
def start_session(request):
    devices = Device.objects.filter(status='Desativo')
    profiles = Profile.objects.filter(status='Desativo')
    if request.method == "POST":
        form = UsageSessionForm(request.POST)
        if form.is_valid():
            form.save()
            session = UsageSession.objects.last()
            session.device.status = 'Ativo'
            session.device.save()
            session.usuario.status = 'Ativo'
            session.usuario.save()
            # adicionar fazer uma contagem de tempo com o celery (deixar para mais tarde), Proximo passo.
            return redirect('dashboard')
    else:
        form = UsageSessionForm()
        

    return render(request,'session_create.html', {'form':form, 'devices':devices, 'profiles':profiles})

@login_required
def get_session(request, id):
    session = get_object_or_404(UsageSession, pk=id)
    return render(request, 'session.html', {"session":session})

@login_required
def get_sessions(request):
    sessions = UsageSession.objects.all()
    return render(request,'sessions.html' ,{'sessions':sessions})

@login_required
def finish_session(request, id):
    session = get_object_or_404(UsageSession, pk=id)
    regra = Rule.objects.get(usuario=session.usuario)
    if session.end_time == '':
        session.end_time = timezone.now()
        session.duracao = int((session.end_time - session.start_time).total_seconds() / 60)
        session.status = 'Desativo'
        session.device.status = 'Desativo'
        session.usuario.status = 'Desativo'
        regra.tempo -= session.duracao
        if regra.tempo < 0:
            regra.tempo = 0
        session.save()
        session.device.save()
        session.usuario.save()
        regra.save()
    else:
        print('sessão ja finalizada')
    return redirect('sessions')
