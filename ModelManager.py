import DeepSeek
import Llama
import Gemma
from threading import Lock  
import torch

class GPUModelManager:
    _instance = None
    _lock = Lock()
    
    class _Singleton:
        def __init__(self):
            self._modelName = ""
            self._currentState = "empty"
            self.model = None
            self.knowledge_base = None
            self.assignment = None

        def getState(self):
            return self._currentState
        
        def getLoadedModel(self):
            return self._modelName if self._currentState == "loaded" else None
        
        def loadModel(self, modelname):        
            self._currentState = "loading"
            self._modelName = modelname
            
            if(modelname == "DeepSeek-r1"):
                self.model = DeepSeek.loadModel(self.knowledge_base)
                self._currentState = "loaded"                
            if(modelname == "Gemma-3"):
                self.model = Gemma.loadModel(self.knowledge_base)
                self._currentState = "loaded"
                
            if(modelname == "Llama-3.2"):
                self.model = Llama.loadModel(self.knowledge_base)
                self._currentState = "loaded"
        
        def clearGpu(self):
            if self._currentState == "loaded":
                self._currentState = "unloading"
                print("unloading model: " + str(self._modelName))
                
                del self.model
                self.model = None

                torch.cuda.empty_cache()
                torch.cuda.ipc_collect()
                torch.cuda.reset_peak_memory_stats()
                torch.cuda.synchronize()
                self._currentState = "empty"
    
        def runInference(self):
            result = self.model.invoke("What are DeepSeek-R1-Zero and DeepSeek-R1?")
            print(result)

    
    
    
    
    @classmethod
    def getInstance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls._Singleton()
        return cls._instance
