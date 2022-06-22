import numpy as np
import matplotlib.pyplot as plt

def plot_xvg(fname, fname2=None, xlabel_set=None, ylabel_set=None, title_set=None,
             figsize=(6.4, 4.8), do_tot_avg=False, do_running_avg=False,
             legend=None):
    """
    Function to plot data from a GROMACS generated XVG file

    Parameters:
    -----------
    fname - str
        Path to SVG file to plot data from
    xlabel_set - str
        Default `None`, taken from XVG file. Desired x-axis label.
    ylabel_set - str
        Default `None`, taken from XVG file. Desired y-axis label.
    title_set - str
        Default `None`, taken from XVG file. Desired plot title.
    """
    # Extract data and metadata
    xdata, ydata, metadata = read_file(fname)

    # Plot data and Metadata
    f, ax = plt.subplots(figsize=figsize)

    make_plot(xdata, ydata, metadata, ax, xlabel_set=xlabel_set, ylabel_set=ylabel_set,
              title_set=title_set, do_tot_avg=do_tot_avg, do_running_avg=do_running_avg, legend=legend)
    
    if fname2:
        xdata2, ydata2, metadata2 = read_file(fname2)
        make_plot(xdata2, ydata2, metadata2, ax, xlabel_set=xlabel_set, ylabel_set=ylabel_set,
                  title_set=title_set, do_tot_avg=do_tot_avg, do_running_avg=do_running_avg, legend=legend)
    f.show()

def read_file(fname):
    xdata = []
    ydata = []
    metadata = {}
    with open(fname) as f:
        for line in f:
            if line[0] == "@":  # line has good metadata, grab it
                data = line.split('"')
                if len(data) > 1:
                    metadata[data[0]] = data[1]
            else:
                data = line.split()
                try:
                    #len(data) == 2:  # line only contains data
                    float(data[0])
                    xdata.append(float(data[0]))
                    ydata.append(float(data[1]))
                except ValueError:
                    pass

    xdata = np.asarray(xdata)
    ydata = np.asarray(ydata)
    return (xdata, ydata, metadata)

def calc_running_avg(xdata, ydata):
    running_avg = []
    for i in range(len(xdata)):
        running_avg.append(np.mean(ydata[0:i + 1]))
    return np.asarray(running_avg)

def make_plot(xdata, ydata, metadata, ax, xlabel_set=None, ylabel_set=None, title_set=None,
              do_tot_avg=False, do_running_avg=False,
              legend=None):
    try:
        xlabel = metadata['@    xaxis  label ']
        ylabel = metadata['@    yaxis  label ']
        title = metadata['@    title ']
        legend = metadata['@ s0 legend ']
        print(legend)
    except:
        pass

    # Output average and standard deviation:
    if do_tot_avg:
        ydata_avg = np.mean(ydata)
        ydata_std = np.std(ydata)
        print(ylabel_set)
        print("Mean +/- Standard Deviation")
        print(str(ydata_avg) + " +/- " + str(ydata_std) + " " + ylabel)
        print("")

    ax.plot(xdata, ydata)
    if xlabel_set is None:
        ax.set_xlabel(xlabel)
    else:
        ax.set_xlabel(xlabel_set)
    if ylabel_set is None:
        ax.set_ylabel(ylabel)
    else:
        ax.set_ylabel(ylabel_set)
    if title_set is None:
        ax.set_title(title)
    else:
        ax.set_title(title_set)

    if do_running_avg:
        # Calculate running average
        running_avg = calc_running_avg(xdata, ydata)
        ax.plot(xdata, running_avg)
        ax.legend([legend, "1 ps Running Average"])
    else:
        ax.legend(legend)


#plot_xvg("potential.xvg",
#    xlabel_set="Number of Steps",
#    ylabel_set="Potential Energy (kJ/mol)",
#    title_set="Energy Minimization, 1AKI, Steepest Descent",
#    figsize=(8, 6))
#
#plot_xvg("temperature.xvg",
#    ylabel_set="Temperature (K)",
#    title_set="Temperature, 1AKI, NVT Equilibration",
#    figsize=(8, 6),
#    do_tot_avg=True,
#    do_running_avg=True)
#
#plot_xvg("pressure.xvg",
#    ylabel_set="Pressure (Bar)",
#    title_set="Pressure, 1AKI, NPT Equilibrium",
#    do_tot_avg=True,
#    do_running_avg=True)
#
#plot_xvg("density.xvg",
#    ylabel_set="Density (kg/m^3)",
#    title_set="Density, 1AKI, NPT Equilibrium",
#    do_tot_avg=True,
#    do_running_avg=True)
#
#plot_xvg("rmsd.xvg",
#    fname2="rmsd_xtal.xvg",
#    title_set="RMSD, 1AKI, Backbone",
#    legend=["Equilibrated", "Crystal"])
#
#plot_xvg("gyrate.xvg",
#         title_set="Radius of gyration, 1AKI, Unrestrained MD")
#
#plt.show()
