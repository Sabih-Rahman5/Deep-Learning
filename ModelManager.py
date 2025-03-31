import DeepSeek.py
from threading import Lock
from numba import cuda

class GPUModelManager:
    _instance = None
    _lock = Lock()
    
    class _Singleton:
        def __init__(self):
            self._modelName = ""
            self._currentState = "empty"
            self.model = None
        
        def getState(self):
            return self._currentState
        
        def getLoadedModel(self):
            return self._modelName if self._currentState == "loaded" else None
        
        def loadModel(self, modelname):
            if self._currentState == "loaded":
                if self._modelName == modelname:
                    print("model already loaded")
                    return
                else:
                    self.clearGpu()
        
            self._currentState = "loading"
            self._modelName = modelname
            
            if(modelname == "DeepSeek-r1"):
                self.model = DeepSeek.loadModel()
                self._currentState = "loaded"
        
        def clearGpu(self):
            if self._currentState == "loaded":
                self._currentState = "unloading"
                print("unloading model: " + str(self._modelName))
                device = cuda.get_current_device()
                device.reset()
                self._modelName = None
                self._currentState = "empty"
    
    @classmethod
    def getInstance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls._Singleton()
        return cls._instance
