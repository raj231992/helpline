from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from task_manager.models import Assign
from register_helper.models import Helper
from management.models import HelperCategory
from ivr.models import Call_Forward_Details
from registercall.models import Task
# Create your views here.

class Home(LoginRequiredMixin,View):
    login_url = '/web_auth/login/'
    redirect_field_name = 'redirect_to'
    def get(self,request):
        user = request.user
        helper = Helper.objects.filter(user=user)
        pending_users = None
        helpers = None
        if helper:
            assigns = Assign.objects.filter(helper__helpline=helper[0].helpline).order_by('-id')
            helpers = Helper.objects.filter(helpline=helper[0].helpline).exclude(login_status=3)
            pending_users = Helper.objects.filter(helpline=helper[0].helpline,login_status=3)
            for assign in assigns:
                print assign.helper.helpline
            pending = 0
            completed = 0
            rejected = 0
            total = 0
            for assign in assigns:
                if assign.action.task.status == 1:
                    pending += 1
                elif assign.action.task.status == 2:
                    completed += 1
                elif assign.action.task.status == 3:
                    rejected += 1
                total += 1
        else:
            assigns = Assign.objects.all().order_by('-id')
            helpers = Helper.objects.all().order_by('-id')
            pending_users = Helper.objects.filter(login_status=3)
            pending = 0
            completed = 0
            rejected = 0
            total = 0
            for assign in assigns:
                if assign.action.task.status==1:
                    pending+=1
                elif assign.action.task.status==2:
                    completed+=1
                elif assign.action.task.status == 3:
                    rejected += 1
                total+=1
        context = {
            'assigns': assigns,
            'pending': pending,
            'completed': completed,
            'rejected': rejected,
            'total': total,
            'helpers': helpers,
            'pending_users':pending_users,
        }
        return render(request,'dashboard.html',context)

