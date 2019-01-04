#################################
#This code is made by: Hammer Heads
#ROV2016
################################
#import  the libraries that we need
import Blue  #import the blue that we make
import time 
import socket #import the lib. of ethernet
import smbus  #import the lib. of I2C
from numpy import interp #import function from numpy lib. this function mapping the values
import signal  #import the lib. that make interrupt when press Crtl-C
import sys     #import the sys. library to exit the programme
bus=smbus.SMBus(1)  #make object of i2c and set the setting

datago='0A0B0C0D'
dir1=0
dir2=0
dir3=0
s1=0
p1=0

try:
    down = Blue.Motor(0x2D)
    up = Blue.Motor(0x2E)
    left = Blue.Motor(0x2B)
    right = Blue.Motor(0x2C)
    latl = Blue.Motor(0x29)
    latr = Blue.Motor(0x2A)
    print "Motors Created. "
except:
    print "Motors did not create"
    print "try to write 'i2cdetect -y 1' in terminal"
    sys.exit(0)


counterser=55
#reading variables for led
state=0
#variables for reading the motor

upm=0
downm=0
rightm=0
leftm=0
latrm=0
latlm=0

temp=0.000
volt=0.000
water=0
depth=0.000

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
print "Client Created. "
port=888
ip="192.168.1.100" #computer address
#s.bind(('',555))

try:
    s.bind(('',555))
except:
    print "port of the device did not create"
    print "try to change the port in 's.bind(('',port))' with another number"
    sys.exit(0)



#List_Motors=[up,down,left,right,latr,latl]
List_values=[0 for sizelist in range(6)]
#List_str=['' for sizestr in range(6)]
List_udp_form=['A','B','C','D','E','F']


def signal_handler(signal, frame):
    print 'You pressed Ctrl+C!'
    s.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def mapp(va,fv,fv2,sv,sv2):
    return int(interp(va,[fv,fv2],[sv,sv2]))


def i2cwrite(ads,wr):
    bus.write_byte(ads,wr)

def i2cread(adds):
    rg=bus.read_byte(adds)
    return rg

def UDPsendC(text):
    s.sendto(text,(ip,port))
    #print "UDP Client send: ",text,"to :",ip 

def UDPreceC():
    de,addrr = s.recvfrom(1024)
    #print "Data received : ",de," from : " ,addr
    return de


def up_do_M(su1,su2):
    up.setspeed(su1)
    down.setspeed(su2)

def ri_le_M(su3,su4):
    right.setspeed(su3)
    left.setspeed(su4)

def lat_r_l_M(su5,su6):
    latr.setspeed(su5)
    latl.setspeed(su6)
'''
def Error_Motor():
    print "Motors State : "
    for err in range(0,6):
        List_Motors[err].update()
        #print err+1,'-',List_Motors[err].isAllive()
        print err+1,'-',"Motor with address  ",hex(List_Motors[err].add),"is work: ",List_Motors[err].isAllive()
'''
def strmanip(string):
    m1=int(string[string.index('A')+1:string.index('B')])
    m2=int(string[string.index('B')+1:string.index('C')])
    m3=int(string[string.index('C')+1:string.index('D')])
    m4=int(string[string.index('D')+1:string.index('E')])
    m5=int(string[string.index('E')+1:string.index('F')])
    m6=int(string[string.index('F')+1:string.index('X')])
    m7=int(string[string.index('X')+1:string.index('Y')])
    m8=int(string[string.index('Y')+1:string.index('Z')])
    m9=int(string[string.index('Z')+1:string.index('L')])
    m10=int(string[string.index('L')+1:string.index('T')])
    m11=int(string[string.index('T')+1:string.index('W')])
    m12=int(string[string.index('W',1)+1:string.index('S',1)])
    m13=int(string[string.index('S',1)+1:len(string)])

    List_values=[m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,m12,m13]
    #print "Motor A value : ",m1
    #print "Motor B value : ",m2
    #print "Motor C value : ",m3
    #print "Motor D value : ",m4
    #print "Motor E value : ",m5
    #print "Motor F value : ",m6
    return List_values
    

def optimize(v0,v1,v2,v3,v4,v5):
    sigm[0]=mapp(abs(v0),0,20000,0,11)
    sigm[1]=mapp(abs(v1),0,20000,0,11)
    sigm[2]=mapp(abs(v2),0,20000,0,11)
    sigm[3]=mapp(abs(v3),0,20000,0,11)
    sigm[4]=mapp(abs(v4),0,20000,0,11)
    sigm[5]=mapp(abs(v5),0,20000,0,11)
    alll=curm[0]+curm[1]+curm[2]+curm[3]+curm[4]+curm[5]
    mall=sigm[0]+sigm[1]+sigm[2]+sigm[3]+sigm[4]+sigm[5]
    if(alll>20):
        print "******************************************"
        print "******** Error ***************************"
        print "******************************************"

    lec=15
    if(mall!=0):
    	curm[0]=(sigm[0]/mall)*lec
    	curm[1]=(sigm[1]/mall)*lec
    	curm[2]=(sigm[2]/mall)*lec
    	curm[3]=(sigm[3]/mall)*lec
    	curm[4]=(sigm[4]/mall)*lec

    	curm[5]=(sigm[5]/mall)*lec

    sigout[0]=v0-(v0+1)*(mapp(curm[0],0,11,0,20000))
    sigout[1]=v1-(v1+1)*(mapp(curm[1],0,11,0,20000))
    sigout[2]=v2-(v2+1)*(mapp(curm[2],0,11,0,20000))
    sigout[3]=v3-(v3+1)*(mapp(curm[3],0,11,0,20000))
    sigout[4]=v4-(v4+1)*(mapp(curm[4],0,11,0,20000))
    sigout[5]=v5-(v5+1)*(mapp(curm[5],0,11,0,20000))
    List_view=[sigout[0],sigout[1],sigout[2],sigout[3],sigout[4],sigout[5]]
    return List_view
    

