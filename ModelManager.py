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
            
        # Example function to create the PDF
        def create_pdf(qa_pairs, feedback, output_filename="output.pdf"):
            pdf = FPDF()
            pdf.add_page()
            
            # Set a base font and size
            pdf.set_font("Arial", size=12)
            
            # Loop through the question-answer pairs
            for number in sorted(qa_pairs, key=int):  # assuming keys are numeric strings
                qa = qa_pairs[number]
                
                # Add Question Heading
                pdf.set_font("Arial", "B", 12)
                pdf.cell(0, 10, f"Question {number}:", ln=True)
                # Add Question Text
                pdf.set_font("Arial", "", 12)
                pdf.multi_cell(0, 10, qa["question"])
                pdf.ln(2)  # small gap
                
                # Add Answer Heading
                pdf.set_font("Arial", "B", 12)
                pdf.cell(0, 10, f"Answer {number}:", ln=True)
                # Add Answer Text
                pdf.set_font("Arial", "", 12)
                pdf.multi_cell(0, 10, qa["answer"])
                pdf.ln(5)  # gap between entries

            # Finally, add the Feedback section
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, "Feedback:", ln=True)
            pdf.set_font("Arial", "", 12)
            pdf.multi_cell(0, 10, feedback)
            
            # Save the PDF to a file
            pdf.output(output_filename)
    
    
        def runInference(self):
            
            pdf_text = extract_text_from_pdf(self.assignment)
            qa_pairs = extract_qa(pdf_text)
            
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            
            
            
            for number in sorted(qa_pairs, key=int):  # assuming keys are numeric strings
                qa = qa_pairs[number]
                question = qa["question"]
                answer = qa["answer"]
                
                
                # Add Question Heading
                pdf.set_font("Arial", "B", 12)
                pdf.cell(0, 10, f"Question {number}:", ln=True)
                # Add Question Text
                pdf.set_font("Arial", "", 12)
                pdf.multi_cell(0, 10, question)
                pdf.ln(2)
                
                # Add Answer Heading
                pdf.set_font("Arial", "B", 12)
                pdf.cell(0, 10, f"Answer {number}:", ln=True)
                # Add Answer Text
                pdf.set_font("Arial", "", 12)
                pdf.multi_cell(0, 10, answer)
                pdf.ln(2)
                
                feedback = self.model.invoke(str(question + "\n" +answer))
                 # Add Feedback Heading
                pdf.set_font("Arial", "B", 12)
                pdf.cell(0, 10, f"Feedback {number}:", ln=True)
                # Add Feedback Text
                pdf.set_font("Arial", "", 12)
                pdf.multi_cell(0, 10, feedback)
                pdf.ln(5)  # Add a gap before next question-answer pair
                    
            # for number in sorted(qa_pairs):
            #     qa = qa_pairs[number]
            #     print(f"Question {number}: {qa['question']}")
            #     print(f"Answer {number}: {qa['answer']}\n")
            
            
            pdf.output("output.pdf")
            
            
            
            
            # prompt = ""
            # feedback = self.model.invoke(str(prompt))
            # print(feedback)

    
    
    
    
    @classmethod
    def getInstance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls._Singleton()
        return cls._instance
