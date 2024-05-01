import os
from PIL import Image


def better_remove(fp):
    try:
        os.remove(fp)
    except FileNotFoundError:
        pass

os.system('mkdir line_frames')
os.system('mkdir waterfalls')
fn='H:\\nc\\Valley of Vapors - Hot Springs National Park\\HotSpringsTape_4FSC-CX-CVBS.mkv'

#delete contents of in and out (burger place)
print('removing contents of /in/...')
for file in os.listdir('line_frames'):
    better_remove('line_frames/'+file)
    
fn2=fn.split('.')[0]
fn2=fn2.split('/')[-1]
fn2=fn2.split('\\')[-1]
for lineno in [40]:#,39,41]:#40,41,26,27,32,33,36,37,39,42]:#range(25,48):
    print('extracting line',lineno)
    os.system('ffmpeg -ss 18:10 -i "'+fn+'" -vf crop=in_w:1:0:'+str(lineno)+' line_frames/%04d.png -y')
    print('processing line',lineno)
    numframes=len(os.listdir('line_frames'))
    waterfall=Image.new(size=(910,numframes),mode='L')
    wf_px=waterfall.load()
    for frame in range(numframes):
        #print(frame)
        line=Image.open('line_frames/'+str(frame+1).zfill(4)+'.png')
        ln_px=line.load()
        for x in range(910):
            wf_px[x,frame]=ln_px[x,0]
    waterfall.save('waterfalls/waterfall_'+fn2+'_'+str(lineno).zfill(3)+'.png')