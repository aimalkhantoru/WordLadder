import json
from pythonds.graphs import Graph, Vertex
from pythonds.basic import Queue
from collections import defaultdict

class WordLadder:
    def __init__(self):
        self.dictionary = {}
        self.graph = Graph()
        self.wordContainer = {}
        self.fileName = 'dictionary.json'
        self.noChain = []
        self.frequency = {}
        
    def readDictionary(self,fileName):
        self.file  = open(self.fileName)
        self.dictionary = json.loads(self.file.read())
    
    
    def isNoChain(self,word):
        for n in range(len(word)):
            bucket = word[:n]+'$'+word[n+1:]
            if(len(self.wordContainer[bucket]) > 1):
                return False
        self.frequency.setdefault(0,0)
        self.frequency[0] += 1
        self.noChain.append(word)
        return True
    
    def parseDictionary(self):
        for word in self.dictionary:
            for n in range(len(word)):
                bucket = word[:n]+'$'+word[n+1:]
                
                if bucket in self.wordContainer:
                    self.wordContainer[bucket].append(word)
                else:
                    self.wordContainer[bucket] = [word]
                    
    def wordToGraph(self):
        for bucket in self.wordContainer.keys():
            for word1 in self.wordContainer[bucket]:
                for word2 in self.wordContainer[bucket]:
                    if word1 != word2:
                        self.graph.addEdge(word1,word2)
        
    def graphSearch(self,wordStart,wordEnd):
        start = self.graph.getVertex(wordStart)
        start.setDistance(0)
        start.setPred(None)
        vrtxQueue = Queue()
        vrtxQueue.enqueue(start)
        print(wordStart+"->",end='')
        
        while vrtxQueue.size() > 0:
            ls = []
            current = vrtxQueue.dequeue()
            prev = None;
            for neighbour in current.getConnections():
                if neighbour.getColor() == "white" :
                    neighbour.setColor("gray")
                    neighbour.setDistance(current.getDistance() + 1)
                    neighbour.setPred(current)                    
                    print(neighbour.getId()+"->",end='')
                    ##if neighbour.getId() == wordEnd :
                    #    print("\n\n\t",end='');
                    vrtxQueue.enqueue(neighbour)
            current.setColor("black")
              
    def test(self,wordStart):
        if self.isNoChain(wordStart):
            return False 
        start = self.graph.getVertex(wordStart)
        start.setDistance(0)
        start.setPred(None)
        vrtxQueue = Queue()
        vrtxQueue.enqueue(start)
        #print(wordStart,end='')
        d = defaultdict(list)
        
        while vrtxQueue.size() > 0:
            ls = []
            current = vrtxQueue.dequeue()
            
            #print(current.getId(),end='')
            prev = None;
            for neighbour in current.getConnections():
                if neighbour.getColor() == "white" :
                    neighbour.setColor("gray")
                    neighbour.setDistance(current.getDistance() + 1)
                    neighbour.setPred(current)
                    dist = neighbour.getDistance()
                    word = neighbour.getId()
                    d[dist].append(word)
                    #print("->"+neighbour.getId(),end='')
                    ls.append(neighbour);
                    ##if neighbour.getId() == wordEnd :
                    #    print("\n\n\t",end='');
                    #vrtxQueue.enqueue(neighbour)
            for i in range(len(ls)):
                vrtxQueue.enqueue(ls.pop(0))
            
                    
            current.setColor("black")
        outfile = open('Chains.txt','a')
        print("WORD : "+wordStart,file=outfile);
        for length in d.keys():
            print('----------------------- Length : {} -----------------------'.format(length),file=outfile )    
            self.frequency.setdefault(length,0)
            self.frequency[length] += len(d[length])
            
            for word in d[length]:
                vert = self.graph.getVertex(word)
                print(vert.getId(),end='',file=outfile)
                for count in range(length):
                    print(" -> " +  vert.getPred().getId(),end='',file=outfile)
                    #print()
                    vert = vert.getPred()
                print(file=outfile)
            print(file=outfile)
    def traverse(self,word):
        vertY = self.graph.getVertex(word)
        vertX = vertY
        while(vertX.getPred()):
            print(vertX.getId()+"->",end='')
            vertX = vertX.getPred()
        print(vertX.getId())
    
    def writeNoChain(self):
        outfile = open("noChain.txt",'w')
        
        for word in self.noChain:
            print(word,file=outfile,end=',')
            
    def frequencyDistribution(self):
        for key,value in self.frequency.items():
            print("{} -> {}".format(key,value))
                    
def main():
    l = WordLadder();
    l.readDictionary('dictionary.json')
    l.parseDictionary()
    l.wordToGraph()
    #l.test()
    for word in l.dictionary:
        l.test(word)
        
    l.writeNoChain()
    l.frequencyDistribution()
   # l.traverse("COLD")
    #l.traverse("COLD")


if __name__ == '__main__': main()

    