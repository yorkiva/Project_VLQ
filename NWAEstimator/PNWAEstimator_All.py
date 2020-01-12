import numpy as np 
from matplotlib import pyplot as plt 
import sys
sys.path.append("../") 
from VLQCouplingCalculator import VLQCouplingCalculator as vlq
import ROOT
from scipy.optimize import curve_fit

def pickler(model, fname):
    with open(fname, "wb") as file:
        pickle.dump(model, file)

def depickler(fname): 
    with open(fname, "rb") as file:
        model = pickle.load(file)
    return model

def funcH(x, a, b):
    return (1 - a*(1 - np.exp(-b*x)))*(np.sign(b) + 1)/2.0

def funcV(x, a, b):
    return 1 + a*x + b*x**2


mode = sys.argv[1]

if mode in ["WTWb", "WTZt", "WBZb", "WBWt"]: seq = 'wzh'
elif mode in ["ZTHt", "ZTZt", "ZBZb", "ZBHb"]: seq = 'zhw'
elif mode in ["ZTWb", "ZBWt"]: seq = 'zwh'
elif mode in ["WTHt", "WBHb"]: seq = 'whz'


file0 = open("Data/xs_table_" + mode +".txt")
seq_dict = {'W':1, 'Z':2, 'H':3, 'w':1, 'z':2, 'h':3}
Plt_dict1 = {}
Plt_dict2 = {}
As = {}
Bs = {}
c = vlq(mode=mode[1])
for line in file0:
    vals = line.split()
    for ii in range(len(vals)):
        vals[ii] = float(vals[ii])
    mass = int(vals[0])
    if mass not in Plt_dict1.keys():
        Plt_dict1[mass] = [[], []]
        Plt_dict2[mass] = [[], []]
    c.setMVLQ(vals[0]*100.)
    c.setc_Vals(vals[1], vals[2], vals[3])
    BRs = c.getBRs()
    if mode[2] == 'W': BR = BRs[0]
    elif mode[2] == 'Z': BR = BRs[1]
    else: BR = BRs[2]
    if c.getGamma()/(mass*100.) < 1.0:
        GM = c.getGamma()/(mass*100.)
        PNWA = vals[4]*BR/vals[5]
        print mass, vals, GM, PNWA
        if PNWA < 1.0: print "PNWA < 1 for m = ", mass, "cw = ", vals[1], "cz = ", vals[2], "ch = ", vals[3]
        #print vals[seq_dict[mode[2]]]
        if vals[seq_dict[seq[2]]] == 0.0:
            Plt_dict1[mass][0].append(GM)
            Plt_dict1[mass][1].append(PNWA)
        else:
            Plt_dict2[mass][0].append(GM)
            Plt_dict2[mass][1].append(PNWA)
        #if mass < 12: print vals, GM, PNWA

#LR = linear_model.LinearRegression(fit_intercept=False)

for key in Plt_dict1.keys():
    X = Plt_dict1[key][0] + Plt_dict2[key][0]
    Y = Plt_dict1[key][1] + Plt_dict2[key][1]
    if mode[2]=="H": params, cov = curve_fit(funcH, X, Y)
    else: params, cov = curve_fit(funcV, X, Y)
    As[key] = params[0]
    Bs[key] = params[1]

print "As: ", As
print "Bs:", Bs
pickler(As, "PNWA_As_"+mode+".pickle")
pickler(Bs, "PNWA_Bs_"+mode+".pickle")


for key in sorted(Plt_dict1.keys()):
    print key
    fig = plt.figure(figsize=(10,6))  
    ax = fig.add_subplot(111) 

    X1 = Plt_dict1[key][0]  
    Y1 = np.array(Plt_dict1[key][1])
    X2 = Plt_dict2[key][0]  
    Y2 = np.array(Plt_dict2[key][1])
    #print len(X1), len(X2)
    Xin = 0.1*np.array(range(0,11))
    if mode[2] == "H": Y_pred = list(funcH(Xin, As[key], Bs[key]))
    else: Y_pred = list(funcV(Xin, As[key], Bs[key]))
    ax.set_xlim(0.0,1.0)
    ax.set_ylim(bottom=0.0,top=2.5)
    
    ax.set_xlabel(r'$\frac{\Gamma}{M}$', fontsize = 30)  
    ax.set_ylabel(r'$P_{NWA}$', fontsize = 30)  
    ax.scatter(X1, Y1, label= r'$\tilde{c}_' + seq[2].upper() + r' = 0$', marker='o', color='g')
    ax.scatter(X2, Y2, label= r'$\tilde{c}_' + seq[2].upper() + r' = \tilde{c}_' + seq[1].upper() + '$', marker='D', color='b')
    ax.plot(0.1*np.array(range(0,11)), Y_pred, label= "Prediction", color='r')
    ax.legend(prop={'size': 15})
    plt.savefig("../Figures2/PNWA_v_Gamma_" + str(key) + "_justLR_"+mode+".png", bbox_inches='tight')
    plt.close()

