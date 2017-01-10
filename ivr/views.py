from django.http import HttpResponse
from django.views.generic import View
from .models import IVR_Call,Call_Forward,Misc_Audio,Misc_Category,IVR_Audio,Language
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
        audio_url = "http://safestreet.cse.iitb.ac.in/helpline"
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
                session_next = Session.CALL_FORWARD
                call = IVR_Call(sid=sid, caller_no=caller_no, helpline_no=helpline_no, caller_location=caller_location,
                                session_next=session_next)
                call.save()
                r.addDial(phoneno=call_forward[0].caller_no)
            else:
                session_next = Session.DISPLAY_LANGUAGE
                call = IVR_Call(sid=sid,caller_no=caller_no,helpline_no=helpline_no,caller_location=caller_location,session_next=session_next)
                call.save()

        if session_next == Session.DISPLAY_LANGUAGE:
            g = r.append(kookoo.CollectDtmf(maxDigits=1, timeout=5000))
            helpline = HelpLine.objects.get(helpline_number=call.helpline_no)
            audio_cat = Misc_Category.objects.get(category="Language")
            audio_objs = Misc_Audio.objects.filter(helpline=helpline,category=audio_cat)
            for audio_obj in audio_objs:
                print audio_url+audio_obj.audio.name
                g.append(kookoo.PlayAudio(url=audio_url+audio_obj.audio.name))
            call.session_next = Session.GET_LANGUAGE
            call.save()

        if request.GET.get("event") == "GotDTMF" and session_next == Session.GET_LANGUAGE:
            if len(request.GET.get("data")) != 0:
                call.language_option = request.GET.get("data")
                call.session_next = Session.WELCOME
                call.save()
            else:
                call.session_next = Session.DISPLAY_LANGUAGE
                call.save()

        if session_next==Session.WELCOME:
            helpline = HelpLine.objects.get(helpline_number = call.helpline_no)
            language = Language.objects.filter(helpline=helpline)[int(call.language_option)-1]
            audio_cat = Misc_Category.objects.get(category="Welcome")
            audio_obj = Misc_Audio.objects.get(helpline=helpline,category=audio_cat,language=language)
            r.addPlayAudio(url=audio_url+audio_obj.audio.name)
            call.session_next = Session.DISPLAY_OPTION
            call.save()

        if session_next==Session.DISPLAY_OPTION:
            g = r.append(kookoo.CollectDtmf(maxDigits=1,timeout=5000))
            helpline = HelpLine.objects.get(helpline_number=call.helpline_no)
            language = Language.objects.filter(helpline=helpline)[int(call.language_option) - 1]
            audio_obj = IVR_Audio.objects.get(helpline=helpline, language=language)
            for audio_obj in audio_objs:
                print audio_url+audio_obj.audio.name
                g.append(kookoo.PlayAudio(url=audio_url+audio_obj.audio.name))
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

            else:
                call.session_next = Session.DISPLAY_OPTION
                call.save()

        if session_next==Session.CALL_EXIT:
            helpline = HelpLine.objects.get(helpline_number = call.helpline_no)
            language = Language.objects.filter(helpline=helpline)[int(call.language_option)-1]
            audio_cat = Misc_Category.objects.get(category="Exit")
            audio_obj = Misc_Audio.objects.get(helpline=helpline,category=audio_cat,language=language)
            r.addPlayAudio(url=audio_url+audio_obj.audio.name)
            r.addHangup()

        if request.GET.get("event")=="Dial" and session_next==Session.CALL_FORWARD:
            caller_no = request.GET.get("cid")
            if request.GET.get("status")=="not_answered":
                call_forward = Call_Forward.objects.get(helper_no=caller_no)
                call_forward.delete()
                r.addHangup()
            else:
                call_forward = Call_Forward.objects.get(helper_no=caller_no)
                call_forward.delete()
                r.addHangup()
        return HttpResponse(r)


