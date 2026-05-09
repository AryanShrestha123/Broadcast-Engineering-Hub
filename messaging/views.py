from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from .models import Message
from .forms import MessageForm
from account.models import CustomUser
from notifications.utils import notify_message_received

@login_required
def inbox(request):
    messages_list = Message.objects.filter(receiver=request.user, is_draft=False).order_by('-timestamp')
    unread_count = messages_list.filter(is_read=False).count()
    context = {
        'messages_list': messages_list,
        'view': 'inbox',
        'unread_count': unread_count,
        'active_page': 'messaging',
    }
    return render(request, 'messaging/messages.html', context)

@login_required
def sent_messages(request):
    messages_list = Message.objects.filter(sender=request.user, is_draft=False).order_by('-timestamp')
    context = {
        'messages_list': messages_list,
        'view': 'sent',
        'unread_count': 0,
        'active_page': 'messaging',
    }
    return render(request, 'messaging/messages.html', context)      
    

@login_required
def drafts(request):
    messages_list = Message.objects.filter(sender=request.user, is_draft=True).order_by('-timestamp')
    context = {
        'messages_list': messages_list,
        'view': 'drafts',
        'unread_count': 0,
        'active_page': 'messaging',
    }
    return render(request, 'messaging/messages.html', context)

@login_required
def compose_message(request):
    draft_id = request.GET.get('draft_id')
    message_instance = None
    if draft_id:
        message_instance = get_object_or_404(Message, sender=request.user, is_draft=True, pk=draft_id)

    initial = {}
    if not message_instance and request.method == 'GET' and 'to' in request.GET:
        try:
            initial['receiver'] = CustomUser.objects.get(pk=request.GET.get('to'))
        except CustomUser.DoesNotExist:
            initial = {}

    if request.method == 'POST':
        form = MessageForm(request.POST, sender=request.user, instance=message_instance)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.is_draft = 'save_draft' in request.POST
            message.save()
            if message.is_draft:
                django_messages.success(request, 'Draft saved successfully.')
                return redirect('messaging:messages_drafts')
            notify_message_received(message.receiver, request.user, message)
            django_messages.success(request, 'Message sent successfully!')
            return redirect('messaging:messages_inbox')
    else:
        form = MessageForm(sender=request.user, instance=message_instance, initial=initial)

    context =  {
        'form': form,
        'draft_id': draft_id,
        'message_instance': message_instance,
        'active_page': 'messaging',
    }
    return render(request, 'messaging/compose.html', context)

@login_required
def view_message(request, message_id):
    message = get_object_or_404(Message, Q(receiver=request.user) | Q(sender=request.user), pk=message_id)
    if message.receiver == request.user and not message.is_read and not message.is_draft:
        message.is_read = True
        message.save()
    return render(request, 'messaging/message_detail.html', {'msg': message})

@login_required
def delete_message(request, message_id):
    msg = get_object_or_404(Message, Q(receiver=request.user) | Q(sender=request.user), pk=message_id)
    if request.method == 'POST':
        redirect_name = 'messages_inbox' if msg.receiver == request.user else 'messages_sent'
        if msg.is_draft:
            redirect_name = 'messages_drafts'
        msg.delete()
        return redirect(f'messaging:{redirect_name}')
    return redirect('messaging:message_detail', message_id=message_id)