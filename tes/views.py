import datetime

from django.shortcuts import get_object_or_404
from django.http.request import HttpRequest
from .models import Question, Choice

from django.contrib import auth
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.
from django.urls import reverse


def index(request):
    context = {
        'active_menu': 'homepage'
    }
    return render(request, 'tes/index.html', context)


#  投票的统计结果
def results(request: HttpRequest, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'tes/results.html', {'question': question})


#  审核通过功能   通过将Question的ready+1 实现展示
@user_passes_test(lambda u: u.is_staff)
def audit(request: HttpRequest, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        question.ready += 1
        question.save()
        # choice = question.choice_set.get(pk=request.POST.get('choice'))
        # choice.votes += 1
        # choice.save()
        return HttpResponseRedirect(redirect_to='/tes/polls_audit/')
    #     上面的什么时候需要try 和 render Redirect 等怎么用
    # 此处 /tes/polls_audit/ 直接回到url  tes/polls_audit
    except Question.DoesNotexist:
        ctx = {'question': question,
               'error_message': 'Question dose not exist'}
        return render(request, 'tes/polls_audit_detail.html', ctx)


#  审核失败功能 直接删除这个问题
@user_passes_test(lambda u: u.is_staff)
def audit_del(request: HttpRequest, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # 上面这句这么牛，搞不懂。
        # question = Question.objects.get(pk=question_id)
        question.delete()
        return HttpResponseRedirect(redirect_to='/tes/polls_audit/')
    except Question.DoesNotexist:
        ctx = {'question': question,
               'error_message': 'Question dose not exist'}
        return render(request, 'tes/polls_audit_detail.html', ctx)


#  审核列表 问题的属性ready！= 1 的显示出来 待审核
@user_passes_test(lambda u: u.is_staff)
def polls_audit(request):
    user = request.user
    questions = Question.objects.all()
    paginator = Paginator(questions, 100)  # 分页操作，每次5个对象
    page = request.GET.get('page')  # 创建分页对象
    try:
        questions = paginator.page(page)  # page(int) 取对象的某页的对象 此处为当前页
    except PageNotAnInteger:
        questions = paginator.page(1)  # 取对象的第一页 分页对象
    except EmptyPage:  # EmptyPage、PageNotAnInteger这两个类是为了防止p值（当前页码）不是int类型、或者大于总页码的情况；
        questions = paginator.page(paginator.num_pages)  # num_pages 总页数

    context = {
        'user': user,
        'active_menu': 'polls_audit',
        'questions_list': questions
    }
    return render(request, 'tes/polls_audit.html', context)


#  审核详情页
@user_passes_test(lambda u: u.is_staff)
def polls_audit_detail(request, questions_id=1):
    user = request.user
    # try:
    question = get_object_or_404(Question, pk=questions_id)

    # questions = Question.objects.get(pk=questions_id)  # 根据id返回相应书籍
    # except Question.DoseNotExist:
    # return HttpResponseRedirect(reverse('polls_list'))

    content = {
        'user': user,
        'active_menu': 'view_book',
        'question': question
    }
    return render(request, 'tes/polls_audit_detail.html', content)


def add_img(request):
    pass


#  发起投票
@login_required
def add_polls(request):
    user = request.user
    state = None
    if request.method == 'POST':
        new_polls = Question(
            author_name_id=user.id,
            end_date=request.POST.get('end_date', ''),
            question_text=request.POST.get('question_text', ''),

        )
        new_polls.save()
        new_polls.choice_set.create(choice_text=request.POST.get('choice_text', ''))
        state = 'success'

    context = {
        'user': user,
        'active_menu': 'add_polls',
        'state': state,
    }
    return render(request, 'tes/add_polls.html', context)


# #  管理员添加书籍
# @user_passes_test(lambda u: u.is_staff)
# def add_book(request):
#     user = request.user
#     state = None
#     if request.method == 'POST':
#         new_book = Question(
#             name=request.POST.get('name', ''),
#             author=request.POST.get('author', ''),
#             category=request.POST.get('category', ''),
#             price=request.POST.get('price', 0),
#             publish_date=request.POST.get('publish_date', '')
#
#         )
#         new_book.save()
#         state = 'success'
#     context = {
#         'user': user,
#         'active_menu': 'add_book',
#         'state': state,
#     }
#     return render(request, 'management/add_book.html', context)


#  所有投票列表
@login_required
def polls_list(request):
    user = request.user
    questions = Question.objects.all()
    paginator = Paginator(questions, 5)  # 分页操作，每次5个对象
    page = request.GET.get('page')  # 创建分页对象
    try:
        questions = paginator.page(page)  # page(int) 取对象的某页的对象 此处为当前页
    except PageNotAnInteger:
        questions = paginator.page(1)  # 取对象的第一页 分页对象
    except EmptyPage:  # EmptyPage、PageNotAnInteger这两个类是为了防止p值（当前页码）不是int类型、或者大于总页码的情况；
        questions = paginator.page(paginator.num_pages)  # num_pages 总页数
    context = {
        'user': user,
        'active_menu': 'view_book',
        'questions_list': questions
    }
    return render(request, 'tes/polls_list.html', context)


#  我发起的投票 的 列表
@login_required
def polls_list_my(request):
    user = request.user
    questions = Question.objects.all()
    paginator = Paginator(questions, 100)  # 分页操作，每次5个对象
    page = request.GET.get('page')  # 创建分页对象
    try:
        questions = paginator.page(page)  # page(int) 取对象的某页的对象 此处为当前页
    except PageNotAnInteger:
        questions = paginator.page(1)  # 取对象的第一页 分页对象
    except EmptyPage:  # EmptyPage、PageNotAnInteger这两个类是为了防止p值（当前页码）不是int类型、或者大于总页码的情况；
        questions = paginator.page(paginator.num_pages)  # num_pages 总页数
    context = {
        'user': user,
        'active_menu': 'view_polls_my',
        'questions_list': questions,
    }
    return render(request, 'tes/polls_list_my.html', context)


#  投票详情
@login_required
def polls_detail(request, questions_id=1):
    user = request.user
    # try:
    question = get_object_or_404(Question, pk=questions_id)

    # questions = Question.objects.get(pk=questions_id)  # 根据id返回相应书籍
    # except Question.DoseNotExist:
    # return HttpResponseRedirect(reverse('polls_list'))

    content = {
        'user': user,
        'active_menu': 'view_book',
        'question': question
    }
    return render(request, 'tes/polls_detail.html', content)


#  投票功能
@login_required
def vote(request: HttpRequest, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        choice = question.choice_set.get(pk=request.POST.get('choice'))
        choice.votes += 1
        choice.save()
        # return  redirect(reverse( 'polls:result',args=(question.id)))
        return HttpResponseRedirect(redirect_to=f'/tes/{question.id}/results')
    except Choice.DoesNotexist:
        ctx = {'question': question,
               'error_message': f'Choice{request.POST.get("choice")} dose not exist'}
        return render(request, 'tes/polls_detail.html', ctx)


#  用户注册功能
def sign_up(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('homepage'))
    state = None
    if request.method == 'POST':  # 判断用户的访问方式是POST还是GET
        password = request.POST.get('password', '')
        repeat_password = request.POST.get('repeat_password', '')
        if password == '' or repeat_password == '':
            state = 'empty'  # state用于描述我们在处理注册流程中的状态
        elif password != repeat_password:
            state = 'repeat_error'
        else:
            username = request.POST.get('username', '')
            if User.objects.filter(username=username):
                state = 'user_exist'
            else:
                new_user = User.objects.create_user(username=username, password=password,
                                                    email=request.POST.get('email', ''))
                new_user.save()
                state = 'success'
    context = {
        'active_menu': 'homepage',
        'state': state,
        'user': None
    }
    return render(request, 'tes/sign_up.html', context)


#  用户登陆功能
def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('homepage'))
    state = None
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            target_url = request.GET.get('next', reverse('homepage'))
            return HttpResponseRedirect(target_url)
        else:
            state = 'not_exist_or_password_error'
    context = {
        'active_menu': 'homepage',
        'state': state,
        'user': None
    }
    return render(request, 'tes/login.html', context)


#  用户注销功能
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('homepage'))


#  修改密码
@login_required  # 判断用户是否为一个登陆用户
def change_password(request):
    user = request.user
    state = None
    if request.method == 'POST':
        old_password = request.POST.get('old_password', '')
        new_password = request.POST.get('new_password', '')
        repeat_password = request.POST.get('repeat_password', '')
        if user.check_password(old_password):
            if not new_password:
                state = 'empty'
            elif new_password != repeat_password:
                state = 'repeat_error'
            else:
                user.set_password(new_password)
                user.save()
                state = 'success'
        else:
            state = 'password_error'
    content = {
        'user': user,
        'active_menu': 'homepage',
        'state': state,

    }

    return render(request, 'tes/change_password.html', content)