class Helper_Profile(LoginRequiredMixin,View):
    login_url = '/web_auth/login/'
    redirect_field_name = 'redirect_to'
    def get(self,request,pk,year,cat):
        helper = Helper.objects.get(pk=pk)
        if cat!='All':
            assigns = Assign.objects.filter(created__year=year,helper=helper,action__task__category__name=cat)
        else:
            assigns = Assign.objects.filter(created__year=year,helper=helper)
        helper_cats = HelperCategory.objects.exclude(name='Repeat')
        pen_jan,pen_feb,pen_mar,pen_apr,pen_may,pen_jun,pen_jul,pen_aug,pen_sep,pen_oct,pen_nov,pen_dec=0,0,0,0,0,0,0,0,0,0,0,0
        com_jan, com_feb, com_mar, com_apr, com_may, com_jun, com_jul, com_aug, com_sep, com_oct, com_nov, com_dec = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        rej_jan, rej_feb, rej_mar, rej_apr, rej_may, rej_jun, rej_jul, rej_aug, rej_sep, rej_oct, rej_nov, rej_dec = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

        for assign in assigns:
            if assign.created.month == 1:
                if assign.action.task.status == 1:
                    pen_jan+=1
                elif assign.action.task.status == 2:
                    com_jan += 1
                elif assign.action.task.status == 3:
                    rej_jan += 1
            elif assign.created.month == 2:
                if assign.action.task.status == 1:
                    pen_feb += 1
                elif assign.action.task.status == 2:
                    com_feb += 1
                elif assign.action.task.status == 3:
                    rej_feb += 1
            elif assign.created.month == 3:
                if assign.action.task.status == 1:
                    pen_mar += 1
                elif assign.action.task.status == 2:
                    com_mar += 1
                elif assign.action.task.status == 3:
                    rej_mar += 1
            elif assign.created.month == 4:
                if assign.action.task.status == 1:
                    pen_apr += 1
                elif assign.action.task.status == 2:
                    com_apr += 1
                elif assign.action.task.status == 3:
                    rej_apr += 1
            elif assign.created.month == 5:
                if assign.action.task.status == 1:
                    pen_may += 1
                elif assign.action.task.status == 2:
                    com_may += 1
                elif assign.action.task.status == 3:
                    rej_may += 1
            elif assign.created.month == 6:
                if assign.action.task.status == 1:
                    pen_jun += 1
                elif assign.action.task.status == 2:
                    com_jun += 1
                elif assign.action.task.status == 3:
                    rej_jun += 1
            elif assign.created.month == 7:
                if assign.action.task.status == 1:
                    pen_jul += 1
                elif assign.action.task.status == 2:
                    com_jul += 1
                elif assign.action.task.status == 3:
                    rej_jul += 1
            elif assign.created.month == 8:
                if assign.action.task.status == 1:
                    pen_aug += 1
                elif assign.action.task.status == 2:
                    com_aug += 1
                elif assign.action.task.status == 3:
                    rej_aug += 1
            elif assign.created.month == 9:
                if assign.action.task.status == 1:
                    pen_sep += 1
                elif assign.action.task.status == 2:
                    com_sep += 1
                elif assign.action.task.status == 3:
                    rej_sep += 1
            elif assign.created.month == 10:
                if assign.action.task.status == 1:
                    pen_oct += 1
                elif assign.action.task.status == 2:
                    com_oct += 1
                elif assign.action.task.status == 3:
                    rej_oct += 1
            elif assign.created.month == 11:
                if assign.action.task.status == 1:
                    pen_nov += 1
                elif assign.action.task.status == 2:
                    com_nov += 1
                elif assign.action.task.status == 3:
                    rej_nov += 1
            elif assign.created.month == 12:
                if assign.action.task.status == 1:
                    pen_dec += 1
                elif assign.action.task.status == 2:
                    com_dec += 1
                elif assign.action.task.status == 3:
                    rej_dec += 1

        assigns = Assign.objects.filter(helper=helper)
        years = set()
        for assign in assigns:
            years.add(assign.created.year)

        context = {
            'pk' : pk,
            'helper_first_name' : helper.user.first_name,
            'helper_last_name' : helper.user.last_name,
            'helper_cats': helper_cats,
            'helper':helper,
            'assigns':assigns,
            'cur_cat':cat,
            'years' : years,
            'cur_year': year,
            'pen_jan' : pen_jan,
            'pen_feb' : pen_feb,
            'pen_mar' : pen_mar,
            'pen_apr' : pen_apr,
            'pen_may' : pen_may,
            'pen_jun' : pen_jun,
            'pen_jul' : pen_jul,
            'pen_aug' : pen_aug,
            'pen_sep' : pen_sep,
            'pen_oct' : pen_oct,
            'pen_nov' : pen_nov,
            'pen_dec' : pen_dec,
            'com_jan' : com_jan,
            'com_feb' : com_feb,
            'com_mar' : com_mar,
            'com_apr' : com_apr,
            'com_may' : com_may,
            'com_jun' : com_jun,
            'com_jul' : com_jul,
            'com_aug' : com_aug,
            'com_sep' : com_sep,
            'com_oct' : com_oct,
            'com_nov' : com_nov,
            'com_dec' : com_dec,
            'rej_jan' : rej_jan,
            'rej_feb' : rej_feb,
            'rej_mar' : rej_mar,
            'rej_apr' : rej_apr,
            'rej_may' : rej_may,
            'rej_jun' : rej_jun,
            'rej_jul' : rej_jul,
            'rej_aug' : rej_aug,
            'rej_sep' : rej_sep,
            'rej_oct' : rej_oct,
            'rej_nov' : rej_nov,
            'rej_dec' : rej_dec,
        }
        return render(request,'helper_profile.html',context)

