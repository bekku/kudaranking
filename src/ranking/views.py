from django.shortcuts import render, get_object_or_404,redirect
from .models import create_ranking,Post_rank,Post_coment
from .forms import create_rankingForm,Post_rankForm,Post_comentForm

from django.db import models
from django.conf import settings
from userAccount.models import CustomUser

from django.db.models import Count
from django.views import generic
from django.utils import timezone

from django.contrib import messages
from django.db.models import Q

from django.db.models import Max, Min

import statistics
import math

import json
from django.utils.safestring import mark_safe
from decimal import Decimal
import random

###########ランキングの並び替え関数U(引数はorderによるオブジェクト)################
def rankduke(a):
    a_string_object=[]#投稿をリストに変換
    number_data=[]
    #数値のみのリスト
    hensati=[]
    #偏差値の入るリスト
    for i in a:
        get_data=list(str(i).split())
        a_string_object.append(get_data)
        number_data.append(float(get_data[1]))

    number_data_mean=statistics.mean(number_data)
    #平均値
    hyohensa=Decimal(statistics.pstdev(number_data))
    #標準偏差
    #偏差値＝(x-平均)/標準偏差*10+50
    ranking_juni=[]##実際の順位が入る配列。
    juni_rank_desicion =0
    for j in range(0,len(a_string_object)-1):
        if hyohensa!=0:
            hyohensa = float(hyohensa)
            hensati.append('{:.1f}'.format((number_data[j]-number_data_mean)/hyohensa*10+50))
        else:
            hensati.append(50.0)
        ranking_juni.append(str(juni_rank_desicion+1))
        if a_string_object[j][1]!=a_string_object[j+1][1]:
            juni_rank_desicion =j+1
    if a_string_object[len(a_string_object)-2][1]!=a_string_object[len(a_string_object)-1][1]:
        juni_rank_desicion =j+1
    ranking_juni.append(str(juni_rank_desicion+1))
    if hyohensa!=0:
        hyohensa = float(hyohensa)
        hensati.append('{:.1f}'.format((number_data[-1]-number_data_mean)/hyohensa*10+50))
    else:
        hensati.append(50.0)

    kaifor=0
    for i in a:
        i.Post_juni=ranking_juni[kaifor]
        i.Post_hensati=hensati[kaifor]
        #データを１つずつ、常に保存する。
        i.save()
        kaifor+=1
    return a
#####################################################

###########逆偏差値################
def up_rankduke(a):
    a_string_object=[]#投稿をリストに変換
    number_data=[]
    #数値のみのリスト
    hensati=[]
    #偏差値の入るリスト
    for i in a:
        get_data=list(str(i).split())
        a_string_object.append(get_data)
        number_data.append(float(get_data[1]))

    number_data_mean=statistics.mean(number_data)
    #平均値
    hyohensa=statistics.pstdev(number_data)
    #標準偏差
    #偏差値＝(x-平均)/標準偏差*10+50
    ranking_juni=[]##実際の順位が入る配列。
    juni_rank_desicion =0
    for j in range(0,len(a_string_object)-1):
        if int(hyohensa)!=0:
            hensati.append('{:.1f}'.format(50-(number_data[j]-number_data_mean)/hyohensa*10))
        else:
            hensati.append(50.0)
        ranking_juni.append(str(juni_rank_desicion+1))
        if a_string_object[j][1]!=a_string_object[j+1][1]:
            juni_rank_desicion =j+1
    if a_string_object[len(a_string_object)-2][1]!=a_string_object[len(a_string_object)-1][1]:
        juni_rank_desicion =j+1
    ranking_juni.append(str(juni_rank_desicion+1))
    if int(hyohensa)!=0:
        hensati.append('{:.1f}'.format(50-(number_data[-1]-number_data_mean)/hyohensa*10))
    else:
        hensati.append(50.0)

    kaifor=0
    for i in a:
        i.Post_juni=ranking_juni[kaifor]
        i.Post_hensati=hensati[kaifor]
        #データを１つずつ、常に保存する。
        i.save()
        kaifor+=1
    return a
#####################################################


