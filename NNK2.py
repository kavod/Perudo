import numpy as np

class NNK(object):
    
    @staticmethod
    def sin(x,eta=1,deriv=False):
        if(deriv==True):
            return np.cos(x)
        return np.sin(x)
    
    @staticmethod
    def tanh(x,eta=1,deriv=False):
        if(deriv==True):
            return 1 - np.square(x)
        return np.arctan(x)
    
    @staticmethod
    def identite(x,eta=1,deriv=False):
        if(deriv==True):
            return eta*1
        return eta*x
    
    @staticmethod
    def logistic(x,eta=1,deriv=False):
        if(deriv==True):
            return eta*x*(1-x)
        return 1/(1+np.exp(-eta*x))
    
    func = {
        'tanh':tanh.__func__,
        'identite':identite.__func__,
        'logistic':logistic.__func__,
        'sin':sin.__func__
    }
    
    def __init__(self,layers = [3,4,1],factiv='logistic', eta=1,seed=None,verbose=False):
        self.layers = layers
        self.seed = seed
        self.verbose = verbose
        self.values = []
        self.errors = []
        self.deltas = []
        self.lerror = []
        self.lerrorTest = []
        self.factiv = factiv
        self.eta = eta
        for val in self.layers:
            self.values.append(np.zeros(val))
            self.errors.append(np.zeros(val))
            self.deltas.append(np.zeros(val))
        
        np.random.seed(self.seed)
        
        self.weights = []
        for idx,val in enumerate(self.layers[:-1]):
            self.weights.append(2*np.random.random((self.layers[idx],self.layers[idx+1])) - 1)
    
    def activation(self,x,deriv=False):
        return self.func[self.factiv](x,eta=self.eta,deriv=deriv)
        
    def predict(self,X):
        self.values[0] = X
        for idx,val in enumerate(self.layers[:-1]):
            self.values[idx+1] = self.activation(np.dot(self.values[idx],self.weights[idx]))
        return self.values[-1]
    
    def backward(self,y):
        for idx1,val in enumerate(self.layers[::-1]):
            idx = len(self.layers)-1-idx1
            print(idx) if self.verbose else 1
            if idx == len(self.layers)-1:
                #self.errors[-1] = np.square(y - self.values[-1])/2
                self.errors[-1] = self.error(self.values[-1],y)
                self.lerror.append(np.mean(np.abs(self.errors[-1])))
            elif idx == 0:
                break
            else:
                self.errors[idx] = np.square(self.deltas[idx+1].dot(self.weights[idx].T))/2
            self.deltas[idx] = self.errors[idx]*self.activation(self.values[idx],deriv=True)
            self.weights[idx-1] += self.values[idx-1].T.dot(self.deltas[idx])
    
    def error(self,ypredict,y):
        return np.square(y - ypredict)/2
    
    def train(self,X,y,Xtest=None,ytest=None,cycle=1):
        for i in range(cycle):
            self.predict(X)
            self.backward(y)
            if not Xtest is None:
                self.lerrorTest.append(np.mean(np.abs(np.square(self.predict(Xtest)-ytest))/2))
            