import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, WhiteKernel, DotProduct, ConstantKernel

import sys, pickle
sys.path.append("/home/avik/Research/vlqanalysisutilityscripts")
from VLQCouplingCalculator import VLQCouplingCalculator as vlq

def datareader(fname, test_masses, test_cws, test_czs):
    X_train = []
    Y_train = []
    X_test = []
    Y_test_true = []
    c = vlq()
    f = open(fname,"r")

    for line in f:
        this_line = line.split()
        for ii in range(len(this_line)):
            this_line[ii] = float(this_line[ii])
        c.setMVLQ(this_line[0]*100.)
        c.setc_Vals(this_line[1], this_line[2], this_line[3])
        BRs = c.getBRs()
        #Xis = c.getxis()
        #print BRs
        ## Correcting for BR vs xi choice
        #kappa = c.getKappa()*np.sqrt(Xis[0]/BRs[0])
        #c.setKappaxi(kappa, BRs[0], BRs[1])
        #BRs = c.getBRs()
        #c_s = c.getc_Vals()
        #print BRs
        ## Done for correcting between BR vs xi
        if int(this_line[0]) in test_masses or float(int(round(this_line[1]*10.))/10.) in test_cws or float(int(round(this_line[2]*10.))/10.) in test_czs:
            X_test.append(np.array([this_line[0], this_line[1], this_line[2]]))  # [ M, cw_, cz_ ]
            Y_test_true.append(this_line[4]*BRs[1]/this_line[5])
        else:
            X_train.append(np.array([this_line[0], this_line[1], this_line[2]]))  # [ M, cw_, cz_ ]
            Y_train.append(this_line[4]*BRs[1]/this_line[5])

    f.close()
    return X_train, Y_train, X_test, Y_test_true


def factor_extractor(Xt, Yt, Yerr = None):
    #print Xt, type(Xt), Xt.shape
    #print Yt
    Ms = []
    cWs = []
    cZs = []
    
    for val in Xt:
        if val[0] not in Ms: Ms.append(val[0])
        if val[1] not in cWs: cWs.append(val[1])
        if val[2] not in cZs: cZs.append(val[2])

    factors = []
    if Yerr is None: factors_err = None
    else: factors_err = []

    X = Xt
    Y = Yt

    for m in sorted(Ms):
        new_list = []
        new_list2 = []
        for cz in sorted(cZs):
            this_list = []
            this_list2 = []
            for cw in sorted(cWs):
                for ii in range(len(X)):
                    if (X[ii] == np.array([m,cw,cz])).all():
                        this_list.append(Y[ii])
                        if Yerr is not None: this_list2.append(Yerr[ii])

            this_list = np.array(this_list)
            if Yerr is not None: this_list2 = np.array(this_list2)

            new_list.append(this_list)
            if Yerr is not None: new_list2.append(this_list2)

        new_list = np.array(new_list)
        if Yerr is not None: new_list2 = np.array(new_list2)

        factors.append(new_list)
        if Yerr is not None: factors_err.append(new_list2)

    return sorted(Ms), sorted(cWs), sorted(cZs), factors, factors_err

def imager(masses, cws, czs, factors, factors_err, tag):   
    for ii in range(len(masses)):

        ## 2D contour plots 
        
        print "mass = ", masses[ii]
        print tag
        #print "factors = \n", factors[ii], "\n"
        fig = plt.figure()
        ax = fig.add_subplot(111)
        levels = np.linspace(1.0, np.round(max(factors[ii].reshape(factors[ii].size,1)),2), 10)
        cs = ax.contourf(cws, czs, factors[ii], levels, extend="neither")
        ax.set_title("Correction Factors for NWA for M(T) = " + str(int(masses[ii]*100.)) + " GeV ")
        ax.set_xlabel(r'$\tilde{c}_W$')
        ax.set_ylabel(r'$\tilde{c}_Z$')
        cbar = fig.colorbar(cs)
        #cbar.add_lines(cs)
        plt.savefig("../Figures/M_" + str(int(masses[ii])) + '_' + tag + ".png")
        plt.close()

        ## factor vs cW for each mass for each cZ
        
        _factors = factors[ii]
        if factors_err is not None: _factors_err = factors_err[ii]
        for jj in range(len(czs)):
            X = cws
            Y = _factors[jj]
            if factors_err is not None: Yerr = _factors_err[jj]
            fig = plt.figure()
	    ax = fig.add_subplot(111)
            ax.plot(X, Y, linewidth=3, color='r')
            if factors_err is not None: ax.fill_between(X, Y - Yerr, Y + Yerr, color='g', alpha=0.5) 
            ax.set_title("Correction Factors for NWA for M(T) = " + str(int(masses[ii]*100.)) + " GeV and cZ = " + str(int(czs[jj]*10.)/10.) + '( ' + tag + ')')
            ax.set_ylabel("Correction Factor")
            ax.set_xlabel("coupling to W")
            plt.savefig("../Figures/M_" + str(int(masses[ii])) + '_CZ_' + str(int(czs[jj]*10.)) + "_" + tag + ".png")
            plt.close()

        ## factor vs cZ for each mass for each cW
        
        _factors = np.transpose(factors[ii])
        if factors_err is not None: _factors_err = np.transpose(factors_err[ii])
        for jj in range(len(cws)):
            X = czs
            Y = _factors[jj]
            if factors_err is not None:	Yerr = _factors_err[jj]
            fig = plt.figure()
	    ax = fig.add_subplot(111)
            ax.plot(X, Y, linewidth=3, color='r')
            if factors_err is not None:	ax.fill_between(X, Y - Yerr, Y + Yerr, color='g', alpha=0.5)
            ax.set_title("Correction Factors for NWA for M(T) = " + str(int(masses[ii]*100.)) + " GeV and cW = " + str(int(cws[jj]*10.)/10.))
            ax.set_ylabel("Correction Factor")
            ax.set_xlabel("coupling to Z")
            plt.savefig("Plots/M_" + str(int(masses[ii])) + '_CW_' + str(int(cws[jj]*10.)) + "_" + tag + ".png")
            plt.close()