class IndexList(generic.ListView):
    model=create_ranking#モデル名_listとしてオブジェクトが与えられる。
    paginate_by = 5
    ordering = ('-post_count','-ranking_updated_at')# Choices are: Posts, Posts_coment, description, element, id, title
    template_name = 'ranking/index.html'#無記述だと、「モデル名」_list.htmlに結ばれる。
    #モデルを複数listviwにすることは不可能なのだろうか？
    #下記の通りでRecommendというキーによって二つ目のモデルを追加することが可能になりました。
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        ####### ログインユーザーが参加済みランキングかどうか判別 #######
        article_list=set()
        if self.request.user.username:
            article_list = Post_rank.objects.filter(Posteduser=self.request.user).values_list('article', flat=True)
            article_list = set(article_list)#表示するランキングが少ない場合、setにしてもその恩恵がとても少ないので、5以上にはするようにしてください。
        context['article_set'] =  article_list

        ####### 新着ランキング表示 #######
        context['Recommend'] =  create_ranking.objects.all().order_by('-id')[:5]

        ####### ランダムランキング表示 #######

        # max_id = create_ranking.objects.all().aggregate(Max('id'))
        # min_id = create_ranking.objects.all().aggregate(Min('id'))
        # random_page_list = random.sample(range(min_id['id__min'],max_id['id__max']), k=10)
        # context['random2'] = random_page_list
        # context['random'] = create_ranking.objects.filter(Q(pk=random_page_list[0]) | Q(pk=random_page_list[1]) | Q(pk=random_page_list[2]) | Q(pk=random_page_list[3]) | Q(pk=random_page_list[4]))

        random_ranking = create_ranking.objects.all()[:5]
        random_ranking = list(random_ranking)
        random.shuffle(random_ranking)
        context['random'] = random_ranking

        ####### 急上昇ランキング表示 #######
        soar_lists=[]
        soar_lists_five=[]
        for soar_list in list(create_ranking.objects.all().order_by('-id')[:100]):
            soar_lists.append([int(soar_list.post_count),int(soar_list.id)])
        soar_lists.sort(reverse=True)
        from itertools import chain
        # https://qa.codeflow.site/questions/431628/how-to-combine-2-or-more-querysets-in-a-django-view
        # chainによってquerysetの結合ができる。
        # 一般的な結合を実施場合、order_byによる順付けの制限が残って並び替えられてしまう。
        if len(soar_lists)>=5:
            tttt=chain(create_ranking.objects.filter(Q(pk=soar_lists[0][1])),create_ranking.objects.filter(Q(pk=soar_lists[1][1])),create_ranking.objects.filter(Q(pk=soar_lists[2][1])),create_ranking.objects.filter(Q(pk=soar_lists[3][1])),create_ranking.objects.filter(Q(pk=soar_lists[4][1])))
            context['Soar'] =tttt


        return context


def rankpage(request, ranking_id):
    rank = get_object_or_404(create_ranking,id=ranking_id)
    a=rank.Posts.order_by('-Post_element')
    post_coment=rank.Posts_coment.order_by('-id')
    # requestがPOSTつまり、フォームで送信されてこのサイトに到達したとき。


    # 上限スイッチを何かしらの理由で消した時、paged関数によってスイッチするため、rankpageが開けてしまうのを阻止するためにrankpageにも同様のスイッチを付与
    if rank.post_count>=1000 and rank.Done_ranking==False:
        rank.Done_ranking=True
        rank.save()

    if rank.Done_ranking==True:
        return redirect('ranking:rankpaged',ranking_id=ranking_id)

    if request.method == "POST":
        Flag=True
        Pform = Post_rankForm(request.POST)
        Cform = Post_comentForm(request.POST)
        rank = get_object_or_404(create_ranking,id=ranking_id)

    ###Cformが正しいコメントが入力されるかどうかを確認する。
        if Cform.is_valid():#正しいフォームの方を保存する。つまり送られたリクエストが正しい方が保存されることになる
            rank.coment_count += 1#コメントするごとに＋１して保存する。投稿も同様
            rank.save()
            Post_coment.objects.create(Post_coment_name=request.POST["Post_coment_name"],Post_coment_text=request.POST["Post_coment_text"],article=rank)
            return redirect('ranking:rankpage',ranking_id=ranking_id)

    else:
        Pform = Post_rankForm
        Cform = Post_comentForm
        max_number=rank.max_number
        min_number=rank.min_number
        return render(request, 'ranking/rankpage.html', {'rankpage': rank,'form':Pform,'a':a,'post_coment':post_coment,'Cform':Cform,'max_number':max_number,'min_number':min_number,})


