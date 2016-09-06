"""
Helper methods to handle incoming requests
"""
import json

import requests
from django.utils import timezone

from register_helper.models import Helper
from registercall.options import TaskStatusOptions
from task_manager.models import Action, Assign, QandA
from task_manager.options import (ActionStatusOptions, ActionTypeOptions,
                                  AssignStatusOptions)
from management.notifications import push_notification


class AssignAction():
    """
    Class to handle Assign Action
    """
    def primary_assign(self, task):
        """
        Assign Action handle for first time, primary is assigned
        """
        helper_methods = HelperMethods()

        current_action = Action.objects.create(
            task=task,
            action_type=ActionTypeOptions.PRIMARY,
        )
        data = "New Task Has Been Assigned"
        helper_methods.assign_helpers(
            action=current_action,
            category=task.category,
            data=data,
            no_of_helpers=2,
        )

    def specialist_assign(self, task):
        """
        Assign action handle once primary assign
        """
        helper_methods = HelperMethods()

        qna = QandA.objects.get(task=task)

        current_action = Action.objects.create(
            task=task,
            action_type=ActionTypeOptions.SPECIALIST,
        )
        data = data = "New Task Has Been Assigned"
        helper_methods.assign_helpers(
            action=current_action,
            category=task.category,
            data=data,
            no_of_helpers=2,
        )

    def feedback_assign(self, task):
        """
        Assign action handle once specialist assign completes
        """
        helper_methods = HelperMethods()

        current_action = Action.objects.create(
            task=task,
            action_type=ActionTypeOptions.FEEDBACK,
        )
        data = "New Feedback Task Has Been Assigned"
        helper_methods.assign_helpers(
            action=current_action,
            category="General",
            data=data,
            no_of_helpers=2,
        )

    def specialist_confirm_assign(self, task):
        """
        Assign action handle once feedback completes
        """
        helper_methods = HelperMethods()

        # Fetches the QandA for the task
        qna = QandA.objects.get(task=task)

        current_action = Action.objects.create(
            task=task,
            action_type=ActionTypeOptions.SPECIALIST_CONFIRM,
        )
        data = "New Confirm Task Has Been Assigned"
        helper_methods.assign_helpers(
            action=current_action,
            category=task.category,
            data=data,
            no_of_helpers=2,
        )

    def specialist_confirm_complete(self, task):
        """
        Task completion
        """
        task.status = TaskStatusOptions.COMPLETED
        task.save()

    def timeout(self, task, previous_action):
        """
        Complete/Assign action timeout handler
        """
        action_to = ActionTypeOptions()

        if action_to.get_action_type(previous_action.action_type) == "Primary":
            self.primary_assign(task)
        elif action_to.get_action_type(previous_action.action_type) == "Specialist":
            self.specialist_assign(task)
        elif action_to.get_action_type(previous_action.action_type) == "Feedback":
            self.feedback_assign(task)
        elif action_to.get_action_type(previous_action.action_type)\
                == "Specialist Confirm":
            self.specialist_confirm_assign(task)

    def assign_action(self, task):
        """
        Method to assigning new action to task based on current action
        """

        # Fetching the previous action
        try:
            previous_action = Action.objects.filter(task=task).latest('created')
        except Action.DoesNotExist:
            previous_action = None

        # If task is incoming is being assigned an action for the first time
        if previous_action is None:
            self.primary_assign(task)

        # In case of Primary Task completes
        elif previous_action.action_type == ActionTypeOptions.PRIMARY and\
                previous_action.status == ActionStatusOptions.COMPLETED:
            self.specialist_assign(task)

        # In case of Specialist Task completes
        elif previous_action.action_type == ActionTypeOptions.SPECIALIST and \
                previous_action.status == ActionStatusOptions.COMPLETED:
            self.feedback_assign(task)

        # In case of Feedback completes
        elif previous_action.action_type == ActionTypeOptions.FEEDBACK and \
                previous_action.status == ActionStatusOptions.COMPLETED:
            self.specialist_confirm_assign(task)

        # In case of task complete
        elif previous_action.action_type == ActionTypeOptions.SPECIALIST_CONFIRM and \
                previous_action.status == ActionStatusOptions.COMPLETED:
            self.specialist_confirm_complete(task)

        # In case of Assigned timeout/ Complete timeout/ Rejected by all helpers, reassign action
        elif previous_action.status == ActionStatusOptions.ASSIGN_TIMEOUT or \
                previous_action.status == ActionStatusOptions.COMPLETE_TIMEOUT or \
                previous_action.status == ActionStatusOptions.REJECTED:
            self.timeout(task, previous_action)

        return True


class HelperMethods():
    """
    Class used to define helper methods
    """
    def assign_helpers(self, action, category, data, no_of_helpers):
        """
        Used to assign helpers to a particular action
            param action: Action to which we need to assign helpers
            param category: Category of helpers
            param data: Data Message to be sent to helpers
            param no_of_helpers: The number of helpers we need to assign
        """

        free_helpers_assigned = 0

        # Initially tries to assign free helpers
        helpers = Helper.objects\
            .filter(category__name=category) \
            .exclude(assigned_to__status=AssignStatusOptions.PENDING) \
            .exclude(assigned_to__status=AssignStatusOptions.ACCEPTED) \
            .order_by('last_assigned')[:no_of_helpers]

        for helper in helpers:
            # Used to prioritize helpers for later selection
            helper.last_assigned = timezone.localtime(timezone.now())
            helper.save()

            # Create new assign object for selected helper
            Assign.objects.create(helper=helper, action=action)

            # Increment the count for helpers assigned
            free_helpers_assigned += 1

        # If it couldn't assign required free helpers it assigns tasks to existing busy helpers
        if no_of_helpers != free_helpers_assigned:
            helpers = Helper.objects \
                .filter(category__name=category) \
                .order_by('last_assigned')[:(no_of_helpers-free_helpers_assigned)]

            for helper in helpers:
                # Used to prioritize helpers for later selection
                helper.last_assigned = timezone.localtime(timezone.now())
                helper.save()

                # Create new assign object for selected helper
                Assign.objects.create(helper=helper, action=action)

        # Send new task notifications to clients
        #self.send_new_task_notification(action=action, data=data)

    def send_new_task_notification(self, action, data):
        """
        Sends task notifications to respective helpers for specified action
        """

        gcm_canonical_ids = []
        assignments = Assign.objects.filter(
            action=action,
            status=AssignStatusOptions.PENDING,
        )

        for assignment in assignments:
            # Send notification to all GCM ids of helpers
            push_notification(assignment.helper.gcm_canonical_id,data)





    def terminate_and_assign_new_action(self, action):
        """
        Terminates current assign and action and creates new action
        """
        try:
            assign = Assign.objects.filter(
                action__task=action.task,
                status=AssignStatusOptions.ACCEPTED,
            ).latest("created")
        except Assign.DoesNotExist:
            return False

        # Completing current assign and action
        assign.status = AssignStatusOptions.COMPLETED
        assign.save()
        assign.action.status = ActionStatusOptions.COMPLETED
        assign.action.save()

        # Assigning new action
        new_action = AssignAction()

        return new_action.assign_action(action.task)

    def set_helper_rating(self, task, rating):
        """
        logic for helper rating to be implemented
        """
        pass
