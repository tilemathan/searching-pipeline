#!/afs/ipp/.cs/python_modules/amd64_sles11/python27/python/2.7.9/bin/python 
## MIGREV


import sys

SNcut=9.0
argv=sys.argv
for i in range(len(argv)): 
    arg = argv[i]
    if (arg == '-f'):
        FIN= argv[i+1]
    if (arg == '-s'):
        SNcut = int(argv[i+1])

file=open(FIN,'r')
print 'Reading in ',FIN
data = file.readlines()
file.close()
Nlines=len(data)
Count=0
fout = open (FIN+'.condensed-SN'+str(SNcut)+'.tmp','w')
fout2 = open (FIN+'removed-SN'+str(SNcut)+'.prd','w')

for i in range(Nlines):
    data2=data[i].split()
    newline= data[i].rstrip('\r\n')
    if (data2[0] == 'DM:'):
        #print 'found new DM at: ',newline
        fout.write(newline)
        fout.write('\n')
        fout2.write(newline)
        fout2.write('\n')

    else:
	try:    
        	CandSN1=float(data2[0])
        	CandSN2=float(data2[2])
        	CandSN3=float(data2[4])
        	CandSN4=float(data2[6])
        	CandSN5=float(data2[8])
        	print(CandSN1, CandSN2, CandSN3, CandSN4, CandSN5)

        	if ((CandSN1 >= SNcut) or (CandSN2 >= SNcut) or (CandSN3 >= SNcut) or (CandSN4 >= SNcut) or (CandSN5 >= SNcut)):
        	#if (CandSN1 >= SNcut):
            	#print 'GOOD:',newline
            		fout.write(newline)
            		fout.write('\n')
        	else:
            	#print 'BAD:',newline
            		fout2.write(newline)
            		fout2.write('\n')
	except:
		print("PROBLEM-PASSED----------------------------------------------------------")
		pass

fout.close()
fout2.close()



file = open(FIN+'.condensed-SN'+str(SNcut)+'.tmp','r')
print 'Reading in ',FIN,'.condensed-SN'+str(SNcut)+'.prd'
data = file.readlines()
file.close()
Nlines=len(data)
Count=0
fout = open (FIN+'.condensed-SN'+str(SNcut)+'.prd','w')
fout2  = open ('temp.prd','w') 

for i in range(Nlines):
    data2=data[i].split()
    newline= data[i].rstrip('\r\n')
    if ((data2[0] == 'DM:') and ( int(i) != int(Nlines) -1 ) ):
        #print 'found new DM at: ',newline
        datanext = data[i+1].split()
        if (datanext[0] == 'DM:'):
            #print 'reject this line:',newline
            fout2.write(newline)
            fout2.write('\n')
        else:
            #print 'GOOD:',newline  
            fout.write(newline)
            fout.write('\n')
          
    elif ((data2[0] == 'DM:') and (int(i) == int(Nlines) -1 )):
        print "Reached last line:"+str(data2[0])
               
            
    else: 
        fout.write(newline)
        fout.write('\n')


fout.close()
fout2.close()
