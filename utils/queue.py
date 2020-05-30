from datetime import datetime, timedelta

import pytz


def recover_queue(users_data, jobQueue, callback_func):
    """
    Recovers jobQueue after restarting of bot
    :param users_data:
    :param jobQueue:
    :param callback_daily:
    :return:
    """
    for chat_id, user in users_data.items():
        for hour, minutes in user.get('notifs', {}).items():
            for minute in minutes:
                t = datetime.strptime(f'{hour}:{3 * minute}', '%H:%M').time()
                if datetime.now().astimezone(pytz.utc) > (user['timezone']).localize(
                        datetime.combine(datetime.today(), t)).astimezone(pytz.utc):
                    t = user['timezone'].localize(
                        datetime.combine(datetime.today() + timedelta(days=1), t))
                else:
                    t = user['timezone'].localize(datetime.combine(datetime.today(), t))
                jobQueue.run_daily(callback_func, t,
                                   context={'chat_id': chat_id, 'lat': user['lat'], 'lon': user['lon']},
                                   name=f"{chat_id}_{t.strftime('%H:%M')}")


def update_queue(chat_id, context, callback_func):
    """
    Function removes all previous jobs for specific user and then creates them again.
    This function is called only when location of user has changed
    :param chat_id: int, id of chat
    :param user_data:
    :param jobQueue:
    :param callback_daily:
    :return:
    """
    for hour, minutes in context.user_data.get('notifs', {}).items():
        for minute in minutes:
            # Delete previous jobs:
            time = f'{hour}:{str(minute * 3).zfill(2)}'
            rem_notif(chat_id, time, context)

            # Add new jobs:
            set_notif(chat_id, time, context, callback_func)


def rem_notif(chat_id, time, context):
    """
    Removes notification from jobsQueue for given user and given time
    :param chat_id:
    :param time:
    :param user_data:
    :return:
    """
    t = datetime.strptime(time, '%H:%M').time()
    # context.user_data['notifs'][hour_int].remove(t)

    for old_job in context.job_queue.get_jobs_by_name(f"{chat_id}_{t.strftime('%H:%M')}"):
        old_job.enabled = False  # Temporarily disable this job
        old_job.schedule_removal()


def set_notif(chat_id, time, context, callback_daily):
    """
    Sets new notification for giver user and given time
    :param chat_id:
    :param time:
    :param user_data:
    :return:
    """
    user_data = context.user_data
    t = datetime.strptime(time, '%H:%M').time()

    # user_data['notifs'][hour].add(t)
    user_tz = user_data['timezone']

    if datetime.now().astimezone(pytz.utc) > (user_tz).localize(
            datetime.combine(datetime.today(), t)).astimezone(pytz.utc):
        t = user_tz.localize(
            datetime.combine(datetime.today() + timedelta(days=1), t))
    else:
        t = user_tz.localize(datetime.combine(datetime.today(), t))
    context.job_queue.run_daily(callback_daily, t,
                                context={'chat_id': chat_id, 'lat': user_data['lat'],
                                         'lon': user_data['lon']},
                                name=f"{chat_id}_{t.strftime('%H:%M')}")