################ランキング作成#################


def new(request):

    # 最大＜最小のような矛盾は、入力値を保持してエラーメッセと共に作成ページに戻します。
    # 最大、最小に値がない場合は、デフォルト値を代入しています。

    Contradiction_flag=False
    if request.method == "POST":
        cp = request.POST.copy()
        if cp["max_number"]=="":
            cp["max_number"] = int(1000000)
        if cp["min_number"]=="":
            cp["min_number"] = int(0)
        Contradiction_flag=False
        if int(cp["max_number"]) >= int(cp["min_number"]):
        #Queryで渡されるvalueは基本文字、数字の比較は絶対intつけてください。
        #"543"<"12234"が辞書順となりFalseになっていました。
            Contradiction_flag=True
            jfldksa1 = int(cp["max_number"])
            jfldksa2 = int(cp["min_number"])
        form = create_rankingForm(cp)
        NG_word_set = set(["殺す","殺害","爆破","死ぬ","自殺","http:","https:"])
        t = ""
        if form.is_valid():

            if Contradiction_flag==False:
                t = "※最大値と最小値が矛盾しています。"
                return render(request, 'ranking/new.html', {'form':form,'t':t,'cp':cp,})

            for NG_word in NG_word_set:
                if NG_word in str(cp["title"]) or NG_word in str(cp["element"]) or NG_word in str(cp["description"]):
                    t = "※NGワードが含まれています。"
                    return render(request, 'ranking/new.html', {'form':form,'t':t,'cp':cp,})

            newranking = form.save(commit=False)###ユーザーに紐付け成功
            newranking.Createduser = request.user
            newranking.save()
            return redirect('ranking:index')
    else:
        form = create_rankingForm
        return render(request, 'ranking/new.html', {'form':form})

################ランキング作成#################




################検索機能#################
class search_results(generic.ListView):
    model = create_ranking
    template_name = 'ranking/search_results.html'
    paginate_by = 10
    def get_queryset(self):
        queryset = create_ranking.objects.order_by('-id')
        keyword = self.request.GET.get('keyword')
        if keyword:
            queryset = queryset.filter(Q(title__icontains=keyword))
            messages.success(self.request, '「{}」の検索結果'.format(keyword))
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['AAA'] =  self.request.GET.get('csrfmiddlewaretoken')
        context['key'] = self.request.GET.get('keyword')
        return context
#######################################

# ?csrfmiddlewaretoken=QUzyI6IlqxF3NXduinhOhUQVuxnpPImM9nTEk7dYIPgWnry10KhzYvHZqutafwpn&keyword

class Soaring_ranking(generic.ListView):
    model=create_ranking#モデル名_listとしてオブジェクトが与えられる。
    paginate_by = 10
    ordering = ('-post_count','-ranking_updated_at')# Choices are: Posts, Posts_coment, description, element, id, title
    template_name = 'ranking/Soaring_ranking.html'#無記述だと、「モデル名」_list.htmlに結ばれる。
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article_list=set()
        if self.request.user.username:
            article_list = Post_rank.objects.filter(Posteduser=self.request.user).values_list('article', flat=True)
            article_list = set(article_list)#表示するランキングが少ない場合、setにしてもその恩恵がとても少ないので、5以上にはするようにしてください。
        context['article_set'] =  article_list
        #context['article_set_type'] = type(article_list)#セットの型になっているか確認。
        return context

class newest_ranking(generic.ListView):
    model=create_ranking#モデル名_listとしてオブジェクトが与えられる。
    paginate_by = 10
    ordering = ('-id')# Choices are: Posts, Posts_coment, description, element, id, title
    template_name = 'ranking/newest_ranking.html'#無記述だと、「モデル名」_list.htmlに結ばれる。
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article_list=set()
        if self.request.user.username:
            article_list = Post_rank.objects.filter(Posteduser=self.request.user).values_list('article', flat=True)
            #modelの投稿者がリクエストユーザーに一致するデータを取り出す。
            article_list = set(article_list)#表示するランキングが少ない場合、setにしてもその恩恵がとても少ないので、5以上にはするようにしてください。
        context['article_set'] =  article_list
        #context['article_set_type'] = type(article_list)#セットの型になっているか確認。
        return context


