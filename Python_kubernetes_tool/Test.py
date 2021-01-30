import unittest

from Python_kubernetes_tool.PythonKubeTool import PythonKubeTool


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.obj = PythonKubeTool()

    def testAllPodsAllNameSpaves(self):
        self.assertEqual(list, type(self.obj.list_all_pods_all_namespaces()))

    def testExecInPodNoCommand(self):
        value = "this is an echo from the pod\n"
        self.assertEqual(value, self.obj.exec_in_pod("api-pod", "default"))

    def testExecInPodWithCommand(self):
        value = "Python 3.6.12\n"
        self.assertEqual(value, self.obj.exec_in_pod("api-pod", "default", "python --version"))

    def testExecInPodWithCommand2(self):
        value = "/app\n"
        self.assertEqual(value, self.obj.exec_in_pod("api-pod", "default", "pwd"))

    def testExecInPodWithNoPod(self):
        self.assertEqual('Please specify a pod', self.obj.exec_in_pod())

    def testExecInPodWithWrongPod(self):
        self.assertEqual('Exception caught', self.obj.exec_in_pod("QWERTY"))


if __name__ == '__main__':
    unittest.main()
