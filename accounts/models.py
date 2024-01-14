from typing import Iterable, Optional
from django.db import models
from base.models import *
from django.contrib.auth.models import User 
# Create your models here.
class Profile(BaseModel):
    user=models.OneToOneField(User,related_name="profile",on_delete=models.CASCADE)
    profile_img=models.ImageField(upload_to='accounts')
    is_teacher=models.BooleanField(default=False)
    is_student=models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user.username

    def get_membership_count(self):
        return self.std.count()
    def is_clubmember(self):
        dict={}
        i=0
        for x in self.std.all():
            print(x.club)
            dict[i]=x.club
            i+=1
        return dict