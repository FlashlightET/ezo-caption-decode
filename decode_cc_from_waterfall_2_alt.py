import pprint
import os
import json
import time
from PIL import Image
from tqdm import tqdm
#infile=Image.open('waterfalls/waterfall_korone_flac_2_040.png')
#infile=Image.open('waterfalls/waterfall_winknewstest_LUMA_040.png')
#infile=Image.open('waterfalls/waterfall_pbs_maybe_test_5_040.png')
infile=Image.open('waterfalls/waterfall_HotSpringsTape_4FSC-CX-CVBS_040.png').convert('L')

FontImg=Image.open('19x36TestFont.png').convert('RGBA')
FontCharW=19
FontCharH=36

ActualFontCharW=12
ActualFontCharH=24

#408x360
screen=Image.new(size=(408,360),mode='RGBA')

fontChars=[]
for y in range(8):
    for x in range(32):
        q=FontImg.crop((x*FontCharW,y*FontCharH,(x*FontCharW)+FontCharW,(y*FontCharH)+FontCharH))
        q=q.resize((ActualFontCharW,ActualFontCharH))
        fontChars.append(q)
        #print(q.width)

q=infile.load()

def scale_bpwp(value,bp,wp):
    try:
        return min(max(int(((value-bp) / (wp-bp))*255),0),255)
    except:
        #print('aah!!')
        #print('WHITE: '+str(wp)+'| BLACK: '+str(bp)+'| VALUE: '+str(value))
        return value

def getstuff(inn,idx,leng):
    return inn[idx:idx+leng]
    
def bin2dec(binart):
    return int(binart,base=2)
mode='Line38'
mode='Line43'
NotFinal=''

buffer=[0]*15*34
buffer2=buffer
print(buffer)

#time.sleep(4)
cursorpos=0
bufferMode=0
recData=[]
recData2=[]
recDataTmp=[]
ascData={
    'nul':'                                ',
    'end':'                                ',
    'Station.CallLetters': '        ', 
    'Station.StationName':'                                ',
    'Current.ProgramID':'                                ',
    'Current.ProgramLength':'                                ',
    'Current.ProgramName':'                                ',
    'Current.ProgramType':'                ',
    
    }
    
    
# ='Station.CallLetters'
            # dataPos=0
        # elif b1==5 and b2==2:  #Control 05 (Station), Type 02 (StationName)
            # packetType='Station.StationName'
            # dataPos=0
        # elif b1==1 and b2==2:  #Control 01 (CurrentProgram), Type 01 (ProgramID)
            # packetType='Current.ProgramID'
            # dataPos=0
        # elif b1==1 and b2==2:  #Control 01 (CurrentProgram), Type 02 (ProgramLength)
            # packetType='Current.ProgramLength'
            # dataPos=0
        # elif b1==1 and b2==3:  #Control 01 (CurrentProgram), Type 03 (ProgramName)
            # packetType='Current.ProgramName'
            # dataPos=0
        # elif b1==1 and b2==4:  #Control 01 (CurrentProgram), Type 04 (ProgramType)
            # packetType='Current.ProgramType'
    
    
caps_text=[{'frame': 0,'text': ''}]
    
cap_text=''
    
packetType='nul'
dataPos=0
#ascData[packetType]=''




cx_center=0 #a selected frame from the cx capture
st_center=0 #corresponding frame on startech capture

cx_offset=cx_center-st_center

#list of frames dropped by cvbs-decode
#corresponding frame in ref video that is subtracted by the ref's offset from the cx capture
FrameDropTable_=[]

FrameDropTable=[i+cx_offset for i in FrameDropTable_]
trueFrame=-1


#what frame in the ST capture the CX capture starts
startOfs=0


