import pickle
from time import time
from datetime import timedelta

from telegram.ext import Updater, Job, PicklePersistence, CallbackContext

f = open('../tokens.json', 'r')
token = f.read(100)
JOBS_PICKLE = 'job_tuples.pickle'

# WARNING: This information may change in future versions (changes are planned)
JOB_DATA = ('callback', 'interval', 'repeat', 'context', 'days', 'name', 'tzinfo')
JOB_STATE = ('_remove', '_enabled')


def load_jobs(jq):
    with open(JOBS_PICKLE, 'rb') as fp:
        while True:
            try:
                next_t, data, state = pickle.load(fp)
            except EOFError:
                break  # loaded all jobs

            # New object with the same data
            job = Job(**{var: val for var, val in zip(JOB_DATA, data)})

            # Restore the state it had
            for var, val in zip(JOB_STATE, state):
                attribute = getattr(job, var)
                getattr(attribute, 'set' if val else 'clear')()

            job.job_queue = jq

            next_t -= time()  # convert from absolute to relative time

            jq._put(job, next_t)


def save_jobs(jq):
    with jq._queue.mutex:  # in case job_queue makes a change

        if jq:
            job_tuples = jq._queue.queue
        else:
            job_tuples = []

        with open(JOBS_PICKLE, 'wb') as fp:
            for next_t, job in job_tuples:

                # This job is always created at the start
                if job.name == 'save_jobs_job':
                    continue

                # Threading primitives are not pickleable
                data = tuple(getattr(job, var) for var in JOB_DATA)
                state = tuple(getattr(job, var).is_set() for var in JOB_STATE)

                # Pickle the job
                pickle.dump((next_t, data, state), fp)


def save_jobs_job(context):
    save_jobs(context.job_queue)


def callback_daily(context: CallbackContext):
    # 304640198 - id of user, you can know your id with @userinfobot bot in Telegram
    context.bot.send_message(chat_id=context.job.context['chat_id'], text='test pers')  # 304640198


def main():
    # updater = Updater(...)
    my_persistence = PicklePersistence(filename='data_storage')
    updater = Updater(token, persistence=my_persistence, use_context=True)
    job_queue = updater.job_queue

    # Periodically save jobs
    job_queue.run_repeating(save_jobs_job, timedelta(seconds=5))

    try:
        load_jobs(job_queue)

    except FileNotFoundError:
        # First run
        pass

    job_queue.run_repeating(callback_daily, interval=10, first=0, context={'chat_id': 304640198})
    updater.start_polling()
    updater.idle()

    # Run again after bot has been properly shutdown
    save_jobs(job_queue)


if __name__ == '__main__':
    main()
