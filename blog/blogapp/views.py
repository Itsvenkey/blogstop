from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from .forms import commentForm,loginForm,registrationForm,AddBlog
from .models import Comment,Post,Category
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    return render(request,"blogapp/base.html")


def register(request):
    
    form = registrationForm()
    if request.method == "POST":
        form = registrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    
    context = {'form':form}
    return render(request,'blogapp/register.html',context=context)



def login(request):
    form = loginForm()
    
    if request.method == 'POST':
        form = loginForm(request,data = request.POST)
        
    if form.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request,username = username,password=password)
        
        if user is not None:
            auth.login(request,user)
            return redirect('blog_index')
    context = {
        'form':form
    }
    
    return render(request,'blogapp/login.html',context)           
            

# @login_required(login_url='login')
def blog_index(request):
    posts = Post.objects.all().order_by("-created_on")
    context = {
        "posts":posts,
    }
    return render(request,"blogapp/index.html",context)

def blog_category(request,category):
    posts = Post.objects.filter(
        categories__name__contains = category
    ).order_by("-created_on")
    context = {
        "category":category,
        "posts": posts,
    }
    return render(request,"blogapp/category.html",context)


@login_required(login_url='login')
def blog_detail(request,pk):
    post = Post.objects.get(pk=pk)
    
    default_author_name = request.user.username if request.user.is_authenticated else "guest"
    
    form  = commentForm(initial={'author':default_author_name})
    
    if request.method == "POST":
        form = commentForm(request.POST)
        if form.is_valid():
            comment= Comment(
                author = form.cleaned_data["author"],
                body = form.cleaned_data["body"],
                post = post,
            )
            comment.save()
            return HttpResponseRedirect(request.path_info)
        
    comments = Comment.objects.filter(post=post)
    context ={
        "post":post,
        "comment":comments,
        "form":form
    }
    return render(request,"blogapp/detail.html",context)


def logout(request):
    auth.logout(request)
    return redirect('login')


@login_required(login_url='login')
def add_blog(request):
    if request.method=='POST':
        form = AddBlog(request.POST)
        
        if form.is_valid():
            post = form.save(commit=False)
           
            existing_categories = form.cleaned_data.get('categories',[])
            post.save()
            post.categories.add(*existing_categories)
            
            custom_categories_str = form.cleaned_data.get('custom_category','').strip()
            custom_categories = [category.strip() for category in custom_categories_str.split(',') if category.strip()]
            
            for custom_category in custom_categories:
                category,created = Category.objects.get_or_create(name=custom_category)
                if created:
                    post.categories.add(category)
                else:
                    print('category already exists:',category)
            
            post.created_by = request.user.username
            post.save()
            # if custom_category:
            #     category,created= Category.objects.get_or_create(name=custom_category)
            #     # post.categories.add(category)
            #     if isinstance(category,Category):
            #         post.categories.add(category)
            #     else:
            #         print('invalid category instance',category)
            # post.save()
            return redirect('blog_index')
    else:
        form = AddBlog()
        # form =AddBlog(initial={'created_by':request.user.username})
        form.fields['categories'].queryset = Category.objects.all()
    
    return render(request,'blogapp/add-blog.html',{'form':form})