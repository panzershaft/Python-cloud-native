import os
import stat
import sys

from kubernetes import client, config
from kubernetes.stream import stream
import subprocess

from colorama import Fore, Back, Style
from termcolor import colored, cprint


class PythonKubePodExecTool(object):

    def __init__(self):
        self.config = config.load_kube_config()
        self.v1 = client.CoreV1Api()

    def list_all_pods_all_namespaces(self):
        print("\nListing all the pods\n")
        print("\033[1;32;40m \n")
        data = self.v1.list_pod_for_all_namespaces(watch=False)
        for i in data.items:
            print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
        return True

    def exec_in_pod(self, pod=None, namespace="default", usr_command="echo this is an echo "
                                                                     "from the pod"):

        exec_command = ['/bin/sh']
        resp = stream(self.v1.connect_get_namespaced_pod_exec,
                      pod,
                      namespace,
                      command=exec_command,
                      stderr=True, stdin=True,
                      stdout=True, tty=False,
                      _preload_content=False)

        commands = [
            usr_command
        ]
        data_items = []
        print("\033[1;32;40m \n")
        while resp.is_open():
            resp.update(timeout=1)
            if resp.peek_stdout():
                print("STDOUT:\n")
                print("%s" % resp.read_stdout())
                data_items.append(resp.read_stdout if resp.read_stdout else None)
            if resp.peek_stderr():
                print("STDERR: %s" % resp.read_stderr())
            if commands:
                c = commands.pop(0)
                print("Running command: %s\n" % c)
                resp.write_stdin(c + "\n")
            else:
                break

        resp.write_stdin("date\n")
        print("date: %s" % resp.read_stdout())
        resp.write_stdin("whoami\n")
        print("user: %s" % resp.read_stdout())

        resp.close()
        return resp


def main():
    os.chmod("run.sh", stat.S_IEXEC)

    with open('run.sh', 'rb') as file:
        script = file.read()
    subprocess.call(script, shell=True)
    obj = PythonKubePodExecTool()

    print_white_on_red = lambda x: cprint(x, 'white', 'on_red')

    while True:
        print("\n")
        print_white_on_red('########################################################')
        print_white_on_red('#######   SELECT ANY OF THE FOLLOWING OPTION   #########')
        print_white_on_red('########################################################')
        print("\n")
        cprint("1. TO SEE ALL THE PODS", 'blue', attrs=['bold'], file=sys.stderr)
        cprint("2. TO EXEC INTO A POD", 'blue', attrs=['bold'], file=sys.stderr)
        cprint("0. TO EXIT", 'blue', attrs=['bold'], file=sys.stderr)
        num = input("\nEnter number: ")
        if num == '1':
            obj.list_all_pods_all_namespaces()
        if num == '2':
            cmd = input("\nEnter the command you wish to execute: ")
            if not cmd:
                cmd = "python --version"
            obj.exec_in_pod("api-pod", "default", cmd)
        if num == '0':
            break


if __name__ == '__main__':
    main()
