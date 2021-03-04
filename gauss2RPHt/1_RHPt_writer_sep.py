import sys
import linecache
import pandas 

f = open('irc.log', 'r')
linecounts = 0
indx_a1 = []
indx_a2 = []

indx_b1 = []
indx_b2 = []

indx_c1 = []
indx_c2 = []

indx_e = []
##构型有22个，第一个是过渡态，后面10个一组分别是forward和backward，最后一个重复，舍去
for line in f.readlines():
    linecounts +=1
    if ' Hessian after L703:' in line: 
        print ('Hsssian found in line: %d'%linecounts)
        #print (line)
        indx_a1.append(linecounts)
    if ' FrcOut:' in line: 
        print ('Hsssian end: %d'%linecounts)
        #print (line)
        indx_a2.append(linecounts)
##--------------------------------------------        
    if 'Number     Number       Type' in line:
        print ('geomerty found in line: %d'%linecounts)
        geomerty_counter1 = linecounts + 1
        indx_b1.append (geomerty_counter1)
    if 'Distance matrix' in line:
        print ('geometry end: %d'%linecounts)
        geomerty_counter2 = linecounts -1
        indx_b2.append (geomerty_counter2)
##--------------------------------------------        
    if 'Forces (Hartrees/Bohr)' in line:
        print ('gradient found in line: %d'%linecounts)
        gradient_counter1 = linecounts + 2        
        indx_c1.append(gradient_counter1)
    if 'Cartesian Forces:  Max' in line:
        print ('gradient end: %d'%linecounts)
        gradient_counter2 =  linecounts - 1
        indx_c2.append(gradient_counter2)
##--------------------------------------------        
    if 'E(UM062X)' in line:
        indx_e.append(linecounts)
f.close()

##test Hessian##
print ('Hessian starts')
len_a1 = len(indx_a1)
print(len_a1)
#print (indx_a1)
print ('Hessian ends')
len_a2 = len(indx_a2)
print(len_a2)
#print (indx_a2)

##test geometry
print ('Geometry starts')
len_b1 = len(indx_b1)
print(len_b1)
#print (indx_b1)
print ('Geometry ends')
len_b2 = len(indx_b2)
print(len_b2)
#print (indx_b2)

##test gradient
print ('gradient starts')
len_c1 = len(indx_c1)
print(len_c1)
#print (indx_c1)
print ('gradient ends')
len_c2 = len(indx_c2)
print(len_c2)
#print (indx_c2)

indx_c1

###Hessian output
for i in range(0,len(indx_a1)):
    fout1 = open('irc.log', 'r')
    opt_hess = open('./irc_files/hessian_%d.dat'%i,'w')
    opt_hess.write(' Hessian\n')
    index_out1 = 0
    for line in fout1.readlines():
        index_out1 += 1
        startp = indx_a1[i]
        endp = indx_a2[i]
        if (index_out1 > startp) and (index_out1 < endp):
            #print (line)
            opt_hess.write(line)
    opt_hess.close()    
###Hessian output ends

###Geometry output 循环遍历的范围需要-1，除去最后一个重复的构型
for i in range(0,len(indx_b1)-1):
    fout1 = open('irc.log', 'r')
    opt_geo = open('./irc_files/geo_%d.dat'%i,'w')
    opt_geo.write(' geometry\n')
    index_out1 = 0
    for line in fout1.readlines():
        index_out1 += 1
        startp = indx_b1[i]
        endp = indx_b2[i]
        if (index_out1 > startp) and (index_out1 < endp):
            #print (line)
            opt_geo.write(line)
    opt_geo.close()    
##Geometry output ends

##gradient output
for i in range(0,len(indx_c1)):
    fout1 = open('irc.log', 'r')
    opt_grad = open('./irc_files/gradient_%d.dat'%i,'w')
    opt_grad.write(' gradient\n')
    index_out1 = 0
    for line in fout1.readlines():
        index_out1 += 1
        startp = indx_c1[i]
        endp = indx_c2[i]
        if (index_out1 > startp) and (index_out1 < endp):
            #print (line)
            opt_grad.write(line)
    opt_grad.close()    
##gradient output ends

##energy output
opt_ene = open('./irc_files/energy.dat','w')
for i in range(0,len(indx_e)):
    fout1 = open('irc.log', 'r')
    opt_ene.write('E%d\t\t'%i)
    index_out1 = 0
    for line in fout1.readlines():
        index_out1 += 1
        startp = indx_e[i]
        if (index_out1 == startp):
            #print (line)
            ene_split = line.split ('  ')
            #print (ene_split)
            #len_ene = len(ene_split)
            #print (len_ene)
            print (ene_split[2])
            opt_ene.write('%s\n'%ene_split[2])
            #opt_ene.write(line) 
opt_ene.close()    
        
#df_ene = pd.read_csv('energy.dat',engine='python')

'''
theline = linecache.getline('irc.gjf',10)
print (index_1)

print (linecounts)
#for i in enumerate(f)
f = open('irc.gjf', 'r')
'''
