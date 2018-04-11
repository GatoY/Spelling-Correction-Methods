c=[]
m=[]
count =0
asd=0
with open('correct.txt') as cf:
	with open('misspell.txt') as mf:
		with open('dictionary.txt') as df:
	        	lines = df.readlines()
        		mline = mf.readline()
        		cline = cf.readline()
            	
			while(cline!=''):
                		asd = asd+1
				if cline in lines:
					count=count + 1
                    			c.append(cline)
                    			m.append(mline)
                		cline = cf.readline()
                		mline = mf.readline()
print asd
print count
with open('c_edit.txt', 'w+') as f:
	for i in c:
		f.write(i)

with open('m_edit.txt','w+') as f:
	for i in m:
		f.write(i)

			
