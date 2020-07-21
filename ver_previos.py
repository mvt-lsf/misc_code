
import numpy as np 

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import glob,time,os,datetime


ahora=datetime.datetime.now()
ahora_t=time.mktime(ahora.timetuple())

if ahora.weekday()==0:
	horas_a_ver=60
else:
	horas_a_ver=36

##asume que esta en la carpeta donde estan los datos

stds_recientes=filter( lamdbda x: ahora_t-os.path.getmtime(x)<=horas_a_ver*60*60 ,sorted(glob.glob('STD/*.std'))[:-1])#no considera el que se esta generando ah0ra
avgs_recientes=filter( lamdbda x: ahora_t-os.path.getmtime(x)<=horas_a_ver*60*60 ,sorted(glob.glob('AVG/*.std'))[:-1])#no considera el que se esta generando ah0ra

bins=8391#por ahora a mano, se deberia leer [cols] de .hdr

path_general_reportes='D:/informes_diarios/'
path_reportes_diarios=str(ahora).replace('-','_').replace(' ','')[:10]
if not(os.path.isdir(path_general_reportes+path_reportes_diarios)): 
	os.mkdir(path_general_reportes+path_reportes_diarios)
	os.mkdir(path_general_reportes+path_reportes_diarios+'/wfs')
	os.mkdir(path_general_reportes+path_reportes_diarios+'/pks')
path_final=path_general_reportes+path_reportes_diarios

for s,a in zip(stds_recientes,avgs_recientes):

	try:	
		wf_std=np.fromfile(s,dtype=np.float32).reshape(-1,bins)
		wf_avg=np.fromfile(a,dtype=np.float32).reshape(-1,bins)

		wf_vista=wf_std/wf_avg
	except:
		print "falla waterfall" , s , datetime.datetime.fromtimestamp(os.path.getctime(s)), datetime.datetime.fromtimestamp(os.path.getmtime(s))
		continue

	plt.imshow(wf_vista,vmax=0.15,aspect='auto')
	plt.title(str(datetime.datetime.fromtimestamp(os.path.getctime(s)))+' -- '+str(datetime.datetime.fromtimestamp(os.path.getmtime(s))))
	fname=s[:6]+'__'str(datetime.datetime.fromtimestamp(os.path.getctime(s)))+'___'+str(datetime.datetime.fromtimestamp(os.path.getmtime(s)))
	plt.savefig(path_final+'/wfs/'+fname+'.png',dpi=200, bbox_inches='tight')
	plt.close()