def rankpaged(request, ranking_id):
    ranking_page = get_object_or_404(create_ranking,id=ranking_id)
    result_ranking=""
    result_element=""
    result_hensati=""

    Done_ranking_error = ""
    #参加していないランキングページだと〜位っていうリザルトの値が設定されていないためエラー表示
    #逆にresult値の判定でエラーページを表示させる方向もありではあるね。エラー404みたいな。

    if ranking_page.up_or_down:
        ranking_page_post=ranking_page.Posts.order_by('Post_element')
        #降順に取り出し
    else:
        ranking_page_post=ranking_page.Posts.order_by('-Post_element')
        #昇順に取り出し
    ranking_page_coment=ranking_page.Posts_coment.order_by('-id')
    post_coment=ranking_page.Posts_coment.order_by('-id')

    # 1000件達していた場合の処理
    # ①1000件以上になった場合にtrueにスイッチする。
    if ranking_page.post_count>=1000 and ranking_page.Done_ranking==False:
        ranking_page.Done_ranking=True
        ranking_page.save()
    # ②1000件以上でかつ、POST(投稿)で飛ばされた場合エラー文と共にリダイレクト
    if ranking_page.Done_ranking==True and request.method == "POST" and Post_rankForm(request.POST).is_valid():
        Done_ranking_error = "※投稿上限に達しているため、投稿できませんでした。"
        Pform = Post_rankForm(request.POST)
        Cform = Post_comentForm(request.POST)
        get_element_list=[]
        ranking_page = get_object_or_404(create_ranking,id=ranking_id)
        if ranking_page.up_or_down:
            ranking_page_post=ranking_page.Posts.order_by('Post_element')
            #降順に取り出し
        else:
            ranking_page_post=ranking_page.Posts.order_by('-Post_element')
            #昇順に取り出し
        ###上記によりデータが追加されたので、もう一度ソートしつつ取り出す。###
        result=""
        if len(ranking_page_post)>=1 and not ranking_page.up_or_down:
            rankduke(ranking_page_post)
            #降順によるランク付
        elif len(ranking_page_post)>=1 and ranking_page.up_or_down:
            up_rankduke(ranking_page_post)
            #昇順によるランク付(偏差値の修正)
        else:
            #len(ranking_page_post)<1となるのは、誰も投稿していないランキングにurlからアクセスされた時である。
            ranking_juni=[]

        return render(request, 'ranking/rankpaged.html', {'rankpage': ranking_page,'result':result,'a':ranking_page_post,'post_coment':post_coment,'Cform':Cform,'ranking_page_json': mark_safe(json.dumps(ranking_id)),'result_hensati':result_hensati,'result_ranking':result_ranking,'result_element':result_element,'error_mse':Done_ranking_error ,})



    if request.method == "POST":

        Pform = Post_rankForm(request.POST)
        Cform = Post_comentForm(request.POST)

        Valid_Flag=True
        #投稿が正しいかどうかを判別。

        if Pform.is_valid():
            Cform = Post_comentForm
            #PformがValidの時点でCformに代入するのは普通のformに変更。
            #そうすることで、(このフィールドは必須ですみたいな)Cformのエラーが表示されない。
            if request.user.username:
                #ユーザーアカウントあり
                get_element_list=[]
                #偏差値を出すために数値だけを取り出すリスト
                for i in ranking_page_post:
                    if i.Posteduser==request.user:
                        #リクエストユーザーが既に投稿済データのPosteduserと同じ場合。
                        i.Post_element=request.POST["Post_element"]
                        #新しく入力された要素値を上書きする。
                        i.save()
                        Valid_Flag=False
                        break
                        #セーブして終了。

                if Valid_Flag==True:
                    #Post_rankにユーザーのデータがなかった場合、正しい投稿と判断。
                    ranking_page.post_count += 1
                    #投稿数を1増やす
                    ranking_page.save()
                    newpost=Pform.save(commit=False)
                    #フォームのforeignkey以外のデータを保留。
                    newpost.Posteduser=request.user
                    newpost.article=ranking_page
                    newpost.save()
                    #保留にしていたためsave()

            else:
                 #ユーザーアカウントなし
                 for i in ranking_page_post:
                     get_data=list(str(i).split())
                     if (not i.Posteduser) and (str(request.POST["Post_name"])==get_data[0] and float(request.POST["Post_element"])==float(get_data[1])):
                         #全く同じデータの時かつ、Posteduserが空の場合。
                         #Posteduser＝空→アカウントなし。
                         #Posteduserは、別にいてもよい。
                         Valid_Flag=False
                         #投稿が正しくないと判別。
                         break

                 if Valid_Flag==True:
                    #post_rankに同名同値ユーザーがいない場合。
                    ranking_page.post_count += 1
                    #投稿数を1増やす
                    ranking_page.save()
                    notaccount_name=str(request.POST["Post_name"])
                    notaccount_element=str(request.POST["Post_element"])
                    #〜位でしたの結果表示のために、値と名前をメモしておく。
                    newpost=Pform.save(commit=False)
                    newpost.article=ranking_page
                    newpost.save()
                 else:
                    #フォーム内容が正しくても、Valid_flag=Falseの時は、値は保存せずにリダイレクトする。
                    Cform = Post_comentForm
                    Pform = Post_rankForm
                    return redirect('ranking:rankpaged',ranking_id=ranking_id)


            ###上記によりデータが追加されたので、もう一度ソートしつつ取り出す。###
            ranking_page = get_object_or_404(create_ranking,id=ranking_id)

            if ranking_page.up_or_down:
                ranking_page_post=ranking_page.Posts.order_by('Post_element')
                #降順に取り出し
            else:
                ranking_page_post=ranking_page.Posts.order_by('-Post_element')
                #昇順に取り出し
            ###上記によりデータが追加されたので、もう一度ソートしつつ取り出す。###
            result=""
            if len(ranking_page_post)>=1 and not ranking_page.up_or_down:
                rankduke(ranking_page_post)
                #降順によるランク付
            elif len(ranking_page_post)>=1 and ranking_page.up_or_down:
                up_rankduke(ranking_page_post)
                #昇順によるランク付(偏差値の修正)
            else:
                #len(ranking_page_post)<1となるのは、誰も投稿していないランキングにurlからアクセスされた時である。
                ranking_juni=[]
            result=""
            #resultに〜位でした！みたいな結果が表示される。

            #####以下リザルト表記######
            if request.user.username:
                #ユーザーアカウント持ちの場合。
                return redirect('ranking:rankpaged',ranking_id=ranking_id)
                # for i in ranking_page_post:
                #     if request.user==i.Posteduser:
                #         #自分のアカウントを見つけた場合。
                #         result=str(ranking_page.title)+"において"+"\n"+str(i.Post_name)+"さんの順位は"+str(int(i.Post_juni))+"位でした！！！"
                #         break
                #これはリダイレクト時もする処理なので、わざわざここで行い、renderする必要なし。アカウントあるならredirectでも表示させられるので。
            else:
                #ユーザーアカウントnot持ちの場合。
                for i in ranking_page_post:
                    if (notaccount_name==i.Post_name) and (notaccount_element==str(i.Post_element) or notaccount_element==str(int(i.Post_element))):
                        #自分が投稿したものを、notアカウント時にメモっているのでそれを探索。名前のみだと名前が重複時バグが発生。
                        #入力がint式なら、notaccount_elementはintになってしまう。float型で保存されてしまっているのでそこで差が生じてしまう。
                        result=str(ranking_page.title)+"において"+"\n"+str(i.Post_name)+"さんの順位は"+str(int(i.Post_juni))+"位でした！！！"
                        result_ranking=str(int(i.Post_juni))
                        result_element=i.Post_element
                        if ranking_page.int_or_float == False:
                            result_element = int(result_element)
                        result_hensati=i.Post_hensati
                        break
                  #####以上リザルト表記######
                return render(request, 'ranking/rankpaged.html', {'rankpage': ranking_page,'result':result,'a':ranking_page_post,'post_coment':post_coment,'Cform':Cform,'ranking_page_json': mark_safe(json.dumps(ranking_id)),'result_hensati':result_hensati,'result_ranking':result_ranking,'result_element':result_element,})
        """
        elif Cform.is_valid():
            #正しいフォームの方を保存する。つまり送られたリクエストが正しい方が保存されることになる。
            Pform = Post_rankForm
            ranking_page.coment_count += 1
            ranking_page.save()
            Post_coment.objects.create(Post_coment_name=request.POST["Post_coment_name"],Post_coment_text=request.POST["Post_coment_text"],article=ranking_page)
            return redirect('ranking:rankpaged',ranking_id=ranking_id)
        """

    else:
        result=""
        if request.user.username:
            for i in ranking_page_post:
                if request.user==i.Posteduser:
                    result=str(ranking_page.title)+"において"+"\n"+str(i.Post_name)+"さんの順位は"+str(int(i.Post_juni))+"位でした！！！"
                    result_ranking=str(int(i.Post_juni))
                    result_element=i.Post_element
                    if ranking_page.int_or_float == False:
                        result_element = int(result_element)
                    result_hensati=i.Post_hensati
                    break
        Pform = Post_rankForm
        Cform = Post_comentForm
        return render(request, 'ranking/rankpaged.html', {'rankpage': ranking_page,'a':ranking_page_post,'post_coment':post_coment,'Cform':Cform,'result':result,'ranking_page_json': mark_safe(json.dumps(ranking_id)),'result_hensati':result_hensati,'result_ranking':result_ranking,'result_element':result_element,})


