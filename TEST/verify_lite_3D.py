#import matplotlib.pyplot as plt
import numpy as np
from numpy import linalg 
import sys
print(np.version.version)


path_ref='/glade/u/home/cmille73/reg_test/CPU_Master/ref/cheyenne/cpu/intel/MURaM_main/TEST/Test_3D/3D/'
path_test='/glade/u/home/cmille73/reg_test/val_test/MURaM_main/TEST/Test_3D/3D/'



iter=50

thresh = 1e-4

trans=[0,1,2]

def inttostring(ii,ts_size=6):

  str_num = str(ii)

  for bb in range(len(str_num),ts_size,1):
    str_num = '0'+str_num
  
  return str_num

def read_var_3d(dir,var,iter,layout=None):
  
  h = np.loadtxt(dir+'Header.'+inttostring(iter,ts_size=6))

  size = h[0:3].astype(int)
  dx   = h[3:6]
  time = h[6]
                               
  tmp = np.fromfile(dir+var+'.'+ inttostring(iter,ts_size=6),dtype=np.float32)
  tmp = tmp.reshape([size[2],size[1],size[0]])
    
  if layout != None :
      tmp = tmp.transpose(layout)
  
  return tmp,dx,size,time

def hdiff(var1,var2,minval):
    var1_m = np.mean(np.abs(var1),axis=(0,1))
    diff_m = np.mean(np.abs(var1-var2),axis=(0,1))
    diff_m = diff_m/np.maximum(var1_m,minval)
    return diff_m

rho_ref,dx,size,time=read_var_3d(path_ref,'result_prim_0',iter,trans)
rho_test,dx,size,time=read_var_3d(path_test,'result_prim_0',iter,trans)

T_ref,dx,size,time=read_var_3d(path_ref,'eosT',iter,trans)
T_test,dx,size,time=read_var_3d(path_test,'eosT',iter,trans)

V_ref,dx,size,time=read_var_3d(path_ref,'result_prim_1',iter,trans)
V_test,dx,size,time=read_var_3d(path_test,'result_prim_1',iter,trans)

E_ref,dx,size,time=read_var_3d(path_ref,'result_prim_4',iter,trans)
E_test,dx,size,time=read_var_3d(path_test,'result_prim_4',iter,trans)

B_ref,dx,size,time=read_var_3d(path_ref,'result_prim_5',iter,trans)
B_test,dx,size,time=read_var_3d(path_test,'result_prim_5',iter,trans)

Qrad_ref,dx,size,time=read_var_3d(path_ref,'Qtot',iter,trans)
Qrad_test,dx,size,time=read_var_3d(path_test,'Qtot',iter,trans)

Jtot_ref,dx,size,time=read_var_3d(path_ref,'Jtot',iter,trans)
Jtot_test,dx,size,time=read_var_3d(path_test,'Jtot',iter,trans)

Qcor_ref,dx,size,time=read_var_3d(path_ref,'QxCor',iter,trans)
Qcor_test,dx,size,time=read_var_3d(path_test,'QxCor',iter,trans)

cond_ref,dx,size,time=read_var_3d(path_ref,'result_prim_8',iter,trans)
cond_test,dx,size,time=read_var_3d(path_test,'result_prim_8',iter,trans)

#if iter > 0:
if 0:
    Qamb_ref,dx,size,time=read_var_3d(path_ref,'Qamb',iter,trans)
    Qamb_test,dx,size,time=read_var_3d(path_test,'Qamb',iter,trans)
else:
    Qamb_ref=np.zeros(size)
    Qamb_test=np.zeros(size)

ref=[rho_ref,T_ref,V_ref,E_ref,B_ref,cond_ref,Qrad_ref,Qcor_ref,Qamb_ref]
test=[rho_test,T_test,V_test,E_test,B_test,cond_test,Qrad_test,Qcor_test,Qamb_test]
names=['Density','Temperature','Velocity','Energy','Magnetic Field','Conduction','Q_Radiation','Q_Corona','Q_Ambipolar']
plot_range_min=[1e-15,1e3,1e4,0.1,0.1,1e3,1e-4,1e-4,1e-4]
minval=[1e-20,1e-20,1e-20,1e-20,1,1e-20,1e-20,1e-20,1e-20]

print("Comparing Iteration: ", iter)

print("Max Relative Error")
for v in range(9):
    hdifference=np.amax(hdiff(ref[v],test[v],minval[v]))
    if hdifference > thresh:
        sys.stdout.write("\033[1;31m")
    else:
        sys.stdout.write("\033[0;32m")
    print(names[v].ljust(14), ":" ,hdifference)

sys.stdout.write("\033[0;0m")

print("\n\n")
print("Linf norm")
for v in range(9):

    linfdt = linalg.norm(ref[v],np.inf,(0,1))
    linfd = np.where(linfdt<1e-5,1e-5,linfdt)
    linfn = np.amax(linalg.norm(test[v]-ref[v],np.inf,(0,1))/linfd)
     
    if linfn > thresh:
        sys.stdout.write("\033[1;31m")
    else:
        sys.stdout.write("\033[0;32m")
    print(names[v].ljust(14), ":" ,linfn)

    #if hdifference > thresh:
#	hd = hdiff(ref[v],test[v],minval[v])
#        print(hd.size)
#       print(ref[v].shape)
#        print("Values over thresh: ",hd[hd>thresh])
#        print("Indices           : ",np.nonzero(hd > thresh))
#        
#        for x in range(ref[v].shape[0]):
#           for y in range(ref[v].shape[1]):
#              for z in range(ref[v].shape[2]):
#                adiff = ref[v][x][y][0]-test[v][x][y][0]
#                if adiff > 1e-6:
#                  print("X: ", x, " Y: ",y," Z: ",z,"  ",ref[v][x][y][0],"  ",test[v][x][y][0],"  ",adiff)
                

sys.stdout.write("\033[0;0m")

