# regression without scipy
# Jorge.pottiez@gmail.com

from numpy import *
import matplotlib.pyplot as plt

'''TOGGLEABLE DATA'''
title="Fuerza vs Ángulo"
xlabel= "$\psi \ (rad)$"
ylabel="$F \ (N)$"


'''LINEAR REGRESSION'''
def linear_regression_weights(x, y, σ):
    """Fits y = a + bx"""
    #Weights
    w = 1 / σ**2
    
    #Calculations
    n = len(x)
    sumw = sum(w)
    sumwx = sum(w*x)
    sumwx2 = sum(w*x**2)
    sumwy = sum(w*y)
    sumwxy = sum(w*x*y)
    sumwy2 = sum(w*y**2)

    Δ = sumw*sumwx2-sumwx**2
    A = (sumwx2*sumwy-sumwx*sumwxy)/Δ
    B = (sumw*sumwxy-sumwx*sumwy)/Δ
    σA = (sumwx2/Δ)**(1/2)
    σB = (sumw/Δ)**(1/2)
    
    sumx = sum(x)
    sumy = sum(y)
    sumx2 = sum(x*x)
    sumy2 = sum(y*y)
    sumxy = sum(x*y)
    R = (n*sumxy-sumx*sumy)/(((n*sumx2-sumx**2)*(n*sumy2-sumy**2)))**(1/2)
    
    print(B,A,R,σB,σA)
    return B,A,R,σB,σA


def plotlinreg(x, y, errorx,errory, a, b, err_a, err_b,r,
				title= title,xlabel= xlabel,ylabel= ylabel):

    print ("\n Fitting to y = A + B·x ")
    print ("r =",round(r, 3))
    print ("B =",round(b, 5))
    print ("σB =",round(err_b, 5))
    print ("A =",round(a, 5))
    print ("σA =",round(err_a, 5))
    print ("y = (",round(a, 5),"±",round(err_a, 5),") + (",round(b, 5),"±",round(err_b, 5),")·x")
    
    
    # Plot the data
    fig, ax1 = plt.subplots(figsize=(9,6))
    
    plt.plot(x, a + b*x ,linewidth=2,color="midnightblue",alpha=0.9, label='Regresión linear \n $y={a:7.3f} + {b:7.3f}x$'.format(a=a,b=b))
    plt.errorbar(x,y,xerr=errorx,yerr=errory, fmt='k.',ecolor='#6a9060',capsize=4,elinewidth=2)
    
    plt.plot(x,(a+err_a) + (b+err_b)*x , color='firebrick', linestyle='--', label='Incertidumbre')
    plt.plot(x,(a-err_a) + (b-err_b)*x , color='firebrick', linestyle='--')
    
    #Grid and legend
    
    plt.xlabel(xlabel, color='k')
    plt.ylabel(ylabel, color='k')
    plt.title(title)
    plt.legend(loc=2, fontsize=12)
    
    plt.show()


def demo():
	# data
	x = array([0, 1.3, 2, 3, 3.9, 5.1, 6.2,7,8,8.5,10.3])
	y = array([0.1,1.1, 1.4, 3.3, 4.8, 5.5, 6,7.4,7.7,9.5,12.1])
    
	# error bar values
	errorx = array([0.01, 0.13, 0.2, 0.3, 0.1, 0.1, 0.2,0.3,0.08,0.8,0.1])
	errory = array([0.01, 0.13, 0.2, 0.3, 0.1, 0.1, 0.2,0.3,0.08,0.8,0.1])
    
	b,a,r,err_b,err_a = linear_regression_weights(x,y, errory)
	plotlinreg(x, y, errorx,errory, a,b,err_a,err_b,r)


if __name__ == '__main__':
	demo()