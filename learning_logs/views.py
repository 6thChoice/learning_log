from django.shortcuts import render
from .models import Topic,entry
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request,'learning_logs/index.html')

@login_required
def topics(request):
    # 显示所有的主题
    # topics = Topic.objects.filter(owner=request.user).order_by('date_added') 根据用户，对显示的主题进行筛选，仅显示该用户创建的主题。
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request,'learning_logs/topics.html',context)

@login_required
def topic(request,topic_id):
    # 显示单个主题以及所有条目
    topic = Topic.objects.get(id = topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic':topic,'entries':entries}

    """# 确认请求的主题属于当前用户
    if topic.owner != request.user:
        raise Http404"""

    return render(request,'learning_logs/topic.html',context)

@login_required
def new_topic(request):
    # 处理两种情况
    # 用户刚刚进入new_topic网页
    # 或者用户完成表单的编辑并提交，将用户重新定向到网页topic

    # 添加新主题
    if request.method != 'POST':
        # 用户尚未提交数据，创建一个新表单
        form = TopicForm()
    else:
        # POST 提交的数据，对数据进行处理
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:Topics'))

    context = {'form':form}
    return render(request,'learning_logs/new_topic.html',context)

@login_required
def new_entry(request,topic_id):
    # 在特定的主题中添加新的条目
    topic = Topic.objects.get(id = topic_id)

    if request.method != 'POST':
        # 未提交数据，创建一个空表单
        form = EntryForm()

    else:
        """# 对用户身份进行核对
        if topic.owner != request.user:
            raise Http404"""

        # POST提交数据，并对数据进行处理
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.owner = request.user
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',args=[topic_id]))

    context = {'topic':topic,'form':form}
    return render(request,'learning_logs/new_entry.html',context)

@login_required
def edit_entry(request,entry_id):
    # 编辑既有条目
    entry1 = entry.objects.get(id=entry_id)
    topic = entry1.topic

    # 确认发出请求的用户为合适的用户
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # 初次请求，使用当前条目填充表单
        form = EntryForm(instance=entry1)
    else:
        # POST提交数据，并对数据进行处理
        form = EntryForm(instance=entry1,data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',args=[topic.id]))

    context = {'entry':entry1,'topic':topic,'form':form}
    return render(request,'learning_logs/edit_entry.html',context)