from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import PostForm
from .models import Post
from laundryManagementSystem.addtocart.models import CartProduct
from django.views.generic import ListView, DetailView, TemplateView
# Create your views here.

class HomeView(ListView):
    model = Post
    template_name = 'homedemo.html'



class CustomDetailView(DetailView):
    model = Post
    template_name = "details.html"
  


"""
def home(request):
    return render(request, 'homedemo.html', {})
"""
"""
def demo(request):
    if request.method == 'POST':
        demo = DemoForm(request.POST)

        username = request.GET.get('username')
        print(username)
        
        password = request.GET.get('password')
        print(password)

       
        if demo.is_valid():
            # Here after getting these post values
            # use queries to create the object instance

            Demo.objects.create(
                username = request.POST.get('username'),
                password = request.POST.get('password')
            )

            print('You are good bro!')

            return HttpResponseRedirect('/index2/')
        
    else:
        demo = DemoForm()
        
    context = {'demo': demo}
    print(request.POST.get('username'))
    print(request.GET.get('passwords'))
    return render(request, 'demo/demo.html', context)
"""

class TestingRESTAPI(TemplateView):
    template_name = 'apidemo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['id'] = 2 
        return context  