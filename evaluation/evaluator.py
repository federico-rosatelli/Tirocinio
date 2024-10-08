#import borderEval
from evaluation import borderEval
from evaluation import printer
import math
import numpy as np

class Eval:
    def __init__(self,b1:float=0.7,b2:float=1,b3:float=0.9,b4:float=1) -> None:
        if (b1 > 1 or b1 < 0) or (b2 > 1 or b2 < 0) or (b3 > 1 or b3 < 0) or (b4 > 1 or b4 < 0):
            value = b1 if b1 > 1 or b1 < 0 else b2 if b2 > 1 or b2 < 0 else b3 if b3 > 1 or b3 < 0 else b4
            raise ValueError(f"Biases must be > 0 and < 1. Got: {value}")
        self.b1 = b1
        self.b2 = b2
        self.b3 = b3
        self.b4 = b4
        self.already_seen = []
        self.next_obj:list[borderEval.Segment] = []
        self.printer = None
        pass

    def newEval(self,png_file) -> list[borderEval.Segment]:
        data = borderEval.borderSegments(png_file)
        if len(data) == 0:
            raise Exception(f"Cannot find an object in image {type(png_file)}")
        segments:list[borderEval.Segment] = []
        for segment in data:
            evalP = self.getEvaluationPoint(segment())
            #data[d]["file_name"] = png_file
            segment.addData("points",evalP)
            segment.addData("pointVect",math.sqrt(sum([d**2 for d in evalP])))
            self.next_obj.append(segment)
            segments.append(segment)
        return segments

    def getEvaluationPoint(self,eval_points:dict) ->list:
        evals = [
            # Grandezza
            self.b1*(
                eval_points["area"]/eval_points["totArea"]
            ),
            # Frastagliato
            self.b2*(
                1 - (
                        (np.count_nonzero(eval_points["bwImage"])/np.count_nonzero(eval_points["gaussianDiff"]))
                )
            ),
            # Colore acceso
            self.b3*(
                1 - (
                    math.sqrt(
                        (255-eval_points["dominantColor"][0])**2 + 
                        (255-eval_points["dominantColor"][1])**2 + 
                        (255-eval_points["dominantColor"][2])**2
                    )/442
                )
            ),
            # Sbilanciato
            # TODO Simmetria
            self.b4*(
                1-(
                    math.sqrt(
                        (eval_points["symmetry"]["center"][0]-eval_points["symmetry"]["closestP"][0])**2 +
                        (eval_points["symmetry"]["center"][1]-eval_points["symmetry"]["closestP"][1])**2
                    ) /
                    (
                        math.sqrt(
                            (eval_points["symmetry"]["center"][0]-eval_points["symmetry"]["farthestP"][0])**2 +
                            (eval_points["symmetry"]["center"][1]-eval_points["symmetry"]["farthestP"][1])**2
                        ) + 1
                    )
                    
                )
            )
        ]
        return evals
    
    def getNextObj(self) -> borderEval.Segment:
        m_vect = max(self.next_obj, key=lambda x:x.get('pointVect'))
        
        self.already_seen.append(m_vect)
        for i in range(len(self.next_obj)):
            if str(self.next_obj[i]) == str(m_vect):
                self.next_obj.pop(i)
                break
        self.printer = printer.Printer(m_vect())
        return m_vect
    
    def delObj(self,objs) -> None:
        for obj in objs:
            for i in range(len(self.next_obj)):
                if str(obj) == str(self.next_obj[i]):
                    self.next_obj.pop(i)
                    break
        return 
    
    def showImage(self) -> None:
        if not self.printer:
            return
        self.printer.showImgContours()
        return
    
    def showBwImage(self) -> None:
        if not self.printer:
            return
        self.printer.showBwImage()
        return
    
    def showGaussianDiff(self) -> None:
        if not self.printer:
            return
        self.printer.showGaussianDiff()
        return


class ImageObject:
    def __init__(self) -> None:
        pass