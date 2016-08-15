"""
Register Call Views
"""
import re

from django.http import JsonResponse
from rest_framework.views import APIView

from registercall.models import CallRequest, Client, HelpLine, Task
from registercall.options import (CallRequestStatusOptions,
                                         TaskStatusOptions)
from task_manager.helpers import AssignAction


class RegisterCall(APIView):
    """
    Register call used to handle incoming call requests
    """
    def validate_input(self, request):
        """
        Incoming input validator
        """
        data = request.data

        client_number = data.get('client_number');
        helpline_number = data.get('helpline_number')


        # Checking for required fields
        if client_number is None or helpline_number is None:
            return False

        # Validating phone pattern
        phone_pattern = r'^(\+91|0)?\d{10}$'
        if re.match(phone_pattern, client_number) is not None and \
           re.match(phone_pattern, helpline_number) is not None:
            return data
        else:
            return False


    def register_call(self, data):
        """
        Handler for valid requests
        """



        # req_status is the status used to keep track of current call request, it is initialized to
        # CREATED and might update its state to BLOCKED/MERGED before inserting into the model
        req_status = CallRequestStatusOptions.CREATED

        client_number = data.get('client_number');
        helpline_number = data.get('helpline_number')
        location = data.get('location')

        # Trying to get client instance and if doesn't exist, create one
        try:
            client = Client.objects.get(client_number=client_number)
            # To check if client is blocked
            if client.is_blocked():
                req_status = CallRequestStatusOptions.BLOCKED

        except Client.DoesNotExist:
            client = Client.objects.create(client_number=client_number,location=location)

        # To check if task already pending for client
        client_has_pending_tasks = Task.objects.filter(
            status=TaskStatusOptions.PENDING,
            call_request__client=client
        ).exists()

        if client_has_pending_tasks:
            req_status = CallRequestStatusOptions.MERGED

        try:
            # Creating call request instance
            call_request = CallRequest.objects.create(
                helpline=HelpLine.objects.get(helpline_number=helpline_number),
                client=client,
                status=req_status,
                )
        except HelpLine.DoesNotExist:
            req_status = CallRequestStatusOptions.INVALID_HELPLINE

        # Creating new task if client isn't blocked and task not pending for client
        if req_status == CallRequestStatusOptions.CREATED:
            new_task = Task.objects.create(call_request=call_request)
            action = AssignAction()
            action.assign_action(new_task)

        return req_status

    def post(self, request):
        """
        Post request handler
        """
        data = self.validate_input(request=request)

        if data:
            state = self.register_call(data=data)

            if state == CallRequestStatusOptions.CREATED:
                return JsonResponse({"notification": "new_task_created"}, status=201)
            elif state == CallRequestStatusOptions.MERGED:
                return JsonResponse({"notification": "merged_with_pending_task"}, status=202)
            elif state == CallRequestStatusOptions.INVALID_HELPLINE:
                return JsonResponse({"notification": "invalid_helpline"}, status=400)
            elif state == CallRequestStatusOptions.BLOCKED:
                return JsonResponse({"notification": "client_blocked"}, status=406)

        else:
            return JsonResponse({"notification": "bad_request"}, status=400)
