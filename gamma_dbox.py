# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import ScalarFormatter

"""Compute specific heat ratio (gamma) based on a superposed 
box-shape velocity distribution function f(v_para).
"""

###Specify the characteristics of f(v_para)###
v_c = 1.0E5   #The lower limit velocity [m/s]
T_1 = 20.0    #The temperature of the lower-T  component [eV]
T_2 = 200.0   #The temperature of the higher-T component [eV]

###Constants###
m = 1.672E-27   #ion mass [kg]
e = 1.602E-19   #elementary charge [C]

###Compute some characteristic parameters of f(v_para)###
Delta_1 = np.sqrt(12.0*T_1*e/m)   #The width of lower-T  component [m/s]
Delta_2 = np.sqrt(12.0*T_2*e/m)   #The width of higher-T component [m/s]
#u_1 = v_c + Delta_1/2.0   #The flow velocity of lower-T  component [m/s]
#u_2 = v_c + Delta_2/2.0   #The flow velocity of higher-T component [m/s]

###Compute the moment quantities of f(v_para)###
c_h    = np.linspace(0.0, 1.0, 1000)   #The density ratio of higher-T component
u_eff  = v_c + (1.0-c_h)*(Delta_1/2.0) + c_h*(Delta_2/2.0)   #The effective flow velocity [m/s]
T_eff  = ((1.0-c_h)*Delta_1**2.0+c_h*Delta_2**2.0)/3.0 - (u_eff - v_c)**2.0   #tentative
T_eff  = T_eff*m/e   #The effective temperature [eV]
q_conv = (0.5*m*u_eff**2.0 + 1.5*e*T_eff)*u_eff   #convective heat flux / n [Wm]
q_cond = ((1.0-c_h)/Delta_1 + c_h/Delta_2)*((v_c + Delta_1 - u_eff)**4.0 - (v_c - u_eff)**4.0)  #tentative
q_cond = q_cond + c_h/Delta_2*((v_c + Delta_2 - u_eff)**4.0 - (v_c + Delta_1 - u_eff)**4.0)  #tentative
q_cond = q_cond*(m/8.0)   #conductive heat flux / n [Wm]
gamma  = u_eff**2.0 - v_c*(v_c+Delta_1)*(v_c+Delta_2)/(v_c+(1.0-c_h)*Delta_2+c_h*Delta_1)   #tentative
gamma  = gamma/(T_eff*e/m)   #specific heat ratio

print("at c_h =", c_h[gamma.argmin()], ", gamma =", min(gamma))

###Get f(v_para) for some of c_h###
c_h_samp = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
v_para   = np.linspace(0.0, Delta_2+2.0*v_c, 1000)
f_v_para = np.zeros((len(c_h_samp), len(v_para)))
for iv in range(len(v_para)):
    if(v_para[iv] >= v_c and v_para[iv] < v_c+Delta_1):
        for ic in range(len(c_h_samp)):
            f_v_para[ic,iv] = (1.0-c_h_samp[ic])/Delta_1+c_h_samp[ic]/Delta_2
    elif(v_para[iv] >= v_c+Delta_1 and v_para[iv] < v_c+Delta_2):
        for ic in range(len(c_h_samp)):
            f_v_para[ic,iv] = c_h_samp[ic]/Delta_2
    else:
        f_v_para[:,iv] = 0.0

###Plots###
plt.rcParams["font.size"] = 16
#f(v_para)
fig, ax = plt.subplots()
for ic in range(len(c_h_samp)):
    ax.plot(v_para/v_c,f_v_para[ic,:],'-',label="n/n$_{\\rm{hot}}$="+str(c_h_samp[ic]))
ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax.ticklabel_format(style="sci",  axis="y",scilimits=(0,0))
ax.tick_params(which='both',axis='both', direction='in')
ax.legend()
ax.set(xlim=[0,(v_para/v_c).max()*1.1],
       ylim=[0,f_v_para.max()*1.1],
       xlabel='v$_{\\parallel}$/v$_{\\rm{c}}$',
       ylabel='f(v$_{\\parallel}$)',
       title='')
plt.savefig("f_v_para.svg",bbox_inches="tight")
plt.savefig("f_v_para.pdf",bbox_inches="tight")
plt.show()

#gamma
fig, ax = plt.subplots()
ax.plot(c_h,gamma,'-')
ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax.ticklabel_format(style="sci",  axis="y",scilimits=(0,0))
ax.tick_params(which='both',axis='both', direction='in')
ax.set(xlim=[0,1],
       ylim=[0,gamma.max()*1.1],
       xlabel='n$_{\\rm{hot}}$/n',
       ylabel='$\gamma$',
       title='')
plt.savefig("gamma.svg",bbox_inches="tight")
plt.savefig("gamma.pdf",bbox_inches="tight")
plt.show()

#flow velocity
fig, ax = plt.subplots()
ax.plot(c_h,u_eff,'-')
ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax.ticklabel_format(style="sci",  axis="y",scilimits=(0,0))
ax.tick_params(which='both',axis='both', direction='in')
ax.set(xlim=[0,1],
       ylim=[0,u_eff.max()*1.1],
       xlabel='n$_{\\rm{hot}}$/n',
       ylabel='u$_{\\parallel}$ [m/s]',
       title='')
plt.savefig("flow.svg",bbox_inches="tight")
plt.savefig("flow.pdf",bbox_inches="tight")
plt.show()

#temperature
fig, ax = plt.subplots()
ax.plot(c_h,T_eff,'-')
ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax.ticklabel_format(style="sci",  axis="y",scilimits=(0,0))
ax.tick_params(which='both',axis='both', direction='in')
ax.set(xlim=[0,1],
       ylim=[0,T_eff.max()*1.1],
       xlabel='n$_{\\rm{hot}}$/n',
       ylabel='T$_{\\parallel}$ [eV]',
       title='')
plt.savefig("temp.svg",bbox_inches="tight")
plt.savefig("temp.pdf",bbox_inches="tight")
plt.show()

#heat fluxes
fig, ax = plt.subplots()
ax.plot(c_h,q_cond/q_conv,'-')
ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax.ticklabel_format(style="sci",  axis="y",scilimits=(0,0))
ax.tick_params(which='both',axis='both', direction='in')
ax.set(xlim=[0,1],
       ylim=[0,(q_cond/q_conv).max()*1.1],
       xlabel='n$_{\\rm{hot}}$/n',
       ylabel='q$_{\\parallel}^{\\rm{cond}}$/q$_{\\parallel}^{\\rm{conv}}$ ',
       title='')
plt.savefig("heatflux.svg",bbox_inches="tight")
plt.savefig("heatflux.pdf",bbox_inches="tight")
plt.show()

