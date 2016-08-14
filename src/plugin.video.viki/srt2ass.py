#!user/bin/env python
#-*- coding:utf-8 -*-

import sys
import math
import random
def coded(str):
    try:
        try:
            try:
                try:
                    try:
                        ans=str.decode('gb2312')
                    except:
                        ans=str.decode('gbk')
                except:
                    ans=str.decode('cp936')
            except:
                ans=str.decode('utf-8')
        except:
            ans=str.decode('big5')
    except:
        ans=None
    return ans
	
def returntime(t):
	hr= math.floor(t/3600)
	mn=t / 60 % 60
	s=t % 60
	return (hr, mn, s, 0)
	
def jsontoass(data,merge):
    style2="Top"
    timectr=-1
    diffrang = [2000,2300,2500,2700,3000,3300,3600]
    timediff=random.choice(diffrang)
    print "timediff="+str(timediff)
    for i, item in enumerate(data):
		#print item.encode('utf-8')
		starttime=int(item['time'])
		if(timectr==-1 or starttime-timectr > timediff):
			merge.append((returntime(starttime/1000), returntime(starttime/1000+4), (item["user"]["username"] +":  "+ item["value"]).encode('utf8'),style2))
			timectr=starttime
    return merge
	
def main(name,jdata):
    import re
    extract=re.compile('\\d+\\s+([0-9:,]+)\\s--?>\\s([0-9:,]+)\\s+(.*?)\\r?\\n')
    gettime=re.compile('(\\d+):(\\d+):(\\d+),(\\d+)')
    style1="Bot"
    def trs(tim):
        i,j,k,t=[int(x) for x in gettime.match(tim).groups()]
        t=t/10+1 if t%10>=5 else t/10
        if t>99:
            k,t=k+1,0
        if k>59:
            j,k=j+1,0
        if j>59:
            i,j=i+1,0
        return (i,j,k,t)

    with open(name,'rb') as file:
        data=coded(file.read())
        if not data:return
        sub=extract.findall(data)
        n1,n2,n3=sub.pop(0)
        merge=[(trs(n1),trs(n2),n3,style1)]
        for n1,n2,n3 in sub:
            p1,p2,p3,p4=merge[-1]
            n1,n2=trs(n1),trs(n2)
            if p3==n3:
                if p2[0]==n1[0] and p2[1]==n1[1] and p2[2]==n1[2]:
                    if n1[3]-p2[3]<=5:
                        merge[-1]=(p1,n2,p3,style1)
                        continue
            merge.append((n1,n2,n3,style1))
    merge=jsontoass(jdata,merge)
    lst=name.split('.')
    lst[-1]='ass'
    name='.'.join(lst)

    merge2= sorted(merge, key=lambda tup: tup[0])
    with open(name,'w') as file:
        file.write('''[Script Info]
ScriptType: v4.00+
Collisions: Normal
PlayDepth: 0
Timer: 100,0000
Video Aspect Ratio: 0
WrapStyle: 0
ScaledBorderAndShadow: no

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Default,Arial,16,&H00FFFFFF,&H00FFFFFF,&H80000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,0,2,10,10,10,0
Style: Top,Arial,14,&H0000FFFF,&H00FFFFFF,&H80000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,0,8,10,10,10,0
Style: Mid,Arial,16,&H0000FFFF,&H00FFFFFF,&H80000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,0,5,10,10,10,0
Style: Bot,Arial,16,&H00F9FFF9,&H00FFFFFF,&H80000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,0,2,10,10,10,0

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
        )
        for n1,n2,n3,n4 in merge2:
            n1='%01d:%02d:%02d.%02d'%n1
            n2='%01d:%02d:%02d.%02d'%n2
            line="Dialogue: 0,%s,%s,%s,,0000,0000,0000,,%s\r\n"%(n1,n2,n4,n3.replace("<i>","{\i1}").replace("</i>","{\i0}").replace("<br>","\\N"))
            #line='Dialogue: 0,%s,%s,*Default,Bot,0000,0000,0000,,%s'%(n1,n2,n3)
            try:
				line=line.encode('utf-8')
            except: pass
            file.write(line)

if __name__=='__main__':
    if len(sys.argv)>1:
        for name in sys.argv[1:]:
            main(name)