from django.db import models
from base.models import *
from accounts.models import *
# Create your models here.
class Club(BaseModel):
    club_name=models.CharField(max_length=100)
    club_desc=models.TextField(null=True)
    club_img=models.ImageField(upload_to="club")
    teacher_cordinator=models.OneToOneField(Profile,related_name="teacher",on_delete=models.SET_NULL,null=True,blank=True)
    def __str__(self) -> str:
        return self.club_name
    def get_stdc_count(self):
        return ClubMember.objects.filter(club=self,is_cordinator=True).count()
    def get_request_count(self):
        return ClubMember.objects.filter(club=self,request=True).count()
    def check_member(self,request):
        print("y")
        if ClubMember.objects.filter(club=self,member=request.user).exists():
            return True
        else:
            return False
    
class ClubChat(BaseModel):
    club=models.ForeignKey(Club,related_name="clubchat",on_delete=models.CASCADE)
    user=models.ForeignKey(Profile,related_name="clubmem",on_delete=models.CASCADE)
    comment=models.CharField(max_length=1000)

    def __str__(self) -> str:
        return self.user.user.username+"("+(self.comment)+")"
    
class ClubMember(BaseModel):
    club=models.ForeignKey(Club,related_name="member",on_delete=models.CASCADE)
    member=models.ForeignKey(Profile,related_name="std",on_delete=models.CASCADE)
    is_cordinator=models.BooleanField(default=False)
    head=models.BooleanField(default=False)
    request=models.BooleanField(default=False)
    def __str__(self) -> str:
        return self.member.user.username

class ClubElections(BaseModel):
    club=models.OneToOneField(Club,related_name="election",on_delete=models.CASCADE)
    voting=models.BooleanField(default=False)
    def __str__(self) -> str:
        return self.club.club_name

class Candidate(BaseModel):
    election=models.ForeignKey(ClubElections,related_name="candidate",on_delete=models.CASCADE)
    candidate=models.OneToOneField(ClubMember,related_name="stdcand",on_delete=models.CASCADE)
    count=models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.candidate.member.user.username

class Voter(BaseModel):
    voter=models.ForeignKey(ClubMember,related_name='voter',on_delete=models.CASCADE)
    election=models.ForeignKey(ClubElections,related_name="votedfor",on_delete=models.CASCADE)
    has_voted=models.BooleanField(default=False)