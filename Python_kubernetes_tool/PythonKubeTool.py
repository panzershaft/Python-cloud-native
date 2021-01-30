from kubernetes import client, config
from kubernetes.stream import stream


class PythonKubeTool(object):

    def __init__(self):
        self.config = config.load_kube_config()
        self.v1 = client.CoreV1Api()

    def list_all_pods_all_namespaces(self):
        print("Listing all the pods")
        data = self.v1.list_pod_for_all_namespaces(watch=False)
        data_list = []
        for i in data.items:
            data_list.append([i.status.pod_ip, i.metadata.namespace, i.metadata.name])
        return data_list

    def exec_in_pod(self, pod=None, namespace="default", usr_command="echo this is an echo "
                                                                     "from the pod"):
        command_executor = [
            '/bin/sh',
            '-c',
            usr_command]
        if not pod:
            return 'Please specify a pod'
        try:
            resp = stream(self.v1.connect_get_namespaced_pod_exec,
                          pod, namespace, command=command_executor, stderr=True, stdin=False,
                          stdout=True, tty=False)
        except Exception as e:
            return 'Exception caught'
        return resp
