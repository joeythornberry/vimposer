import ctypes 

ctypes.cdll.LoadLibrary("./libtest.so")
libtest = ctypes.CDLL("./libtest.so")
libtest.message()

def talk():
    print("A something is a something in the category of somethings.")

class py_functor:
    def __init__(self, name):
        self.name = name

    def __call__(self):
        print(f"my name is {self.name}")

TALKFUNC = ctypes.CFUNCTYPE(None)

py_talk = TALKFUNC(talk)
py_name = py_functor("bobby")
py_self_namer = TALKFUNC(py_name)

libtest.run_py_func(py_talk)
libtest.run_py_func(py_self_namer)
