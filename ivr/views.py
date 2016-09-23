from django.http import HttpResponse
from django.views.generic import View
from .models import IVR_Call,Call_Forward
from .options import Session
from management.models import HelperCategory,HelpLine
import kookoo,requests,json

# Create your views here.

class IVR(View):
    def post_data(self,url, data):
        base_url = "http://safestreet.cse.iitb.ac.in:9000/"
        authentication = ("raj", "r@j2331992")
        headers = {'Content-type': 'application/json',}
        r = requests.post(base_url + url, data=json.dumps(data), headers=headers, auth=authentication)

    def get(self,request):
        r = kookoo.Response()
        sid = request.GET.get("sid")
        try:
            call = IVR_Call.objects.get(sid=sid)
            session_next = int(call.session_next)
        except:
            pass
        if request.GET.get("event")=="NewCall":
            caller_no = request.GET.get("cid")
            helpline_no = request.GET.get("called_number")
            caller_location = request.GET.get("circle")
            call_forward = Call_Forward.objects.filter(helper_no=caller_no)
            if call_forward:
                r.Dial(phoneno=call_forward[0].caller_no)
                session_next = Session.CALL_FORWARD
            else:
                session_next = Session.WELCOME
                call = IVR_Call(sid=sid,caller_no=caller_no,helpline_no=helpline_no,caller_location=caller_location,session_next=session_next)
                call.save()
        if session_next==Session.WELCOME:
            helpline = HelpLine.objects.get(helpline_number = helpline_no)
            r.addPlayText("Welcome to "+helpline.name+" Helpline")
            call.session_next = Session.DISPLAY_OPTION
            call.save()
        if session_next==Session.DISPLAY_OPTION:
            g = r.append(kookoo.CollectDtmf(maxDigits=1,timeout=5000))
            helpline = HelpLine.objects.get(helpline_number=call.helpline_no)
            help_cats = HelperCategory.objects.filter(helpline=helpline)
            idx=1;
            for help_cat in help_cats:
                g.append(kookoo.PlayText("Press "+str(idx)+" for"+help_cat.name))
                idx+=1
            call.session_next = Session.GET_OPTION
            call.save()
        if request.GET.get("event")=="GotDTMF" and session_next==Session.GET_OPTION:
            if len(request.GET.get("data"))!=0:
                call.category_option = request.GET.get("data")
                call.session_next = Session.CALL_EXIT
                call.save()
                data = {
                    "client_number":call.caller_no,
                    "helpline_number":call.helpline_no,
                    "location":call.caller_location,
                    "category":call.category_option
                }
                self.post_data("registercall/", data)
                helpline = HelpLine.objects.get(helpline_number=call.helpline_no)
                r.addPlayText("Thank You for calling " + helpline.name + " Helpline.")
                r.addHangup()
            else:
                call.session_next = Session.DISPLAY_OPTION
                call.save()
        if request.GET.get("event")=="Dial" and session_next==Session.CALL_FORWARD:
            if request.GET.get("status")=="not_answered":
                r.addHangup()
            else:
                r.addHangup()
        return HttpResponse(r)


