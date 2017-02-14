from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView
from .forms import UserForm, MemberForm, TopUpForm
from .models import  TopUp


def register(request):
    if request.method == 'POST':
        userform = UserForm(request.POST)
        memberform = MemberForm(request.POST)
        if userform.is_valid() * memberform.is_valid():
            user = userform.save(commit=False)
            user.set_password(userform.cleaned_data['password1'])
            user.save()
            member = memberform.save(commit=False)
            member.user = user
            member.save()
            return redirect('login')
    else:
        userform = UserForm()
        memberform = MemberForm()
    return render(request, 'register.html',
                  {'userform':userform, 'memberform':memberform})


class TopUpFormView(CreateView):
    form_class = TopUpForm
    template_name = 'topup_form.html'

    def form_valid(self, form):
        topup = form.save(commit=False)
        topup.member = self.request.user.member
        topup.status = 'p'
        topup.save()
        return redirect('index')


class TopUpListView(ListView):
    template_name = 'topup_list.html'
    model = TopUp

    def get_queryset(self):
        return TopUp.objects.filter(member=self.request.user.member)
