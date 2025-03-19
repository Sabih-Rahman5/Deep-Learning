from threading import Lock

class GPUModelManager:
    _instance = None
    _lock = Lock()
    
    class _Singleton:
        def __init__(self):
            self._modelName = ""
            self._currentState = "empty"
        
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
                
            self._modelName = modelname
            self._currentState = "loading"
            # Simulate loading process
            print("loading " + modelname)
            self._currentState = "loaded"
        
        def clearGpu(self):
            if self._currentState == "loaded":
                self._currentState = "unloading"
                print("unloading model: " + str(self._modelName))
                self._modelName = None
                self._currentState = "empty"
    
    @classmethod
    def getInstance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls._Singleton()
        return cls._instance