#########################ユーザーページ###############################

def userpage(request, user_id):
    userinfo = get_object_or_404(CustomUser,id=user_id)
    Createdranking=userinfo.Createduser.order_by('-id')[:5]
    Postedranking=userinfo.Posteduser.order_by('-id')[:5]

    return render(request, 'ranking/userpage.html', {'userinfo':userinfo,'Createdranking':Createdranking,'Postedranking':Postedranking})

class Posted_ranking_user(generic.ListView):
    model=Post_rank
    template_name = 'ranking/Posted_ranking_user.html'
    paginate_by = 10
    ordering = ('-id')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article_list=set()
        if self.request.user.username:
            article_list = Post_rank.objects.filter(Posteduser=self.request.user).values_list('article', flat=True)
            article_list = set(article_list)#表示するランキングが少ない場合、setにしてもその恩恵がとても少ないので、5以上にはするようにしてください。
        context['article_set'] =  article_list
        #context['article_set_type'] = type(article_list)#セットの型になっているか確認。
        return context
    def get_queryset(self):
        queryset = Post_rank.objects.order_by('-id')
        userinfo = get_object_or_404(CustomUser,pk=self.kwargs['pk'])
        return super().get_queryset().filter(Posteduser=userinfo.id)

class Created_ranking_user(generic.ListView):
    model=create_ranking
    template_name = 'ranking/Created_ranking_user.html'
    paginate_by = 10
    ordering = ('-id')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article_list=set()
        if self.request.user.username:
            article_list = Post_rank.objects.filter(Posteduser=self.request.user).values_list('article', flat=True)
            article_list = set(article_list)#表示するランキングが少ない場合、setにしてもその恩恵がとても少ないので、5以上にはするようにしてください。
        context['article_set'] =  article_list
        #context['article_set_type'] = type(article_list)#セットの型になっているか確認。
        return context
    def get_queryset(self):
        queryset = create_ranking.objects.order_by('-id')
        userinfo = get_object_or_404(CustomUser,pk=self.kwargs['pk'])
        return super().get_queryset().filter(Createduser=userinfo.id)

def user_edit(request):
    if request.method == "POST":
        userinfo = get_object_or_404(CustomUser,id=request.user.id)
        cp = request.POST.copy()
        userinfo.biography=cp["biography"]
        #userinfoに入るのはCustomuserという型である。
        #.nameみたいな形で引き渡せる
        userinfo.save()
        return redirect('ranking:userpage',user_id=request.user.id)

    else:
        userinfo = get_object_or_404(CustomUser,id=request.user.id)
        return render(request, 'ranking/user_edit.html', {'userinfo':userinfo,})

def user_edit_result(request):
    return render(request, 'ranking/user_edit_result.html', {})


from django.views.decorators.http import require_POST


def aboutpage(request):
    return render(request, 'ranking/aboutpage.html', {})

def TermsofUse(request):
    return render(request, 'ranking/TermsofUse.html', {})



###　削除ボタン処理です。####
@require_POST
def delete_ranking(request, ranking_id):
    ranking_page = get_object_or_404(create_ranking, id = ranking_id)
    ranking_page.delete()
    # return redirect('ranking:Created_ranking_user', id = request.user.id)
    return redirect(request.META['HTTP_REFERER'])
