'''
Created on 2012-6-24

@author: avastms
'''
import re;

class PPPLog ():
    """Class For pppd Log Analysis."""
    RelevantPattern = '^.*pppd\[(?P<pid>\d+)\]: (?P<contant>.*)$';
    PatternList = ['^remote IP address (?P<ip>(\d{1,3}\.){3}\d{1,3})$',
                   '^Connect time (?P<time>\d+\.\d) minutes\.$',
                   '^Sent (?P<sent>\d+) bytes, received (?P<recv>\d+) bytes\.$'];
    Keys=('ip' , 'time' , 'sent' , 'recv') ;
    ReObjList = [];
    RawFileStr = '';
    ContantList = [];
    LogDict = {} ;
    ResultDict = {} ;
    SumDict = {} ;
    
    def __init__ (self,File) :
        try :
            with open(File) as filehandle :
                self.RawFileStr = filehandle.read();
        except :
            pass ;
#            print('Exception while reading log file.');
    
    def ReCompile (self) :
        """Compile RE Objects From Patterns."""
        self.ReObjList = [] ;
        for patt in self.PatternList :
            try :
                self.ReObjList.append(re.compile(patt));
            except :
                pass;
#                print('Exception While Compiling RE Objects.');
        return len(self.ReObjList);
    
    def Analyze (self):
        """Do Actual Analysis, Produce A Sub Dictionary."""
        self.ReCompile();
        matchobj = None ;
        try :
            if len(self.ContantList) == 0 :
                self.ContantList = re.findall(self.RelevantPattern,self.RawFileStr,re.M);
            else :
                return self ;
            del self.RawFileStr ;
        except :
            pass;
#            print('Exception while matching relevant.');
        def insertlog ():
                nonlocal matchobj , item , self ;
                if matchobj != None :
                    if list(matchobj.groupdict())[0] in self.LogDict[item[0]] :
                        item=list(item);
                        item[0] = str(- abs( int(item[0]) + 1 ));
                        if item[0] not in self.LogDict :
                            self.LogDict[item[0]] = {} ;
                        else :
                            pass;
                        insertlog();
                        return ;
                    else:
                        self.LogDict[item[0]] = dict ( self.LogDict[item[0]] , **matchobj.groupdict() ) ;
                else:
                    pass;
                return;
        for item in self.ContantList :
            for reobj in self.ReObjList :
                matchobj = reobj.match(item[1]);
                if item[0] not in self.LogDict :
                    self.LogDict[item[0]] = {} ;
                else :
                    pass;
                insertlog () ;
        return self;
     
    def Summrise (self) :
        """Do analysis from sublog into result dictionary."""
        self.ResultDict = {} ;
        for item in list(self.LogDict.values()) :
            try :
                if item[self.Keys[0]] not in self.ResultDict :
                    self.ResultDict[item[self.Keys[0]]] = {};
            except :
                pass;
#                print('Exception while finding prime key.');
                continue;
            for key in self.Keys[1:] :
                try :
                    if type(item[key]) == str and item[key].isdigit() : 
                        item[key] = int(item[key]) ;
                    elif type(item[key]) == str :
                        try :
                            item[key] = float(item[key]) ;
                        except :
                            pass;                        
                    if key not in self.ResultDict[item[self.Keys[0]]] :
                        self.ResultDict[item[self.Keys[0]]][key] = item[key] ;
                    else:
                        self.ResultDict[item[self.Keys[0]]][key] += item[key] ; 
                except :
                    pass;
#                    print('Expection while building result dict.');
                    break ;
        return self;

    def SumUp (self) :
        """
        Adds Up all Keys, stores values in SumDict.
        """
        if len(self.ResultDict) > 0 and len(self.SumDict) == 0 :
            for item in self.ResultDict.values():
                for key in self.Keys[1:]:
                    if key not in self.SumDict :
                        self.SumDict[key] = item[key] ;
                    else :
                        self.SumDict[key] += item[key] ;
        return self ;

    def Run (self) :
        return self.Analyze().Summrise().SumUp().SumDict ;
