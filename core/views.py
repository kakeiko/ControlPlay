from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, DeviceForm, RuleForm, UsageSessionForm
from .models import Profile, Device, Rule, UsageSession
from .service import format_mac, usage_service, NetworkdiscoveryService
from datetime import timedelta


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
            form.data['macAddress'] = format_mac(form.data['macAddress'])
            form.save()
            return redirect('devices')
    else:
        form = DeviceForm()
        NetworkdiscoveryService()

    return render(request,'device_create.html',{'form': form})

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
    if request.method == "POST":
        form = UsageSessionForm(request.POST)
        if form.is_valid():
            form.save()
            session = UsageSession.objects.last()
            session.device.status = 'Ativo'
            session.usuario.status = 'Ativo'
            # adicionar fazer uma contagem de tempo com o celery (deixar para mais tarde)
            return redirect('dashboard')
    else:
        form = UsageSessionForm()
    
    return render(request,'session_create.html', {'form':form})

@login_required
def get_session(request, id):
    session = get_object_or_404(UsageSession, pk=id)
    usado, restante = usage_service(session, False)
    return render(request, {"session":session, 'usado':usado, 'restante':restante})

