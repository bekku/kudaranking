from django.forms import ModelForm
from .models import create_ranking,Post_rank,Post_coment

class create_rankingForm(ModelForm):
    class Meta:
        model = create_ranking
        fields = ['title', 'element','description','max_number','min_number','up_or_down','int_or_float']

        # def reverse_max_min(self):
        #     max_n = self.cleaned_data.get('max_number')
        #     min_n = self.cleaned_data.get('min_number')
        #     if max_n<=min_n:
        #         # self.add_error('max_number', '最大値と最小値が矛盾しています。')
        #         raise forms.ValidationError('最大値と最小値が矛盾しています。')
        #     return max_n
    #
    # def clean_NGword(self):
    #     super(create_rankingForm, self).clean()
    #     NG_or_OK_title = self.cleaned_data.get('title')
    #     NG_or_OK_element = self.cleaned_data.get('element')
    #     NG_or_OK_discription = self.cleaned_data.get('description')

        # NG_word_set = set(["殺す","殺害","爆破","死ぬ","自殺","http:","https:"])
        # for NG_word in NG_word_set:
        #     if (NG_word in NG_or_OK_title) or (NG_word in NG_or_OK_element) or (NG_word in NG_or_OK_discription):
        #         raise forms.ValidationError("NGワードが含まれています。")


class Post_rankForm(ModelForm):
    class Meta:
        model = Post_rank
        fields = ['Post_name', 'Post_element']

    def clean_NGword(self):
        super(Post_rankForm, self).clean()
        NG_or_OK_rank_element = self.cleaned_data.get('Post_element')
        NG_or_OK_rank_name = self.cleaned_data.get('Post_name')

        # NG_word_set = set(["殺す","殺害","爆破","死ぬ","自殺","http:","https:"])
        # for NG_word in NG_word_set:
        #     if (NG_word in NG_or_OK_rank_element) or (NG_word in NG_or_OK_rank_name):
        #         raise forms.ValidationError("NGワードが含まれています。")


class Post_comentForm(ModelForm):
    class Meta:
        model = Post_coment
        fields = ['Post_coment_name', 'Post_coment_text']

    # def clean_NGword(self):
    #     super(Post_comentForm, self).clean()
    #     NG_or_OK_coment_element = self.cleaned_data.get('Post_coment_text')
    #     NG_or_OK_coment_name = self.cleaned_data.get('Post_coment_name')
    #
    #     NG_word_set = set(["殺す","殺害","爆破","死ぬ","自殺","http:","https:"])
    #     for NG_word in NG_word_set:
    #         if (NG_word in NG_or_OK_coment_element) or (NG_word in NG_or_OK_coment_name):
    #             raise forms.ValidationError("NGワードが含まれています。")