class Yearly_Stats(LoginRequiredMixin,View):
    login_url = '/web_auth/login/'
    redirect_field_name = 'redirect_to'
    def get(self,request,cat,year):
        user = request.user
        helper = Helper.objects.filter(user=user)
        if cat!= 'All':
            assigns = Assign.objects.filter(created__year=year,action__task__category__name=cat,action__task__call_request__helpline=helper[0].helpline)
        else:
            assigns = Assign.objects.filter(created__year=year,action__task__call_request__helpline=helper[0].helpline)
        helper_cats = HelperCategory.objects.exclude(name='Repeat')
        pen_jan,pen_feb,pen_mar,pen_apr,pen_may,pen_jun,pen_jul,pen_aug,pen_sep,pen_oct,pen_nov,pen_dec=0,0,0,0,0,0,0,0,0,0,0,0
        com_jan, com_feb, com_mar, com_apr, com_may, com_jun, com_jul, com_aug, com_sep, com_oct, com_nov, com_dec = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        rej_jan, rej_feb, rej_mar, rej_apr, rej_may, rej_jun, rej_jul, rej_aug, rej_sep, rej_oct, rej_nov, rej_dec = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

        for assign in assigns:
            if assign.created.month == 1:
                if assign.action.task.status == 1:
                    pen_jan+=1
                elif assign.action.task.status == 2:
                    com_jan += 1
                elif assign.action.task.status == 3:
                    rej_jan += 1
            elif assign.created.month == 2:
                if assign.action.task.status == 1:
                    pen_feb += 1
                elif assign.action.task.status == 2:
                    com_feb += 1
                elif assign.action.task.status == 3:
                    rej_feb += 1
            elif assign.created.month == 3:
                if assign.action.task.status == 1:
                    pen_mar += 1
                elif assign.action.task.status == 2:
                    com_mar += 1
                elif assign.action.task.status == 3:
                    rej_mar += 1
            elif assign.created.month == 4:
                if assign.action.task.status == 1:
                    pen_apr += 1
                elif assign.action.task.status == 2:
                    com_apr += 1
                elif assign.action.task.status == 3:
                    rej_apr += 1
            elif assign.created.month == 5:
                if assign.action.task.status == 1:
                    pen_may += 1
                elif assign.action.task.status == 2:
                    com_may += 1
                elif assign.action.task.status == 3:
                    rej_may += 1
            elif assign.created.month == 6:
                if assign.action.task.status == 1:
                    pen_jun += 1
                elif assign.action.task.status == 2:
                    com_jun += 1
                elif assign.action.task.status == 3:
                    rej_jun += 1
            elif assign.created.month == 7:
                if assign.action.task.status == 1:
                    pen_jul += 1
                elif assign.action.task.status == 2:
                    com_jul += 1
                elif assign.action.task.status == 3:
                    rej_jul += 1
            elif assign.created.month == 8:
                if assign.action.task.status == 1:
                    pen_aug += 1
                elif assign.action.task.status == 2:
                    com_aug += 1
                elif assign.action.task.status == 3:
                    rej_aug += 1
            elif assign.created.month == 9:
                if assign.action.task.status == 1:
                    pen_sep += 1
                elif assign.action.task.status == 2:
                    com_sep += 1
                elif assign.action.task.status == 3:
                    rej_sep += 1
            elif assign.created.month == 10:
                if assign.action.task.status == 1:
                    pen_oct += 1
                elif assign.action.task.status == 2:
                    com_oct += 1
                elif assign.action.task.status == 3:
                    rej_oct += 1
            elif assign.created.month == 11:
                if assign.action.task.status == 1:
                    pen_nov += 1
                elif assign.action.task.status == 2:
                    com_nov += 1
                elif assign.action.task.status == 3:
                    rej_nov += 1
            elif assign.created.month == 12:
                if assign.action.task.status == 1:
                    pen_dec += 1
                elif assign.action.task.status == 2:
                    com_dec += 1
                elif assign.action.task.status == 3:
                    rej_dec += 1

        assigns = Assign.objects.filter(action__task__call_request__helpline=helper[0].helpline)
        years = set()
        for assign in assigns:
            years.add(assign.created.year)
        categories = HelperCategory.objects.filter(helpline=helper[0].helpline)

        cat_count = []

        for cata in categories:
            cat_count.append(len(
                Assign.objects.filter(created__year=year, action__task__category__name=cata,
                                      action__task__call_request__helpline=helper[0].helpline)))
        context = {
            'years' : years,
            'helper_cats' : helper_cats,
            'cur_year': year,
            'cur_cat' : cat,
            'cat_count' : cat_count,
            'pen_jan' : pen_jan,
            'pen_feb' : pen_feb,
            'pen_mar' : pen_mar,
            'pen_apr' : pen_apr,
            'pen_may' : pen_may,
            'pen_jun' : pen_jun,
            'pen_jul' : pen_jul,
            'pen_aug' : pen_aug,
            'pen_sep' : pen_sep,
            'pen_oct' : pen_oct,
            'pen_nov' : pen_nov,
            'pen_dec' : pen_dec,
            'com_jan' : com_jan,
            'com_feb' : com_feb,
            'com_mar' : com_mar,
            'com_apr' : com_apr,
            'com_may' : com_may,
            'com_jun' : com_jun,
            'com_jul' : com_jul,
            'com_aug' : com_aug,
            'com_sep' : com_sep,
            'com_oct' : com_oct,
            'com_nov' : com_nov,
            'com_dec' : com_dec,
            'rej_jan' : rej_jan,
            'rej_feb' : rej_feb,
            'rej_mar' : rej_mar,
            'rej_apr' : rej_apr,
            'rej_may' : rej_may,
            'rej_jun' : rej_jun,
            'rej_jul' : rej_jul,
            'rej_aug' : rej_aug,
            'rej_sep' : rej_sep,
            'rej_oct' : rej_oct,
            'rej_nov' : rej_nov,
            'rej_dec' : rej_dec,
        }
        return render(request,'stats_year.html',context)

