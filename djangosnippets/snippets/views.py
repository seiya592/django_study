from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from snippets.models import Snippet
from django.contrib.auth.decorators import login_required
from snippets.forms import SnippetForm

def top(request):
    snippets = Snippet.objects.all()
    context = {'snippets': snippets}
    return render(request=request, template_name='snippets/top.html', context=context)

@login_required     # ユーザーログインが必要なViewに付けるデコレーター　未認証の場合ログインページにリダイレクト
def snippet_new(request):
    if request.method == 'POST':
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.created_by = request.user
            snippet.save()
            return redirect(snippet_detail, snippet_id=snippet.pk)  #renderでHTMLを返すとブラウザの再読み込みボタンで再度データが操作されてしまうのでredirectにする
    else: # elif request.method == 'GET' の意
        form = SnippetForm()
    return render(request, 'snippets/snippet_new.html', {'form':form})


@login_required
def snippet_edit(request, snippet_id):
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    if snippet.created_by_id != request.user.id:
        return  HttpResponseForbidden('このスニペットの編集は許可されていません。')
    
    if request.method == 'POST':
        form = SnippetForm(request.POST, instance=snippet)      # instance設定をするとフォームのデフォルトの値がHTMLフォームに設定される
        if form.is_valid():
            form.save()
            return redirect(snippet_detail, snippet_id=snippet_id)
    else:
        form = SnippetForm(instance=snippet)
    return render(request, 'snippets/snippet_edit.html', {'form':form})


def snippet_detail(request, snippet_id):
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    return render(request, 'snippets/snippet_detail.html', {'snippet': snippet})

