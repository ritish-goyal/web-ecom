from django.shortcuts import render,redirect,resolve_url
from django.http import HttpResponse
from .models import *
from django.views import generic
from django.contrib.auth import mixins
from django.contrib import messages
# Create your views here.
class Home(mixins.LoginRequiredMixin,generic.ListView):
    login_url='/accounts/login/'
    template_name="clubs/home.html"
    model=Club
    context_object_name='clubs'
    queryset=Club.objects.all()
    
class Clubs(mixins.LoginRequiredMixin,generic.ListView):
    login_url='/accounts/login/'
    template_name="clubs/clubs.html"
    model=Club
    context_object_name='clubs'
    queryset=Club.objects.all()
    def join_club(request,id):
        if not (request.user.is_superuser or request.user.profile.is_teacher or request.user.profile.get_membership_count() >= 2):
            ClubMember.objects.create(
                club=Club.objects.get(id=id),
                member=Profile.objects.get(user=request.user)
            )
        else:
            messages.warning(request,"Only students are allowed to join Club")
        return redirect('/')
    def start_elections(request,id):
        if request.user.profile.is_teacher and Club.objects.get(teacher_cordinator=Profile.objects.get(user=request.user)):
            ClubElections.objects.create(
                club=Club.objects.get(id=id),
            )
            return redirect('/club-view/'+id)
    def start_voting(request,id):
        if Club.objects.get(teacher_cordinator=Profile.objects.get(user=request.user)) and Candidate.objects.filter(election=ClubElections.objects.get(club=Club.objects.get(id=id))).count() >= 1:
            obj=ClubElections.objects.get(club=Club.objects.get(id=id))
            obj.voting=True
            obj.save()
            messages.success(request,"Voting started")
            return redirect('/club-view/'+id)
        else:
            messages.warning(request,"not even 1 nominie is there")
            return redirect('/club-view/'+id)
    def stop_voting(request,id):
        if Club.objects.get(teacher_cordinator=Profile.objects.get(user=request.user)):
            obj=ClubElections.objects.get(club=Club.objects.get(id=id))
            cobj=Candidate.objects.filter(election=ClubElections.objects.get(club=Club.objects.get(id=id)))
            print(cobj)
            count=cobj[0].count
            for x in cobj:
                if count<x.count:
                    count=x.count
                    print(count)         
            print(ClubMember.objects.filter(club=Club.objects.get(id=id),head=True))
            # ClubMember.objects.filter(club=Club.objects.get(id=id),head=True)[0].head=False
            sobj=ClubMember.objects.filter(stdcand__count=count)[0]
            
            if not ClubMember.objects.filter(member=sobj.member,head=True).exists():
                sobj.head=True
                sobj.save()
            else:
                sobj=ClubMember.objects.filter(stdcand__count=count)[1]
                if not ClubMember.objects.filter(member=sobj.member,head=True).exists():
                    sobj.head=True
                    sobj.save()
                else:
                    messages.warning(request,"Already head")
                    return redirect('/club-view/'+id)
            cobj.delete()
            obj.delete()
            return redirect('/club-view/'+id)
            
    def nominate(request,id):
        obj1=Club.objects.get(id=id)
        obj2=ClubMember.objects.get(club=obj1,member__user=request.user)
        if not obj1.election.voting and obj2.is_cordinator:
           Candidate.objects.create(
                election=ClubElections.objects.get(club=Club.objects.get(id=id)),
                candidate=ClubMember.objects.get(member=Profile.objects.get(user=request.user),club=Club.objects.get(id=id))
                )
           messages.success(request,"You are nominated successfuly")
           return redirect('/club-view/'+id)
        else:
            messages.success(request,"You are already nominated or not eligible")
            return redirect('/club-view/'+id)
    def Vote(request,id):
        obj1=ClubElections.objects.get(candidate__id=id).club
        
        if ClubMember.objects.filter(member__user__username=request.user,club=obj1).exists():
            vobj=Voter.objects.filter(election__club=obj1,voter__member=Profile.objects.get(user=request.user))
            if not vobj.exists():
                obj=Candidate.objects.get(
                    id=id
                )
                obj.count+=1
                obj.save()
                Voter.objects.create(
                    voter=ClubMember.objects.filter(member=Profile.objects.get(user=request.user))[0],
                    election=ClubElections.objects.get(candidate__id=id),
                    has_voted=True,
                )
                messages.success(request,"Voted Succesfully")
                return redirect('/club-view/'+str(obj1.id))
            else:
                messages.warning(request,"you have already voted")
                return redirect('/club-view/'+str(obj1.id))
        else:
            messages.warning(request,"you can't vote in this election")
            return redirect('/club-view/'+str(obj1.id))
        
class add_club(mixins.LoginRequiredMixin,generic.CreateView):
    login_url='/accounts/login/'
    template_name="clubs/add_club.html"
    model=Club
    fields=['club_name','club_desc','club_img']
    success_url='/clubs/'

class club_view(generic.DetailView):
    model=Club
    template_name='clubs/clubview.html'
    context_object_name='club'
    def club_chat(request,id):
            if request.method=="POST":
                comment=request.POST.get("comment")
                ClubChat.objects.create(
                    comment=comment,
                    club=Club.objects.filter(id=id)[0],
                    
                    user=Profile.objects.get(user=request.user)
                )
                return redirect('/club-view/'+id)
            
class add_stdc(mixins.LoginRequiredMixin,generic.DetailView):
    login_url='/accounts/login/'
    template_name="clubs/add_stc.html"
    context_object_name="club"
    model=Club
    def add(request,id):
        obj=ClubMember.objects.get(id=id)
        if not ClubMember.objects.filter(member=obj.member,is_cordinator=True).exists():
            print(ClubMember.objects.filter(member=obj.member,is_cordinator=True))
            obj.is_cordinator=True
            obj.request=False
            obj.save()
        else:
            messages.warning(request,"Alraedy cordinator of other club")
            return redirect('/addstdc/'+str(obj.club.id))
        
        return redirect('/addstdc/'+str(obj.club.id))
    def remove(request,id):
        obj=ClubMember.objects.filter(club__id=id)
        for x in obj:
            x.is_cordinator=False
            x.head=False
            x.save()
        return redirect('/club-view/'+id)
    def removesp(request,id):
        obj=ClubMember.objects.get(id=id)
        obj.is_cordinator=False
        obj.request=False
        obj.save()
        return redirect('/addstdc/'+str(obj.club.id))
    def request(request,id):
        obj=ClubMember.objects.get(member__user=request.user,club__id=id)
        if not ClubMember.objects.filter(member__user=request.user,is_cordinator=True).exists():
            obj.request=True
            obj.save()
        else:
            messages.warning(request,"You can be cordinator of only one club")
            return redirect('/club-view/'+id)
        return redirect('/club-view/'+id)
class vote(mixins.LoginRequiredMixin,generic.DetailView):
    login_url='/accounts/login/'
    template_name="clubs/elections.html"
    model=ClubElections
    context_object_name="elec"
