from django.http import HttpResponse
from django.views.generic import View
from .models import IVR_Call,Call_Forward,Misc_Audio,Misc_Category,IVR_Audio,Language,Call_Forward_Details, FeedbackType, Feedback, FeedbackResponse
from .options import Session
from management.models import HelperCategory,HelpLine
from registercall.models import Task
import kookoo,requests,json

# Create your views here.

class IVR(View):
    def post_data(self,url, data):
        base_url = "http://vmocsh.cse.iitb.ac.in/"
        authentication = ("admin", "r@j2331992")
        headers = {'Content-type': 'application/json',}
        r = requests.post(base_url + url, data=json.dumps(data), headers=headers, auth=authentication)

    def get(self,request):
        audio_url = "http://vmocsh.cse.iitb.ac.in/media/"
        r = kookoo.Response()
        sid = request.GET.get("sid")
        try:
            call = IVR_Call.objects.get(sid=sid)
            session_next = int(call.session_next)
        except:
            pass
        if request.GET.get("event") == "Hangup" and request.GET.get("process") == "dial" and request.GET.get(
                "status") == "answered":
            helper_no = request.GET.get("cid")
            call_forward = Call_Forward.objects.get(helper_no=helper_no)
            caller_no = call_forward.caller_no
            task = call_forward.task
            caller_no_len = len(call_forward.caller_no)
            caller_no = caller_no[caller_no_len - 10:]
            call_forward_details = Call_Forward_Details.objects.get(helper_no=helper_no, caller_no=caller_no, task=task,status='initiated')
            call_forward_details.status = "completed"
            call_forward_details.call_duration = request.GET.get("callduration")
            call_forward_details.call_pickup_duration = request.GET.get("pickduration")
            call_forward_details.save()
            call_forward.delete()
        if request.GET.get("event") == "Hangup" and request.GET.get("process") == "none":
            try:
                helper_no = request.GET.get("cid")
                call_forward = Call_Forward.objects.get(helper_no=helper_no)
                caller_no = call_forward.caller_no
                task = call_forward.task
                caller_no_len = len(call_forward.caller_no)
                caller_no = caller_no[caller_no_len - 10:]
                call_forward_details = Call_Forward_Details.objects.get(helper_no=helper_no, caller_no=caller_no, task=task,
                                                                        status='initiated')
                call_forward_details.status = "not_answered"
                call_forward_details.save()
                call_forward.delete()
            except:
                pass
        if request.GET.get("event")=="NewCall":
            caller_no = request.GET.get("cid")
            helpline_no = request.GET.get("called_number")
            caller_location = request.GET.get("circle")
            call_forward = Call_Forward.objects.filter(helper_no=caller_no[len(caller_no)-10:])
            task = Task.objects.filter()
            if call_forward:
                session_next = Session.CALL_FORWARD
                helper_no = call_forward[0].helper_no
                caller_no = call_forward[0].caller_no
                task = call_forward[0].task
                caller_no_len = len(call_forward[0].caller_no)
                caller_no = caller_no[caller_no_len - 10:]
                call_forward_details = Call_Forward_Details(helper_no=helper_no,caller_no=caller_no,task=task)
                call_forward_details.save()
                r.addDial(phoneno=caller_no)
            else:
                try:
                    session_next = Session.DISPLAY_LANGUAGE
                    caller_no_len = len(caller_no)
                    caller_no = caller_no[caller_no_len - 10:]
                    call = IVR_Call(sid=sid,caller_no=caller_no,helpline_no=helpline_no,caller_location=caller_location,session_next=session_next)
                    call.save()
                except:
                    pass

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


        return HttpResponse(r)

class FeedbackView(View):
    def get(self,request):
        audio_url = "http://vmocsh.cse.iitb.ac.in/media/"

        try:
            number_of_questions = len(FeedbackType.objects.all())
            caller_no = request.GET.get("cid")
            feedback_obj = Feedback.objects.filter(task__call_request__client__client_number = caller_no).filter(isFeedbackTaken=False).order_by('-id')[0]

        except Exception, e:
            print str(e)

        r = kookoo.Response()

        if (request.GET.get("event") == "NewCall"):
            r.addPlayText("Good Morning, Dear User we would like to take your feedback on your experience with career counselling. ")

        if (request.GET.get("event") != "GotDTMF" and request.GET.get("event") != "Disconnect"):
            g = r.append(kookoo.CollectDtmf(maxDigits=1, timeout=5000))
            feedback_type = FeedbackType.objects.get(id=feedback_obj.current_question+1)
            # r.addPlayText(feedback_type.question)
            # g.append(kookoo.PlayAudio(url=audio_url + audio_obj.audio.name))
            g.append(kookoo.PlayText(feedback_type.question))

        if request.GET.get("event")=="GotDTMF":

            if len(request.GET.get("data"))!=0:
                new_feedback_type = FeedbackType.objects.get(id=feedback_obj.current_question+1)
                feedback_resp = FeedbackResponse(feedbackType=new_feedback_type,response = int(request.GET.get("data")))
                feedback_resp.save()
                feedback_obj.feedbackresponses.add(feedback_resp)
                feedback_obj.current_question+=1
                feedback_obj.save()

                if (feedback_obj.current_question >= len(FeedbackType.objects.all())):
                    feedback_obj.isFeedbackTaken = True
                    feedback_obj.save()
                    r.addPlayText("Thank you for your feedback, Have a nice day ")
                    r.addHangup()

        return HttpResponse(r)



