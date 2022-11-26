from django.db import models
from django.conf import settings
from userAccount.models import CustomUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.contrib.auth import get_user_model

class create_ranking(models.Model):
    title = models.CharField("タイトル",blank=False, null=False, max_length=150)
    element =models.CharField("要素",blank=False, null=False,max_length=8)
    description = models.TextField("説明",blank=False, null=False,)
    coment_count= models.IntegerField("コメント数",default=0)
    post_count= models.IntegerField("参加数",default=0)
    ranking_updated_at = models.DateTimeField("更新日",auto_now=True)
    int_or_float = models.BooleanField(verbose_name='小数値を適用',default=True,)
    #int_or_floatは、True時小数です。False時整数で保存されます。
    #使用用途しては、対象のランクページのint_or_floatがTrueなのかFalseなのかで判別します。
    #また、投稿ページでの型を設定しておきます。intなのかfloatなのか。
    up_or_down = models.BooleanField(verbose_name='昇順にする。',default=False,)
    #False時降順とする。
    max_number = models.IntegerField("最大値",default=1000000)
    min_number = models.IntegerField("最小値",default=0)
    Createduser = models.ForeignKey(to=CustomUser, verbose_name='ユーザー',related_name='Createduser', on_delete=models.PROTECT)
    Done_ranking = models.BooleanField(verbose_name='1000到達',default=False)
    #Posttoranking = models.ForeignKey(to=Post_rank, related_name='Posttoranking', on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class Post_rank(models.Model):
    Post_name = models.CharField("投稿者",blank=False, null=False, max_length=50)
    Post_element =models.FloatField("要素",blank=False, null=False)
    Post_juni = models.IntegerField("順位",default=0)
    Post_hensati = models.FloatField("偏差値",default=50)
    article = models.ForeignKey(to=create_ranking, related_name='Posts', on_delete=models.CASCADE)
    Posteduser = models.ForeignKey(to=CustomUser, verbose_name='投稿ユーザー',related_name='Posteduser', on_delete=models.PROTECT,blank=True,null=True)
    def __str__(self):
        return str(self.Post_name+" "+str(self.Post_element))

class Post_coment(models.Model):
    Post_coment_name = models.CharField("投稿者",blank=False, null=False, max_length=50)
    Post_coment_text =models.TextField("コメント",blank=False, null=False,max_length=300)
    article = models.ForeignKey(to=create_ranking, related_name='Posts_coment', on_delete=models.CASCADE)
    def __str__(self):
        return self.Post_coment_name
