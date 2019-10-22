import time
import math
import numpy as np
import scipy; from scipy import optimize; from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import csv
import pandas as pd
from definitions import *
from attainableMass import *
import errorCalc; from errorCalc import *

def main(N,preOrPost,dataPath,smallestIncrement,coffeeCellSize,whichInformation):

    ##### Extract Data from .csv files #####
    # Loop through each grind setting
    grindSetting=np.arange(1,N+1)
    for a in range(1,N+1): # need to start at 1 because filenames are setting1 - settingEnd
        # import each file, list the values, then change the lists into arrays
        valuesArray = np.array(pd.read_csv("{}/setting{}_stats.csv".format(dataPath,a) ))
        
        # get the value from each stats column in the order:  '', avg_diam, std_diam, avg_surface, std_surface, efficiency, quality
        avgDiam.append(float(valuesArray[:,1])); stdDiam.append(float(valuesArray[:,2]))
        avgSurf.append(float(valuesArray[:,3])); stdSurf.append(float(valuesArray[:,4]))
        efficiency.append(float(valuesArray[:,5])); quality.append(float(valuesArray[:,6]))

        # get the value from each .csv column in the order: ID, surface, roundness, short_axis, long_axis, volume, pixel_scale
        # data for grind setting 'a' can be retrieved as parameter[a]
        dataArray = np.array(pd.read_csv("{}/setting{}.csv".format(dataPath,a)))

        # retrieve error values from exterior function
        epos,eneg = errorCalc.posNegError(dataArray,whichInformation,coffeeCellSize)

        # append value 1 sigma positive and 1 sigma negative the average value calculated above
        stdUpper.append(epos)
        stdLower.append(eneg)


    ##### Information To Plot #####                
    # Details which value the user wants to view and which units to use in regression values as well as on plots
    print()
    dataTypes=[avgDiam, stdDiam, avgSurf, stdSurf]
    def dataType(type):
        global data, pltTitle, units
        if type == "d":
            data = dataTypes[0]
            pltTitle = "Average Diameter"
            units = "mm"
        elif type == "s":
            data = dataTypes[2]
            pltTitle = "Average Surface Area"
            units = "mm^2"
        return data
    dataType(whichInformation)


    ###### Calculate the average adjustment made between each whole-number grind setting and print results #####
    for b in range(0,N-1):
        settingAdjustment.append(data[b+1] - data[b])
    avgAdjustment = np.sum(settingAdjustment)/len(settingAdjustment)

    # Print the values calculated above
    print()
    print("-----------------------------------------------")
    print("---------Grinder Adjustment Parameters --------")
    print()
    print("Total Adjustment Range (Setting {}-1): {:.2}{}".format(N,data[-1]-data[0],units))
    print("Average Adjustment Between Each Setting: {:.2}{}".format(avgAdjustment,units))
    print()


    ##### Fitting #####
    print()
    # Perform all linear-regression related procedures
    popt, pcov = curve_fit(funcLinear, grindSetting, data, maxfev=2000) # the regression
    perr = np.sqrt(np.diag(pcov)) # error in the regression

    # calculate R^2 value
    residuals = np.sum((data - funcLinear(grindSetting,*popt))**2)
    variance = np.sum ((data - np.mean(data))**2)
    r_squared = 1 - (residuals/variance)

    # Plot the regression line on the data plot
    plt.plot(grindSetting, funcLinear(grindSetting, *popt), label="Linear Fit", color='green')
#    plt.text(grindSetting[0],data[-1],r'$Equation\ of\ Linear\ Fit: y={:.2}x +({:.2})$'.format(popt[0],popt[1])) # generate equation of fit on figure

    # Plot the R^2 value on the data plot
    plt.text(grindSetting[0],data[9],r'$R^2={:.2}$'.format(r_squared))
    # Print the regression parameters 
    print()
    print("------------- Fit Parameters ------------")       
    print("\n Slope = {:.2} +/- {:.2}".format(popt[0],perr[1]))
    print("\n Intercept = {:.2} +/- {:.2}{}".format(popt[1],perr[0],units))
    print("\n R^2 = {:.2}".format(r_squared))
    print()


    ##### Plotting #####
    plt.title("{} vs. Grind Setting [{}-Adjustment]".format(pltTitle,preOrPost))
    plt.xlabel("Grind Setting")
    # Plot sizing
    plt.xlim([0,N+1])
    plt.xticks(ticks=grindSetting)
    plt.ylabel("{} [{}]".format(pltTitle,units))

    # Plot the upper and lower standard deviation values calulated in epos and eneg
    plt.errorbar(grindSetting,data, fmt='o', color='black', ecolor='red', capsize=2, label='{}'.format(pltTitle), xerr=smallestIncrement/2, yerr=[stdLower,stdUpper])

    # Annotate the values found in the data and the positive and negative 1 sigma
    # The larger error side (boulders or fines) are labeled green (helps visually distinguish skewness of data)
    for i in range(0,N):

        plt.annotate(data[i],(grindSetting[i]+.1*max(data),data[i]), color='black')
        if (stdUpper[i] > stdLower[i]):
            plt.annotate("{:.2}".format(stdUpper[i]),(grindSetting[i],stdUpper[i]+data[i]), color='green', label="error")
        else:
            plt.annotate("{:.2}".format(stdUpper[i]),(grindSetting[i],stdUpper[i]+data[i]), color='red', label="error")

        if (stdLower[i] > stdUpper[i]):
            plt.annotate("{:.2}".format(stdLower[i]),(grindSetting[i],data[i]-stdLower[i]), color='green', label="error")
        else:
            plt.annotate("{:.2}".format(stdLower[i]),(grindSetting[i],data[i]-stdLower[i]), color='red', label="error")

    plt.legend()
    # Save the figure in the $PWD 
    plt.savefig('{}Adjustment{}Plot.png'.format(preOrPost,pltTitle), dpi=199)
    plt.show()