class Monthly_Stats(LoginRequiredMixin,View):
    login_url = '/web_auth/login/'
    redirect_field_name = 'redirect_to'
    def get(self,request,cat,month,year):
        user = request.user
        helper = Helper.objects.filter(user=user)
        if month=='Jan':
            cur_month=1
        elif month=='Feb':
            cur_month=2
        elif month == 'Mar':
            cur_month = 3
        elif month == 'Apr':
            cur_month = 4
        elif month == 'May':
            cur_month = 5
        elif month == 'Jun':
            cur_month = 6
        elif month == 'Jul':
            cur_month = 7
        elif month == 'Aug':
            cur_month = 8
        elif month == 'Sep':
            cur_month = 9
        elif month == 'Oct':
            cur_month = 10
        elif month == 'Nov':
            cur_month = 11
        elif month == 'Dec':
            cur_month = 12
        if cat!= 'All':
            assigns = Assign.objects.filter(created__month=cur_month,created__year=year,action__task__category__name=cat,action__task__call_request__helpline=helper[0].helpline)
        else:
            assigns = Assign.objects.filter(created__month=cur_month,created__year=year,action__task__call_request__helpline=helper[0].helpline)
        helper_cats = HelperCategory.objects.exclude(name='Repeat')
        pen_week1,pen_week2,pen_week3,pen_week4,pen_week5=0,0,0,0,0
        com_week1, com_week2, com_week3, com_week4, com_week5 = 0, 0, 0, 0, 0
        rej_week1, rej_week2, rej_week3, rej_week4, rej_week5 = 0, 0, 0, 0, 0

        for assign in assigns:
            if (assign.created.day-1)/7 == 0:
                if assign.action.task.status == 1:
                    pen_week1+=1
                elif assign.action.task.status == 2:
                    com_week1 += 1
                elif assign.action.task.status == 3:
                    rej_week1 += 1
            elif (assign.created.day-1)/7 == 1:
                if assign.action.task.status == 1:
                    pen_week2 += 1
                elif assign.action.task.status == 2:
                    com_week2 += 1
                elif assign.action.task.status == 3:
                    rej_week2 += 1
            elif (assign.created.day - 1) / 7 == 2:
                if assign.action.task.status == 1:
                    pen_week3 += 1
                elif assign.action.task.status == 2:
                    com_week3 += 1
                elif assign.action.task.status == 3:
                    rej_week3 += 1
            elif (assign.created.day - 1) / 7 == 3:
                if assign.action.task.status == 1:
                    pen_week4 += 1
                elif assign.action.task.status == 2:
                    com_week4 += 1
                elif assign.action.task.status == 3:
                    rej_week4 += 1
            elif (assign.created.day - 1) / 7 == 4:
                if assign.action.task.status == 1:
                    pen_week5 += 1
                elif assign.action.task.status == 2:
                    com_week5 += 1
                elif assign.action.task.status == 3:
                    rej_week5 += 1


        assigns = Assign.objects.filter(action__task__call_request__helpline=helper[0].helpline)
        years = set()
        for assign in assigns:
            years.add(assign.created.year)

        categories = HelperCategory.objects.filter(helpline=helper[0].helpline)

        cat_count=[]

        for cata in categories:
            cat_count.append(len(Assign.objects.filter(created__month=cur_month, created__year=year, action__task__category__name=cata,
                                                       action__task__call_request__helpline=helper[0].helpline)))

        context = {
            'years' : years,
            'helper_cats' : helper_cats,
            'cur_year': year,
            'cur_month': month,
            'cur_cat' : cat,
            'cat_count' : cat_count,
            'pen_week1' : pen_week1,
            'pen_week2' : pen_week2,
            'pen_week3' : pen_week3,
            'pen_week4' : pen_week4,
            'pen_week5' : pen_week5,
            'com_week1' : com_week1,
            'com_week2' : com_week2,
            'com_week3' : com_week3,
            'com_week4' : com_week4,
            'com_week5' : com_week5,
            'rej_week1' : rej_week1,
            'rej_week2' : rej_week2,
            'rej_week3' : rej_week3,
            'rej_week4' : rej_week4,
            'rej_week5' : rej_week5,
        }
        return render(request,'stats_month.html',context)
class Task_Details(LoginRequiredMixin,View):
    login_url = '/web_auth/login/'
    redirect_field_name = 'redirect_to'
    def get(self,request,pk):
        task = Task.objects.get(id=pk)
        call_forward = Call_Forward_Details.objects.filter(task=task)
        return render(request,'task_details.html',{'call_forward':call_forward})