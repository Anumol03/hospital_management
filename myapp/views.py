from django.shortcuts import render,redirect, get_object_or_404
from django.views.generic import View,FormView
from myapp.forms import RegistrationForm,LoginForm,PasswordResetForm,DoctorForm,DepartmentForm,TimeSlotForm,AppointmentForm
from myapp.models import Doctor,Department,TimeSlot,Appointment
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

class SignUpView(View):
  
    model=User
    template_name="register.html"
    form_class=RegistrationForm
    def get(self,request,*args,**kwargs):
        form=self.form_class
        return render(request,self.template_name,{"form":form})
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"account has been created")
            return redirect("signin")
        messages.error(request,"failed to create account")
        return render(request,self.template_name,{"form":form})
class SignInView(View):
    model=User
    template_name="login.html"
    form_class=LoginForm
    def get(self,request,*args,**kwargs):
        form=self.form_class
        return render(request,self.template_name,{"form":form})
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                messages.success(request,"login success")
                return redirect("index")
            messages.error(request,"login error")
            return render(request,self.template_name,{"form":form})
class PasswordResetView(FormView):
    model=User
    template_name="password-reset.html"
    form_class=PasswordResetForm
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            email=form.cleaned_data.get("email")
            pwd1=form.cleaned_data.get("password1")
            pwd2=form.cleaned_data.get("password2")
            if pwd1==pwd2:
                try:
                    usr=User.objects.get(username=username,email=email)
                    
                    usr.set_password(pwd1)
                    usr.save()
                    messages.success(request,"password changed")
                    return redirect("signin")
                except Exception as e:
                    messages.error(request,"invalid ctredentials")
                    return render(request,self.template_name,{"form":form})
            else:
                messages.error(request,"password mismatch")
                return render(request,self.template_name,{"form":form})
    

class DoctorCreateView(View):
    model=Doctor
    form_class=DoctorForm
    template_name="doctor-add.html"
    def get(self,request,*args,**kwargs):
        form=self.form_class
        return render(request,self.template_name,{"form":form})
    def post(self,request,*args,**kwargs):
        form=self.form_class(files=request.FILES,data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"create doctor successfully")
            return redirect("doctor-add")
        messages.error(request,"failed to create doctor")
        return render(request,self.template_name,{"form":form})
class IndexView(View):
    template_name="index.html"
    def get(self,request,*args,**kwargs):
        return render(request,self.template_name)
def create_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('department-list')
    else:
        form = DepartmentForm()
    return render(request, 'add-department.html', {'form': form})
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'department-list.html', {'departments': departments})
def edit_department(request, department_id):
    department = get_object_or_404(Department, pk=department_id)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect('department-list')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'edit-department.html', {'form': form})
def delete_department(request, department_id):
    department = get_object_or_404(Department, pk=department_id)
    if request.method == 'POST':
        department.delete()
        return redirect('department-list')
    return render(request, 'delete-department.html', {'department': department})
def add_time_slot(request):
    if request.method == 'POST':
        form = TimeSlotForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('time-slot-list')
    else:
        form = TimeSlotForm()
    return render(request, 'addtime-slot.html', {'form': form})