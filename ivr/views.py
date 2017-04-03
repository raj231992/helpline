from django.http import HttpResponse
from django.views.generic import View
from .models import IVR_Call,Call_Forward,Misc_Audio,Misc_Category,IVR_Audio,Language,Call_Forward_Details
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
                caller_no_len = len(caller_no)
                caller_no = caller_no[caller_no_len - 10:]
                call = IVR_Call(sid=sid, caller_no = caller_no, helpline_no=helpline_no, caller_location=caller_location,
                                session_next=session_next)
                call.save()
                call_forward_details = Call_Forward_Details(helper_no=helpline_no,caller_no=caller_no)
                call_forward_details.save()
                r.addDial(phoneno=call_forward[0].caller_no)
                call_forward_details.status = 'completed'
                call_forward_details.save()
            else:
                session_next = Session.DISPLAY_LANGUAGE
                caller_no_len = len(caller_no)
                caller_no = caller_no[caller_no_len - 10:]
                call = IVR_Call(sid=sid,caller_no=caller_no,helpline_no=helpline_no,caller_location=caller_location,session_next=session_next)
                call.save()

        if session_next == Session.DISPLAY_LANGUAGE:
            g = r.append(kookoo.CollectDtmf(maxDigits=1, timeout=5000))
            helpline = HelpLine.objects.get(helpline_number=call.helpline_no)
            audio_cat = Misc_Category.objects.get(category="Language")
            audio_objs = Misc_Audio.objects.filter(helpline=helpline,category=audio_cat)
            for audio_obj in audio_objs:
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
            audio_objs = IVR_Audio.objects.filter(helpline=helpline, language=language)
            for audio_obj in audio_objs:
                g.append(kookoo.PlayAudio(url=audio_url+audio_obj.audio.name))
            call.session_next = Session.GET_OPTION
            call.save()

        if request.GET.get("event")=="GotDTMF" and session_next==Session.GET_OPTION:
            if len(request.GET.get("data"))!=0:
                call.category_option = request.GET.get("data")
                helpline = HelpLine.objects.get(helpline_number=call.helpline_no)
                language = Language.objects.filter(helpline=helpline)[int(call.language_option) - 1]
                tot_opts = str(len(IVR_Audio.objects.filter(language=language)))
                print tot_opts,call.category_option
                if call.category_option== tot_opts:
                    call.session_next = Session.DISPLAY_OPTION
                    call.save()
                else:
                    call.session_next = Session.DISPLAY_TERMS
                    call.save()

            else:
                call.session_next = Session.DISPLAY_OPTION
                call.save()

        if session_next == Session.DISPLAY_TERMS:
            g = r.append(kookoo.CollectDtmf(maxDigits=1, timeout=5000))
            helpline = HelpLine.objects.get(helpline_number=call.helpline_no)
            language = Language.objects.filter(helpline=helpline)[int(call.language_option) - 1]
            audio_cat = Misc_Category.objects.get(category="Terms")
            audio_obj = Misc_Audio.objects.get(helpline=helpline,category=audio_cat,language=language)
            g.append(kookoo.PlayAudio(url=audio_url+audio_obj.audio.name))
            call.session_next = Session.GET_TERMS
            call.save()

        if request.GET.get("event") == "GotDTMF" and session_next == Session.GET_TERMS:
            if len(request.GET.get("data")) != 0:
                terms_option = request.GET.get("data")
                if terms_option=='1':
                    call.session_next = Session.CALL_EXIT
                    call.save()
                    data = {
                        "client_number": call.caller_no,
                        "helpline_number": call.helpline_no,
                        "location": call.caller_location,
                        "category": call.category_option
                    }
                    self.post_data("registercall/", data)
                elif terms_option=='2':
                    r.addHangup()
                else:
                    call.session_next = Session.DISPLAY_TERMS
                    call.save()

            else:
                call.session_next = Session.DISPLAY_TERMS
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

class Feedback(View):
    def get(self,request):
        r = kookoo.Response()
        r.addPlayText("Hello World")
        r.addHangup()
        return HttpResponse(r)


class Feedbackold(View):
    def get(self,request):
        pass
        # audio_url = "http://safestreet.cse.iitb.ac.in/helpline"
        # r = kookoo.Response()
        # try:
        #     session_next = int(call.session_next)
        # except:
        #     pass
        #
        # if request.GET.get("event") == "NewCall":
        #     caller_no = request.GET.get("cid")
        #
        #
        # r = kookoo.Response()
        # r.addPlayText("Hello World")
        #
        # audio_objs = FeedbackType.objects.filter(helpline=helpline, category=audio_cat)
        # for audio_obj in audio_objs:
        #     g.append(kookoo.PlayAudio(url=audio_url + audio_obj.audio.name))
        # r.addHangup()
        # return HttpResponse(r)




