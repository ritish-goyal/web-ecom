from django.urls import path
from .views import *

urlpatterns = [
    path('', Home.as_view(),name="Home"),
    path('clubs/', Clubs.as_view(),name="Club"),
    path('addclub/',add_club.as_view(),name="AddClub"),
    path('remstdc/<id>',add_stdc.remove,name="Remstdc"),
    path('addstdc/<pk>',add_stdc.as_view(),name="Addstdc"),
    path('reqc/<id>',add_stdc.request,name="Reqc"),
    path('add/<id>',add_stdc.add,name="add"),
    path('rem/<id>',add_stdc.removesp,name="rem"),
    path('club-view/<pk>',club_view.as_view(),name="ClubView"),
   path('club-chat/<id>',club_view.club_chat,name="ClubChat"),
   path('join/<id>',Clubs.join_club,name="ClubJoin"),
   path('elections/<id>',Clubs.start_elections,name="StartElections"),
   path('elections/voting/<id>',Clubs.start_voting,name="StartVoting"),
   path('elections/voting/stop/<id>',Clubs.stop_voting,name="StopVoting"),
   path('elections/voting/nominate/<id>',Clubs.nominate,name="Nominate"),
   path('elections/voting/vote/<id>',Clubs.Vote,name="Vote"),
   path('elections/voting/selectvote/<pk>',vote.as_view(),name="selectVote"),
]