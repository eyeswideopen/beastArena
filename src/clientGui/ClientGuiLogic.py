import datetime, time

"""
module for logical calculation stuff needed by gui implementations
"""

def parseStartTime(startTime):
    """
    creates a datetime object from a string, generated by time.asctime
    @param startTime string: time string in format: %a %b %d %H:%M:%S %Y
    """
   
    currentDay=datetime.datetime.now().day
    currentMonth=datetime.datetime.now().month

    try:
        seconds=float(startTime)
        t=time.time() + seconds
        timeString = time.ctime(t)
        timeStringSplit= timeString[11:]
        return datetime.datetime.strptime(timeStringSplit,'%H:%M:%S %Y').replace(month=currentMonth,day=currentDay)
    except:
        try:        
            t= str(startTime)[11:]
            return datetime.datetime.strptime(t,'%H:%M:%S %Y').replace(month=currentMonth,day=currentDay)
        except:
            return

def readServersFromFile(comboBox,serverMap):
    """
    reads server addresses from a file and adds them to an passed combo box a map
    @param comboBox: combo box to insert an item containing the servers host and port
    @param serverMap: map to insert an value containing the servers address, port and path of certificate  
    """
    try:
        serverFile = open('../clientGui/resources/serverAddresses.txt', 'r')
        servers = serverFile.readlines()
        for i in range(len(servers)):
            split = servers[i].rstrip().split(':', 3)
            if len(split) == 3:
                hostPort = split[0] + ':' + split[1]
                cert = split[2]
                comboBox.insertItem(i, hostPort)
                serverMap[hostPort] = (split[0], split[1], cert)
        serverFile.close()
    except Exception:
        pass

def appendServerToFile(server):
    """
    writes a server address into a file
    """
    try:
        serverFile = open('../clientGui/resources/serverAddresses.txt', 'r')
        servers = serverFile.readlines()
    except Exception:
        servers = []
        
    serversWrite = open('../clientGui/resources/serverAddresses.txt', 'a')
    
    if server not in servers:
        serversWrite.write(str(server))
    serversWrite.close()
    try:
        serverFile.close()
    except:
        pass    

def updateWaitingProgressBar(bar): 
    """
    updates the value of a passed progress bar, invert the appearance if the value reaches hundred and zero
    @param bar: progress bar which value should be changed
    """
    progressValue=bar.value()
    if progressValue < 100 and str(bar.statusTip())=='forward':
        progressValue += 1
        bar.setInvertedAppearance(False)
    else:
        bar.setInvertedAppearance(True)
        bar.setStatusTip('backward')
        progressValue -= 1
        if progressValue == 0:
            bar.setStatusTip('forward')
    bar.setValue(progressValue)        

def updateProgressBar(bar, countdownBarStartTime, gameStartTime):
    totalWaitingTime = timedeltaToTotalSeconds(gameStartTime - countdownBarStartTime)
    elapsedWaitingTime = totalWaitingTime - timedeltaToTotalSeconds(gameStartTime - datetime.datetime.now())
    bar.setValue(elapsedWaitingTime/totalWaitingTime*100)
    
def timedeltaToTotalSeconds(td): 
    return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 1e6) / 1e6

if __name__=='__main__':
    parseStartTime(12)

