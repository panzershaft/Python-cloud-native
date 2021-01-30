import os
import stat
import sys

from kubernetes import client, config
from kubernetes.client import ApiException
from kubernetes.stream import stream
import subprocess

from colorama import Fore, Back, Style
from termcolor import colored, cprint
from tabulate import tabulate


class PythonKubePodExecTool(object):

    def __init__(self):
        self.config = config.load_kube_config()
        self.v1 = client.CoreV1Api()
        self.pod_list = []

    def read_namespaced_pod(self,pod_name, name_space="default"):
        try:
            resp = self.v1.read_namespaced_pod(pod_name,name_space)
            print(resp)
            return True
        except ApiException as e:
            if e.status != 404:
                print("Unknown error: %s" % e)
                exit(1)

    def list_all_pods_all_namespaces(self):
        print("\nListing all the pods\n")
        data = self.v1.list_pod_for_all_namespaces(watch=False)
        for i in data.items:
            self.pod_list.append([i.status.pod_ip, i.metadata.namespace, i.metadata.name])
        print(tabulate(self.pod_list, headers=['IP', 'NAMESPACE', 'POD_NAME']))
        return True

    def list_available_pods_namespaces(self):
        print("\nSELECT FROM THE FOLLOWING PODS, NAMESPACES")
        if self.pod_list:
            print(tabulate(self.pod_list, headers=['IP', 'NAMESPACE', 'POD_NAME']))
            return True
        self.list_all_pods_all_namespaces()
        return True

    def exec_in_pod(self, pod=None, namespace="default", usr_command="echo this is an echo "
                                                                     "from the pod"):
        """

        :param pod: name of pod (str)
        :param namespace: string value
        :param usr_command: unix command
        :return: True
        """
        try:
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

            while resp.is_open():
                resp.update(timeout=1)
                if resp.peek_stdout():
                    print("STDOUT:\n")
                    print("%s" % resp.read_stdout())
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

        except ApiException as e:
            if e.status != 404:
                print("Unknown error: %s" % e)

                exit(1)


def main():
    os.chmod("run.sh", stat.S_IEXEC)

    with open('run.sh', 'rb') as file:
        script = file.read()
    subprocess.call(script, shell=True)
    obj = PythonKubePodExecTool()

    print_red_on_white = lambda x: cprint(x, 'red', 'on_white')

    while True:
        print("\n")
        print_red_on_white('########################################################')
        print_red_on_white('#######   SELECT ANY OF THE FOLLOWING OPTION   #########')
        print_red_on_white('########################################################')
        print("\n")

        cprint("1. List all pods of all namespaces", 'blue', attrs=['bold'], file=sys.stderr)
        cprint("2. Show pod data", 'blue', attrs=['bold'], file=sys.stderr)
        cprint("3. Exec into a particular pod", 'blue', attrs=['bold'], file=sys.stderr)
        cprint("0. TO EXIT", 'blue', attrs=['bold'], file=sys.stderr)

        num = input("\nEnter number: ")

        if num == '1':
            obj.list_all_pods_all_namespaces()

        if num == '2':
            obj.list_available_pods_namespaces()
            pod_name = input("\nEnter the pod to exec: ")
            namespace = input("\nEnter the Namespace of the pod: ")
            if not namespace:
                namespace="default"
            obj.read_namespaced_pod(pod_name, namespace)

        if num == '3':
            obj.list_available_pods_namespaces()
            pod_name = input("\nEnter the pod to exec: ")
            cmd = input("\nEnter the command to exec: ")

            if not cmd:
                cmd = "python --version"
            obj.exec_in_pod(pod_name, "default", cmd)

        if num == '0':
            break


if __name__ == '__main__':
    main()