#Error_Motor()
#test
'''
while(1):
    print "cvsdvccsv"
    up.setspeed(2000)
    down.setspeed(2000)
    latr.setspeed(0)
    latl.setspeed(0)
    right.setspeed(0)
    left.setspeed(0)
    time.sleep(2)
    print "sdda"
    up.setzeros()
    down.setzeros()
    latr.setzeros()
    latl.setzeros()
    right.setzeros()
    left.setzeros()
    time.sleep(2)
    print"skgjvjfpvmvnf"
'''

while(1):
    UDPsendC(datago)
    data=UDPreceC()
    #print data
 
    strmanipv=strmanip(data)
    print data
    '''
    print "Motor A value : ",mapp(strmanipv[0],-32768,32768,spl,sph)
    print "Motor B value : ",mapp(strmanipv[1],-32768,32768,spl,sph)
    print "Motor C value : ",mapp(strmanipv[2],-32768,32768,spl,sph)
    print "Motor D value : ",mapp(strmanipv[3],-32768,32768,spl,sph)
    print "Motor E value : ",mapp(strmanipv[4],-32768,32768,spl,sph)
    print "Motor F value : ",mapp(strmanipv[5],-32768,32768,spl,sph)
    print "X value : ",strmanipv[6]
    print "Y value: ",strmanipv[7]
    print "Z value : ",strmanipv[8]
    print "L value : ",strmanipv[9]
    print "T value : ",strmanipv[10]
    print "---------------------------------------"
    '''
    '''
    rightm=mapp(strmanipv[1],-32768,32768,spl,sph)
    leftm=mapp(strmanipv[0],-32768,32768,spl,sph)
    upm=mapp(strmanipv[4],-32768,32768,spl,sph)
    downm=mapp(strmanipv[5],-32768,32768,spl,sph)
    latrm=mapp(strmanipv[2],-32768,32768,spl,sph)
    latlm=mapp(strmanipv[3],-32768,32768,spl,sph)
    '''
    rightm=strmanipv[1]
    leftm=strmanipv[0]
    upm=strmanipv[4]
    downm=strmanipv[5]
    latrm=strmanipv[2]
    latlm=strmanipv[3]
    state=strmanipv[10]
    #c1=up.currentwi()
    #c2=down.currentwi()
    #c3=latr.currentwi()
    #c4=latl.currentwi()
    #c5=right.currentwi()
    #c6=left.currentwi()
    #print
   
    if(strmanipv[10]==1):
	print"hhh"
        r1=i2cread(0x0A)
        #time.sleep(1)
        r1=i2cread(0x0A)
        r2=i2cread(0x0A)
        temp=float(((r1<<8)| r2)/100)
        print "temp = ",temp
        water=i2cread(0x0A)
        print "water sensor = ",water
        r1=i2cread(0x0A)
        r2=i2cread(0x0A)
        volt=float(((r1<<8) |r2)/100)
        print "volt = ",volt
        r1=i2cread(0x0C)
        r1=i2cread(0x0C)
        r2=i2cread(0x0C)
        depth=float(((r1<<8) |r2)/100)
        print "depth = ",depth
        r1=i2cread(0x0A)
        r2=i2cread(0x0A)
        datago=str(temp)+'A'+str(volt)+'B'+str(depth)+'C'+str(water)
        time.sleep(0.1)
    s1=strmanipv[9]
    if(s1!=p1):
    	i2cwrite(0x0A,strmanipv[9])
    #print strmanipv[9]
    
    #i2cwrite(0x0B,strmanipv[6])
    #i2cwrite(0x0B,strmanipv[7])
    #i2cwrite(0x0B,strmanipv[8])

    if(strmanipv[6]<0):
        dir1=1
    if(strmanipv[7]<0):
        dir2=1
    if(strmanipv[8]<0):
        dir3=1
    if(strmanipv[6]>0):
        dir1=0
    if(strmanipv[7]>0):
        dir2=0
    if(strmanipv[8]>0):
        dir3=0
   # i2cwrite(0x0B,int(str(dir3*1)+str(dir2*2)+str(dir1*4)))
    
    if(strmanipv[11]==1):
	i2cwrite(0x0C,12)
        print"barometer"
    
    counterser=counterser+strmanipv[12]
    #i2cwrite(0x0B,counterser)
    up.setspeed(upm)

    down.setspeed(downm)
    
    right.setspeed(rightm)
   
    left.setspeed(leftm)
    
    latr.setspeed(latrm)
    
    latl.setspeed(latlm)
    p1=strmanipv[9]

'''
while(1):
	r1=i2cread(0x0A)
	r2=i2cread(0x0A)
	print "temp = ",((r1<<8) |r2)/100
        r1=i2cread(0x0A)
        print "water sensor = ",r1
	r1=i2cread(0x0A)
	r2=i2cread(0x0A)
	print "current = ",((r1<<8) |r2)/100
        r1=i2cread(0x0A)
	r2=i2cread(0x0A)
	time.sleep(0.1)

'''