def regressor(X_train, Y_train):
    kernel = 1.0 * RBF(length_scale=0.01, length_scale_bounds=(1e-1, 1e2)) + (DotProduct() ** 3)*WhiteKernel(noise_level=2.e-8, noise_level_bounds=(1e-10, 1e-1))
    gp = GaussianProcessRegressor(kernel=kernel,alpha=0.,n_restarts_optimizer=15).fit(X_train, Y_train)
    print "kernel init: ", kernel
    print "kernel init params: ", kernel.theta
    print "kenel optimum: ", gp.kernel_
    print "opt kernel params: ", gp.kernel_.theta
    print "LML (opt): ", gp.log_marginal_likelihood()
    return gp

def pickler(model, fname):
    with open(fname, "wb") as file:
        pickle.dump(model, file)

def depickler(fname):
    with open(fname, "rb") as file:
        model = pickle.load(file)
    return model

def LML_Plotter(gp):
    prefactor = np.exp(gp.kernel_.theta[0])
    print prefactor
    sig_0 = np.exp(gp.kernel_.theta[2])
    print sig_0
    Lopt = np.exp(gp.kernel_.theta[1])
    print Lopt
    Nopt = np.exp(gp.kernel_.theta[3])
    print Nopt

    print gp.log_marginal_likelihood(gp.kernel_.theta)
    print gp.log_marginal_likelihood(np.log([prefactor, Lopt, sig_0, Nopt]))
    Lscale = np.logspace(-2, 3, 50)
    Nscale = np.logspace(-12, -5, 50)

    LML = []
    for L in Lscale:
        new_list = []
        for N in Nscale:
            new_list.append(-1.*gp.log_marginal_likelihood(np.log([prefactor, L, sig_0, N])))
        new_list = np.array(new_list)
        LML.append(new_list)

    LML = np.array(LML)

    LML = np.multiply(np.sign(LML), np.log(np.abs(LML)))

    vmin, vmax = LML.min(), LML.max()
    print Nscale[np.where(LML==vmin)[0]], Lscale[np.where(LML==vmin)[1]], "\n\n"

    fig = plt.figure()
    ax = fig.add_subplot(111)
    level = np.around(np.linspace(vmin, vmax, 50), decimals=1)
    cs = ax.contour(Nscale, Lscale, LML, level)
    ax.set_xlabel("Noise Level")
    ax.set_ylabel("Length Scale")
    ax.set_xscale("log")
    ax.set_yscale("log")
    cbar = fig.colorbar(cs)
    #cbar.add_lines(cs)
    plt.savefig("Plots/chcz/LML.png")
    plt.close()

# test_masses = range(7,23,2)
# test_cws = [0.3, 0.5, 0.6, 0.9, 1.0, 1.3, 1.4]
# test_czs = [0.4, 1.0, 1.2]


#masses_train, cw_s, cz_s, factors_train, factors_train_err = factor_extractor(X_train + X_test, np.append(Y_train,Y_test_true), None)
#imager(masses_train, cw_s, cz_s, factors_train, factors_train_err, 'observation')

#print len(Y_train), len(Y_test_true)
#sys.exit(1)


## Make the log marginal likelihood plot



# Y_test_pred, Y_test_cov  =  gp.predict(X_test, return_cov=True)
# Y_train_pred, Y_train_cov = gp.predict(X_train, return_cov=True)
# Y_test_sigma = np.sqrt(np.diag(Y_test_cov))
# Y_train_sigma = np.sqrt(np.diag(Y_train_cov))

# print "Predited values for the test samples: "
# for ii in range(len(Y_test_true)):
#     #print X_test[ii], Y_test_true[ii], Y_test_pred[ii], Y_test_sigma[ii]
#     pass

# print "Predicted values for the training samples: "
# for ii in range(len(Y_train)):
#     #print X_train[ii], Y_train[ii], Y_train_pred[ii], Y_train_sigma[ii]
#     pass


#masses_train, cw_s, cz_s, factors_train, factors_train_err = factor_extractor(X_train + X_test, np.append(Y_train_pred,Y_test_pred), np.append(Y_train_sigma,Y_test_sigma))
#imager(masses_train, cw_s, cz_s, factors_train, factors_train_err, 'prediction')
    
