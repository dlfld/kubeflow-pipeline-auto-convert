import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from matplotlib.pylab import mpl



def fun3(x, b0, b1, b2, b3, b4, b5, b6, c1, s1, c2, s2):
    res = b0 + b1 * x[0] + b2 * x[1] + b3 * x[2] + b4 * x[3] + b5 * x[4] + b6 * x[5] + c1 * x[6] + s1 * x[7] + c2 * x[8] + s2 * x[9]
    return res

def fun1_wrapper_for_odr(beta, x):
    return fun1(x, *beta)

def fun2_wrapper_for_odr(beta, x):
    return fun2(x, *beta)

def fun3_wrapper_for_odr(beta, x):
    return fun3(x, *beta)

def get_results(fun_wrapper_for_odr, x, y, params, param_names):
    model = scipy.odr.odrpack.Model(fun_wrapper_for_odr)
    data = scipy.odr.odrpack.Data(x.T, y)
    myodr = scipy.odr.odrpack.ODR(data, model, beta0 = params,  maxit = 0)
    
    myodr.set_job(fit_type=2)
    
    parameterStatistics = myodr.run()
    df_e = len(x) - len(parameters)
    cov_beta = parameterStatistics.cov_beta
    sd_beta = parameterStatistics.sd_beta * parameterStatistics.sd_beta
    ci = []
    t_df = scipy.stats.t.ppf(0.975, df_e)

    for i in range(len(params)):
        ci.append([params[i] - t_df * parameterStatistics.sd_beta[i], params[i] + t_df * parameterStatistics.sd_beta[i]])

    tstat_beta = params / parameterStatistics.sd_beta # coeff t-statistics
    pstat_beta = (1.0 - scipy.stats.t.cdf(np.abs(tstat_beta), df_e)) * 2.0
    
    print('\t\t{}\t\t{}\t\t{}\t\t{}'.format('Coef.', 'P', 'L 95%CI', 'U 95%CI'))
    
    for i in range(len(params)):
        print('{}\t\t{:.3f}\t\t{:.4f}\t\t{:.3f}\t\t{:.3f}'.format(param_names[i], params[i], pstat_beta[i], ci[i][0], ci[i][1]))

def plt_results(x, y, fun, params, start, end):
    plt.figure(figsize = (10, 8), dpi = 100)
    plt.plot(x[:, 0], y, 'b*', label = 'data')
    plt.plot(x[start:end, 0], fun(x.T, *params)[start:end])
    plt.axvline(55, color = "red", ls = "--")
    plt.axvline(63, color = "green", ls = "--")
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title("Model Fitting")
    plt.show()
    
def plt_final_results(x, y, fun1, params1, fun2, params2, fun3, params3):
    plt.figure(figsize = (10, 8), dpi = 100)
    plt.plot(xdata.values[:, 0], ydata.values, 'b*', label='data')
    plt.plot(xdata.values[55:144, 0], fun1(x.T, *params1)[55:144], 'g-', label="疫情未发生预测")
    plt.plot(xdata.values[63:144, 0], fun2(x.T, *params2)[63:144], 'b-', label="疫情爆发但是没有缓解预测")
    plt.plot(xdata.values[:, 0], fun3(x.T, *params3), 'r-',label="真实数据点拟合")
    plt.axvline(55,color="red",ls="--")
    plt.axvline(63,color="green",ls="--")
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title("Model Fitting")
    plt.legend()
    plt.show()
    