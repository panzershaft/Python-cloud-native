from kubernetes import client, config
from kubernetes.stream import stream


class PythonKubePodExecTool(object):

    def __init__(self):
        self.config = config.load_kube_config()
        self.v1 = client.CoreV1Api()

    def list_all_pods_all_namespaces(self):
        print("Listing all the pods")
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
        while resp.is_open():
            resp.update(timeout=1)
            if resp.peek_stdout():
                print("STDOUT: %s" % resp.read_stdout())
                data_items.append(resp.read_stdout if resp.read_stdout else None)
            if resp.peek_stderr():
                print("STDERR: %s" % resp.read_stderr())
            if commands:
                c = commands.pop(0)
                print("Running command... %s\n" % c)
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
    obj = PythonKubePodExecTool()
    obj.list_all_pods_all_namespaces()
    obj.exec_in_pod("api-pod", "default", "python --version")

if __name__ == '__main__':
    main()