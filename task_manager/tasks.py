"""
Script used to manage schedule jobs using celery-redis.
    All four tasks will be need to be added in models related to task
    management in celery which runs after intervals
"""
from datetime import timedelta

from django.utils import timezone

from dtss.celery import app
from task_manager.helpers import AssignAction, HelperMethods
from task_manager.models import Action, Assign
from task_manager.options import (ActionStatusOptions, ActionTypeOptions,
                                  AssignStatusOptions)


@app.task
def new_task_remainder():
    """
    New task remainder to helper to accept/reject new task
    """

    # Start time below which actions have to be picked
    start = timezone.localtime(timezone.now()) - timedelta(hours=4)

    pending_actions = Action.objects.select_related('task__call_request__client').filter(
        status=ActionStatusOptions.ASSIGN_PENDING,
        modified__lte=start,
    )

    # For each pending action, send remainder
    for pending_action in pending_actions:

        # Change action modified timestamp, to track last remainder sent
        pending_action.save()

        action_to = ActionTypeOptions()
        task_type = action_to.get_action_type(pending_action.action_type)
        data = {
            "notification": "new_task_pending",
            "client_number": pending_action.task.call_request.client.client_number,
            "task_id": pending_action.task.pk,
            "task_type": task_type,
        }

        helper_methods = HelperMethods()
        helper_methods.send_new_task_notification(action=pending_action, data=data)


@app.task
def pending_task_remainder():
    """
    Task pending remainder to assigned helper to complete assigned task
    """

    # Start time below which assigns have to be picked
    start = timezone.localtime(timezone.now()) - timedelta(hours=4)

    pending_assigns = Assign.objects.select_related('action__task__call_request__client').filter(
        status=AssignStatusOptions.ACCEPTED,
        modified__lte=start,
    )

    # For each pending assign, send remainder
    for pending_assign in pending_assigns:
        # Change assign modified timestamp, to track last remainder sent
        pending_assign.save()

        action_to = ActionTypeOptions()
        task_type = action_to.get_action_type(pending_assigns.action.action_type)
        data = {
            "notification": "assigned_task_pending",
            "client_number": pending_assign.action.task.call_request.client.client_number,
            "task_id": pending_assign.action.task.pk,
            "task_type": task_type,
        }

        gcm_canonical_id = [pending_assign.helper.gcm_canonical_id]
        helper_methods = HelperMethods()
        helper_methods.send_gcm_message(gcm_canonical_id, data)


@app.task
def complete_timeout():
    """
    None of the helpers accepted in given time, leading to new action and assigns
    """
    reassign_action_tasks = []

    # Start time below which assigns have to be picked
    start = timezone.localtime(timezone.now()) - timedelta(hours=12)

    timeout_assigns = Assign.objects.select_related('action__task').filter(
        status=AssignStatusOptions.PENDING,
        action__status=ActionStatusOptions.ASSIGN_PENDING,
        created__lte=start,
    )

    # For each timed out assign, change status to timeout
    for timeout_assign in timeout_assigns:
        timeout_assign.status = AssignStatusOptions.TIMEOUT
        timeout_assign.save()

        # If task not in reassign action task list, append
        if timeout_assign.action.task not in reassign_action_tasks:
            reassign_action_tasks.append(timeout_assign.action.task)
            timeout_assign.action.status = ActionStatusOptions.COMPLETE_TIMEOUT
            timeout_assign.action.save()

    assign_act = AssignAction()
    # For all tasks in reassign action, run assign_action helper method
    for task in reassign_action_tasks:
        assign_act.assign_action(task)


@app.task
def assign_timeout():
    """
    Assigned helper didn't complete task in time, leading to new action and assigns
    """

    # Start time below which assigns have to be picked
    start = timezone.localtime(timezone.now()) - timedelta(hours=12)

    timeout_assigns = Assign.objects.select_related('action__task').filter(
        status=AssignStatusOptions.ACCEPTED,
        accepted__lte=start,
    )

    # For each timed out assign and action, change status to timeout
    for timeout_assign in timeout_assigns:
        timeout_assign.status = AssignStatusOptions.TIMEOUT
        timeout_assign.save()
        timeout_assign.action.status = ActionStatusOptions.ASSIGN_TIMEOUT
        timeout_assign.action.save()

        # Assign new action
        assign_act = AssignAction()
        assign_act.assign_action(timeout_assign.action.task)