for y in tqdm(range(infile.height)):


    trueFrame+=1
    if trueFrame in FrameDropTable:
        print('frame drop')
        trueFrame+=1


    try:
        dummy=ascData[packetType]
    except:
        ascData[packetType]=' '*32
    dataLen=17
    dataStart=395
    dataEnd=878
    
    dataStart=389
    dataEnd=872
    
    
    dataStart=398
    dataEnd=880
    
    #get black point
    temp=[]
    for x in range(363,363+28):
        temp.append(q[x,y])
    bp=sum(temp)/len(temp)

    #get white point
    temp=[]
    for x in range(399,399+24):
        temp.append(q[x,y])
    wp=sum(temp)/len(temp)
    
    
    dataPoints=[]
    for i in range(dataLen):
        dataPoints.append(int(((((dataEnd-dataStart)/dataLen)*i)+dataStart)+(((dataEnd-dataStart)/dataLen)/2)))
    data=[]
    for x in dataPoints:
        v=0
        if scale_bpwp(q[x,y],bp,wp)>127: v=1
        data.append(v)
    data=''.join([str(gay) for gay in data])
    #print(data)
    Char1=getstuff(data,1,8)[::-1]
    Char2=getstuff(data,9,8)[::-1]
    cmd=Char1+Char2
    #print(Char1,Char2)
    
    char1=int(Char1[1:],base=2)
    char2=int(Char2[1:],base=2)
    
    #CONTROL: bits 0 and 8 are always parity bits, bit 4 is always channel bit
    
    #CONTROL: bits 1,2 always 0; bit 3 always 1; bit 9 always 1
    if cmd[1]=='0' and cmd[2]=='0' and cmd[3]=='1' and cmd[9]=='1':
        pass#print('Preamble address code')
    
    if char1==int('14',base=16) or char1==int('15',base=16):
        if char2==int('20',base=16):
            #print('resume caption loading')
            #if cap_text!='': caps_text.append({'frame': y,'text': cap_text})
            
            #cap_text=''
            
            if caps_text[-1]['text']!='': caps_text.append({'frame': trueFrame,'text': ''})
            
            pass
        if char2==int('21',base=16):
            #print('backspace')
            cap_text=cap_text[:-1]
            pass
        if char2==int('22',base=16):
            #print('alarm off')
            pass
        if char2==int('23',base=16):
            #print('alarm on')
            pass
        if char2==int('24',base=16):
            #print('delete to end of row')
            pass
        if char2==int('25',base=16):
            #print('roll up 2')
            bufferMode=0
            pass
        if char2==int('26',base=16):
            #print('roll up 3')
            bufferMode=0
            pass
        if char2==int('27',base=16):
            #print('roll up 4')
            bufferMode=0
            pass
        if char2==int('28',base=16):
            #print('flashes captions on')
            pass
        if char2==int('29',base=16):
            #print('resume direct captioning')
            pass
        if char2==int('2A',base=16):
            #print('text restart')
            pass
        if char2==int('2B',base=16):
            #print('resume text display')
            pass
        if char2==int('2C',base=16):
            #print('erase display memory')
            pass
        if char2==int('2D',base=16):
            #print('carriage return')
            #cap_text+='\n'
            caps_text[-1]['text']=caps_text[-1]['text']+'\n'
            
        if char2==int('2E',base=16):
            pass
            #print('erase non displayed memory')
        if char2==int('2F',base=16):
            #print('end of caption')
            pass
        if char2>int('2F',base=16):
            try:
                if caps_text[-1]['text'][-1]!='\n': caps_text[-1]['text']=caps_text[-1]['text']+'\n'
            except IndexError:
                pass
    
    for brer in range(34):
        buffer[brer]=buffer[brer+1]
    for brer in range(34):
        buffer[brer]=buffer[brer+1]
    buffer[32]=bin2dec(Char1[1:])
    buffer[33]=bin2dec(Char2[1:])
    
    
    
    
    recData.append(bin2dec(Char1[1:]))
    recData.append(bin2dec(Char2[1:]))
    b1=bin2dec(Char1[1:])
    b2=bin2dec(Char2[1:])
    

            
    
    
    if b1==15:
        sghsftghjsfgjhf=list(ascData[packetType])
        for beeb in range(len(sghsftghjsfgjhf)):
            if beeb>=dataPos:
                sghsftghjsfgjhf[beeb]=' '
        ascData[packetType]=''.join(sghsftghjsfgjhf)
        
        
        
        packetType='end'
        for grg in recDataTmp:
            recData2.append(grg)
        for grg in range(64-len(recDataTmp)):
            recData2.append(255)
        recDataTmp=[]
        
        
    else:
        if b1==5 and b2==1:    #Control 05 (Station), Type 01 (CallLetters)
            packetType='Station.CallLetters'
            dataPos=0
        elif b1==5 and b2==2:  #Control 05 (Station), Type 02 (StationName)
            packetType='Station.StationName'
            dataPos=0
        elif b1==5 and b2==3:  #Control 05 (Station), Type 03 (TapeDelay)
            packetType='Station.TapeDelay'
            dataPos=0
        elif b1==5 and b2==4:  #Control 05 (Station), Type 04 (Unknown)
            packetType='Station.Unknown'
            dataPos=0
        elif b1==13 and b2==13:  #Control 13 (Unknown), Type 13 (Unknown)
            packetType='Unknown.Unknown'
            dataPos=0
        elif b1==7 and b2==1:  #Control 07 (Misc), Type 01 (Time)
            packetType='Misc.Time'
            dataPos=0
        elif b1==7 and b2==2:  #Control 07 (Misc), Type 02 (ImpulseCaptureID)
            packetType='Misc.ImpulseCaptureID'
            dataPos=0
        elif b1==7 and b2==3:  #Control 07 (Misc), Type 03 (SupplementalDataLocation)
            packetType='Misc.SupplementalDataLocation'
            dataPos=0
        elif b1==7 and b2==4:  #Control 07 (Misc), Type 04 (TimeZone)
            packetType='Misc.TimeZone'
            dataPos=0
        elif b1==7 and b2==5:  #Control 07 (Misc), Type 05 (OutOfBandChannelNumber)
            packetType='Misc.OutOfBandChannelNumber'
            dataPos=0
        elif b1==1 and b2==2:  #Control 01 (CurrentProgram), Type 01 (ProgramID)
            packetType='Current.ProgramID'
            dataPos=0
        elif b1==1 and b2==2:  #Control 01 (CurrentProgram), Type 02 (ProgramLength)
            packetType='Current.ProgramLength'
            dataPos=0
        elif b1==1 and b2==3:  #Control 01 (CurrentProgram), Type 03 (ProgramName)
            packetType='Current.ProgramName'
            dataPos=0
        elif b1==1 and b2==4:  #Control 01 (CurrentProgram), Type 04 (ProgramType)
            packetType='Current.ProgramType'
            dataPos=16
        elif b1==1 and b2==5:  #Control 01 (CurrentProgram), Type 05 (ProgramRating)
            packetType='Current.ProgramRating'
            dataPos=0
        elif b1==1 and b2==6:  #Control 01 (CurrentProgram), Type 06 (ProgramAudio)
            packetType='Current.ProgramAudio'
            dataPos=0
        elif b1==1 and b2==7:  #Control 01 (CurrentProgram), Type 07 (ProgramCaption)
            packetType='Current.ProgramCaption'
            dataPos=0
        elif b1==1 and b2==8:  #Control 01 (CurrentProgram), Type 08 (ProgramCGMSA)
            packetType='Current.ProgramCGMSA'
            dataPos=0
        elif b1==1 and b2==9:  #Control 01 (CurrentProgram), Type 09 (ProgramAspect)
            packetType='Current.ProgramAspect'
            dataPos=0
        elif b1==1 and b2==16:  #Control 01 (CurrentProgram), Type 16..23 (ProgramDesc)
            packetType='Current.ProgramDesc1'
            dataPos=0
        elif b1==1 and b2==17:  #Control 01 (CurrentProgram), Type 16..23 (ProgramDesc)
            packetType='Current.ProgramDesc2'
            dataPos=0
        elif b1==1 and b2==18:  #Control 01 (CurrentProgram), Type 16..23 (ProgramDesc)
            packetType='Current.ProgramDesc3'
            dataPos=0
        elif b1==1 and b2==19:  #Control 01 (CurrentProgram), Type 16..23 (ProgramDesc)
            packetType='Current.ProgramDesc4'
            dataPos=0
        elif b1==1 and b2==20:  #Control 01 (CurrentProgram), Type 16..23 (ProgramDesc)
            packetType='Current.ProgramDesc5'
            dataPos=0
        elif b1==1 and b2==21:  #Control 01 (CurrentProgram), Type 16..23 (ProgramDesc)
            packetType='Current.ProgramDesc6'
            dataPos=0
        elif b1==1 and b2==22:  #Control 01 (CurrentProgram), Type 16..23 (ProgramDesc)
            packetType='Current.ProgramDesc7'
            dataPos=0
        elif b1==1 and b2==23:  #Control 01 (CurrentProgram), Type 16..23 (ProgramDesc)
            packetType='Current.ProgramDesc8'
            dataPos=0
            
        else:
            recDataTmp.append(bin2dec(Char1[1:]))
            recDataTmp.append(bin2dec(Char2[1:]))
            if packetType!='end' and packetType!='nul':
                if packetType=='Current.ProgramType':
                    #print('program type')
                    programTypes=[
                        (int('20',base=16), 'Education'.ljust(16)),
                        (int('21',base=16), 'Entertainment'.ljust(16)),
                        (int('22',base=16), 'Movie'.ljust(16)),
                        (int('23',base=16), 'News'.ljust(16)),
                        (int('24',base=16), 'Religious'.ljust(16)),
                        (int('25',base=16), 'Sports'.ljust(16)),
                        (int('26',base=16), 'Other'.ljust(16)),
                        (int('27',base=16), 'Action'.ljust(16)),
                        (int('28',base=16), 'Advertisement'.ljust(16)),
                        (int('29',base=16), 'Animated'.ljust(16)),
                        (int('2A',base=16), 'Anthology'.ljust(16)),
                        (int('2B',base=16), 'Automobile'.ljust(16)),
                        (int('2C',base=16), 'Awards'.ljust(16)),
                        (int('2D',base=16), 'Baseball'.ljust(16)),
                        (int('2E',base=16), 'Basketball'.ljust(16)),
                        (int('2F',base=16), 'Bulletin'.ljust(16)),
                        ]
                    try:
                        grgr=0
                        for grgr in range(255):
                            if programTypes[grgr][0]==b1: 
                                #print(ascData['Current.ProgramType'])
                                ascData['Current.ProgramType']=programTypes[grgr][1]
                                
                                #print(ascData['Current.ProgramType'])
                                #print(programTypes[grgr][1])
                                break
                        
                    except IndexError:
                        print('indexerror')
                    #print('!!!'*50)
                    
                    #print(json.dumps(ascData, indent=4))
                    #print('!!!'*50)
                    
                    
                    
                else:
                    
                    #print(packetType)
                    sghsftghjsfgjhf=list(ascData[packetType])
                    try:
                        sghsftghjsfgjhf[dataPos]=chr(b1)
                        sghsftghjsfgjhf[dataPos+1]=chr(b2)
                    except IndexError:
                        pass
                    ascData[packetType]=''.join(sghsftghjsfgjhf)
                    #ascData[packetType]+=chr(b1)+chr(b2)
                    #print(ascData)
                    #pprint.pp(ascData)
                    #print(json.dumps(ascData, indent=4))
                    curse2=0
                    keez=list(ascData.keys())
                    for curse2 in range(len(keez)):
                        try:
                            grump=[]
                            curse=0
                            for grump2 in ascData[keez[curse2]][:34]:
                                grump.append(bin(ord(grump2))[2:].zfill(8))
                                try:
                                    buffer[((curse2+1)*34)+curse]=ord(grump2)
                                except IndexError:
                                    pass
                                curse+=1
                            #print(grump)
                        except KeyError:
                            pass
                       
                    dataPos+=2
                
    LegalCharacters='1234567890-=[]\\;\',./<>?:"{}|+_)(*&^%$#@! QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm~`'
                
    #bit 1 or 2 on always = show two chars
    if cmd[1]=='1' or cmd[2]=='1':
        #cap_text+=chr(bin2dec(Char1[1:]))
        #cap_text+=chr(bin2dec(Char2[1:]))


        c1=chr(bin2dec(Char1[1:]))
        c2=chr(bin2dec(Char2[1:]))
        if c1 in LegalCharacters: caps_text[-1]['text']=caps_text[-1]['text']+c1
        if c2 in LegalCharacters: caps_text[-1]['text']=caps_text[-1]['text']+c2
    
    #print(caps_text[-1])

#with open('x:/nc/RecData.bin','wb') as f:
    #f.write(bytes(recData))
    
caps_text.append({'frame': caps_text[-1]['frame']+30, 'text': '[captions end]'})
    
srt=[]
    
for i in range(len(caps_text)-1):
    print(caps_text[i])
    capstart=caps_text[i]['frame']+startOfs
    capend=caps_text[i+1]['frame']+startOfs
    def frame2captime(frame):
        ms=int(round(((frame%29.97)/29.97)*1000))
        sc=int((frame//29.97)%60)
        mn=int(((frame//29.97)//60)%60)
        hr=int(((frame//29.97)//60)//60)
        
        return f'{str(hr).zfill(2)}:{str(mn).zfill(2)}:{str(sc).zfill(2)},{str(ms).zfill(3)}'
    srt.append(str(i+1))
    srt.append(frame2captime(capstart)+' --> '+frame2captime(capend))
    srt.append(caps_text[i]['text'])
    srt.append('')
    
    
for i in srt:
    print(i)
        
    
with open('h:\\nc\\4fsc_bath.srt','w') as f:
    f.write('\n'.join(srt))
    
with open('h:/nc/RawCaptionData_bath.bin','wb') as f:
    f.write(bytes(recData))
    
