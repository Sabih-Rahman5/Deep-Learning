import DeepSeek
import Llama
import Gemma
from threading import Lock  
import torch
from fpdf import FPDF

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
                # torch.cuda.ipc_collect()
                # torch.cuda.reset_peak_memory_stats()
                # torch.cuda.synchronize()
                self._currentState = "empty"
    
    
    
        def extract_text_from_pdf(pdf_path):
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        
        def extract_qa(text):
            # This regex looks for "question <number>:" and then "answer <same number>:".
            # It uses a backreference (\1) to ensure that the question and answer numbers match.
            pattern = re.compile(
                r"question\s*(\d+):\s*(.*?)\s*answer\s*\1:\s*(.*?)(?=question\s*\d+:|$)",
                re.IGNORECASE | re.DOTALL
            )
            # Find all matches; each match is a tuple (number, question_text, answer_text)
            matches = pattern.findall(text)
            
            # Build a dictionary mapping question numbers to a structured dictionary
            qa_dict = {}
            for num, question, answer in matches:
                qa_dict[int(num)] = {
                    'question': question.strip(),
                    'answer': answer.strip()
                }
            return qa_dict
            
    
    
        def runInference(self):
            
            pdf_text = extract_text_from_pdf(self.assignment)
            qa_pairs = extract_qa(pdf_text)
            
            for number in sorted(qa_pairs):
                qa = qa_pairs[number]
                print(f"Question {number}: {qa['question']}")
                print(f"Answer {number}: {qa['answer']}\n")
            
            
            # prompt = ""
            # feedback = self.model.invoke(str(prompt))
            # print(feedback)

    
    
    
    
    @classmethod
    def getInstance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls._Singleton()
        return cls._instance
