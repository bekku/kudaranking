from django.db import models

class comenting(models.Model):
    coment_text = models.TextField("コメント", max_length=150)
    coment_room_name=models.TextField("ルーム名", max_length=150,default='a')
    def __str__(self):
        return self.coment_text
