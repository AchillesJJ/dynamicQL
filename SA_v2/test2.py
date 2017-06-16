import pickle
import numpy as np
from utils import UTILS
import pandas as pd
from matplotlib import pyplot as plt
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

def main():

    with open('optimal.pkl','rb') as f:
        res = pickle.load(f)

    ### READING ES data and finding optimal state and the gap to excited states.
    ### Looping over parameters and storing data in a dictionary. 
    
    utils=UTILS()
    parameters = utils.read_parameter_file()
    
    prob_vs_T = {}
    for T_tmp in np.arange(0.025,4.001,0.025):
        T = round(T_tmp,2)
        prob_vs_T[T] = np.zeros((13,2),dtype=np.float64)
        ii = 0
        for n_step in [4,6,8,10,12,14,16,18,20,22,24,26,28] :
            
            parameters['T']= T
            parameters['n_step'] = n_step
            parameters['dt'] = T/n_step
            gs_fid = res[(T,n_step)][0]
            
            file = utils.make_file_name(parameters,root='data/')
            
            with open(file,'rb') as f:
                _, data = pickle.load(f)
                n_elem = len(data)
                v = np.zeros(n_elem,dtype=np.float64) # careful here, precision is important ---> !!!
                n_eval = np.zeros(n_elem,dtype=np.float64) # careful here, precision is important ---> !!!
                for i,elem in zip(range(n_elem),data):
                    v[i] = elem[1]
                    n_eval[i] = elem[0]

            count = (v[np.abs(v - gs_fid) < 1e-14].shape[0])

            prob = count/n_elem
            mean = np.mean(n_eval)
            if prob > 1e-14:
                prob=prob**-1*mean
            else:
                prob=2**n_step # worst case ... need to search the whole space ...
            if prob > 2**n_step:
                prob = 2**n_step # worst case ...   
            
            prob_vs_T[T][ii,0] = n_step
            prob_vs_T[T][ii,1] = prob 
            mean=np.mean(n_eval)
            std=np.std(n_eval)
            out_str = "{0:<6.2f}{1:<6}{2:<20.3f}{3:<10.4f}{4:<10.4f}{5:<8}".format(T,n_step,prob,std/mean,mean,count)
            print(out_str)
            ii += 1

    file_tmp='scaling_SD.pkl'
    with open(file_tmp, 'wb') as f:
        pickle.dump(prob_vs_T,f)
    exit()
    #exit()
    with open(file_tmp,'rb') as f:
        prob_vs_T = pickle.load(f)

    #print(prob_vs_T[0.1][:-3,1])
    #print(-np.log(prob_vs_T[0.1][:-3,1]))
    #exit()
    for Ttmp in np.arange(0.1,4.0,0.3) :
        T=round(Ttmp,2)
        plt.plot(prob_vs_T[T][:-2,0],np.log(prob_vs_T[T][:-2,1]),label='$T=%.2f$'%T)
        #plt.scatter(prob_vs_T[T][:-3,0],-np.log(prob_vs_T[T][:-3,1]))

    plt.xlabel('$N$',fontsize=16)
    plt.ylabel('$-\log p(h(t)=h_{\mathrm{opt}}(t))$',fontsize=16)
    plt.legend(loc='best')
    plt.tick_params(labelsize=16)
    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
    main()
