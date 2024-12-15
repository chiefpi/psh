class Job(object):
    def __init__(self, name, thread):
        self.name = str(name)
        self.thread = thread

    def __repr__(self):
        return f'{self.status(): <10}{self.name}'

    def done(self):
        return not self.thread.is_alive()

    def status(self):
        return 'Done' if self.done() else 'Running'


class JobList(object):
    def __init__(self):
        self.jobs = {}

    def __repr__(self):
        return '\n'.join([f'[{jid}] {job}' for jid, job in self.jobs.items()])

    def add_job(self, job):
        self.jobs[len(self.jobs)] = job

    def del_job(self, jid):
        del self.jobs[jid]

    def check(self):
        jids_done = []
        for jid, job in self.jobs.items():
            if job.done():
                print(f'[{jid}] {job}')
                jids_done.append(jid)
        for jid in jids_done:
            self.del_job(jid)
