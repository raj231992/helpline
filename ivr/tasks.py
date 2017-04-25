from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from models import FeedbackType, FeedbackResponse, Feedback
from registercall.models import CallRequest
logger = get_task_logger(__name__)
import urllib2, time


@periodic_task(
    run_every=(crontab(hour=01, minute=17)),
    name="GetFeedback",
    ignore_result=True
)
def GetFeedback():
	print "Job occured !"

	number_of_questions = len(FeedbackType.objects.all())

	feedback_objects = Feedback.objects.exclude(current_question=number_of_questions).exclude(isCallRaised=True).order_by('-id')

	while (len(Feedback.objects.exclude(current_question=number_of_questions).exclude(isCallRaised=True))!=0):
		feedback_obj = Feedback.objects.exclude(current_question=number_of_questions).exclude(isCallRaised = True).order_by('-id')[0]
		print "inside while"
		print feedback_obj.isCallRaised

		if not feedback_obj.isCallRaised:
			print "setting isCallRaised to true"
			feedback_obj.isCallRaised = True
			feedback_obj.save()
			contactnumber = feedback_obj.task.call_request.client.client_number
			print "Contact number"
			print contactnumber
			#contactnumber= "8149599012"
			appurl="http://safestreet.cse.iitb.ac.in/helplinefeedback/"
			apikey="KKdfb62acea9b25be2363b8e3a4281d0ee"

			url = "http://www.kookoo.in/outbound/outbound.php?phone_no="+contactnumber+"&api_key="+apikey+"%20&outbound_version=2&url="+appurl
			print "calling to url"
			print url
			response = urllib2.urlopen(url)
			headers = response.info()
			time.sleep(5)
			print "Sleep done after url call!!"





    
