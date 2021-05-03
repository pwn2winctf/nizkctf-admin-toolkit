# -*- encoding: utf-8 -*-
import os
import sys
import time
import random
import subprocess
from .settings import Settings


MAIN_BRANCH = 'main'
PUSH_RETRIES = 5
SLEEP_FACTOR = 0.2


class Repo(object):
    @classmethod
    def set_clone_into(cls, clone_into):
        cls.clone_into = clone_into

    def __init__(self, url, name):
        self.url = url
        self.path = os.path.join(self.clone_into, name)
    
    def get_path(self, subpath=''):
        if os.path.exists(self.path):
            return os.path.join(self.path, subpath)
        raise EnvironmentError("The subrepository path ('%s') was not created "
                               "yet. Please call 'ctf init' to get it cloned "
                               "before performing any further actions." %
                               self.path)

    def checkout(self, ref):
        self.git(['checkout', ref])

    def clone(self):
        self.git(['clone', self.url, self.path], cwd=self.clone_into)
        self.git(['remote', 'add', 'upstream', self.url])

    def pull(self):
        self.checkout(MAIN_BRANCH)
        self.git(['pull', '--rebase', 'upstream', MAIN_BRANCH])

    def add(self, files=None):
        if files is None:
            self.git(['add', '-A'])
        else:
            self.git(['add'] + files)

    def push(self, commit_message='commit'):
        self.git(['commit', '--no-gpg-sign', '-m', commit_message],
                returncodes={0, 1})  # do not fail on 'nothing to commit'
        self.git(['push', '-u', 'origin', MAIN_BRANCH])

    def retry_push(self, commit_message, retries=PUSH_RETRIES):
        for retry in range(1, retries + 1):
            try:
                self.checkout(MAIN_BRANCH)
                self.git(['fetch', 'upstream'])
                self.git(['reset', '--hard', 'upstream/' + MAIN_BRANCH])
                self.pull()
                yield retry  # do local modifications
                self.push(commit_message)
                break
            except:
                time.sleep(SLEEP_FACTOR * (2**retry) * random.random())
                if retry == retries:
                    raise

    def git(self, args, **kwargs):
        returncodes = kwargs.pop('returncodes', {0})
        if 'cwd' not in kwargs:
            kwargs['cwd'] = self.get_path()

        p = subprocess.run(['git'] + args, cwd=kwargs['cwd'], capture_output=True)

        print(p.args, file=sys.stderr)
        if p.stdout.decode():
            print(p.stdout.decode())

        r = None
        if 'stdout' in kwargs:
            r = p.stdout

        returncode = p.returncode
        if returncode not in returncodes:
            print(p.stderr.decode())
            raise GitError(returncode)

        return r


class GitError(Exception):
    def __init__(self, returncode, *args):
        self.returncode = returncode
        super(GitError, self).__init__(*args)
    def __repr__(self):
        return 'GitError(%r)' % self.returncode


thisdir = os.path.dirname(os.path.realpath(__file__))
Repo.set_clone_into(os.path.realpath(os.path.join(thisdir, os.pardir)))

contents = Repo(Settings.contents_repo, 'contents')
trail = Repo(Settings.trail_repo, 'trail')
