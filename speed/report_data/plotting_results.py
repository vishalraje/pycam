#!/usr/bin/env python

"""

Notes and code for plotting and testing the apps

Brian
"""
import pylab


def plot_compare(data, title, show=False):
    python_cv_title = 'Python OpenCV'
    c_title = 'C++ OpenCV'
    scipy_title = 'SciPy'
    try:
        python_data, c_data, scipy_data = data
        SCIPY = True
        
    except:
        python_data, c_data = data
        SCIPY = False
    
    x = 1+pylab.arange(len(data))  # Either 2 or 3...

    pylab.title(title)
    
    all_data = pylab.array(data).flatten()
    
    bars = pylab.bar( (1), ( python_data.mean() ), yerr=python_data.std(), width=0.8, color='#88aa33', align='center', ecolor='black', capsize=50)
    bars2 = pylab.bar((2), ( c_data.mean()      ), yerr=c_data.std(),      width=0.8, color='#774499', align='center', ecolor='black', capsize=50)
    
    #pylab.errorbar(x, 
    #    [d.mean() for d in data], 
    #    [d.std() for d in data],
    #    fmt=None,
    #     marker='', mec='green', ms=300, mew=5)
    
    if SCIPY: 
        bars3 = pylab.bar((3), scipy_data.mean(), yerr=scipy_data.std(), width=0.4, color='red', align='center', ecolor='black', capsize=50)
        #pylab.legend((bars[0], bars2[0], bars3[0]), (python_cv_title,c_title ))
        pylab.xticks((1,2,3),(python_cv_title, c_title, scipy_title))
    else:
        pylab.xticks((1,2),(python_cv_title, c_title))
        #pylab.legend((bars[0], bars2[0]), (python_cv_title,c_title ))
    
    pylab.xlabel('Programming Language')
    
    pylab.ylabel('Frames Per Second')
    ymin = all_data.min() - 2*all_data.std()
    if ymin < 0:ymin=0
    yaxis = pylab.linspace(ymin,all_data.max() + 1*all_data.std(),10)
    
    pylab.ylim(ymin, all_data.max() + 2*all_data.std())
    pylab.yticks(yaxis,["%.3f" % i for i in yaxis])
    pylab.savefig("%s.png" % "_".join(title.lower().split(" ")), transparent=True)

    if show:
        pylab.show()

def plot_webcam_results():
    py_webcam_stream = pylab.array([15.0073, 15.0033,	15.0072]) #, 15.005808])
    cpp_webcam_stream = pylab.array([15.0170, 15.0092,	15.0101])#, 15.0177])
    plot_compare((py_webcam_stream, cpp_webcam_stream),"_Streaming from webcam in OpenCV", True)


#plot_webcam_results()

def plot_gaussian_results():
    py_gaussian = pylab.array([ 14.555189, 14.736740, 13.988899])  # mean 14.4269, std: 0.318
    scipy_gaussian = pylab.array([7.295238, 7.537303, 7.559511])   #mean: 7.4640173333 std:0.1196888920
    cpp_gaussian = pylab.array([14.7219, 14.6268, 14.6117])    # mean: 14.6534, std: 0.048780
    plot_compare(pylab.array([py_gaussian, cpp_gaussian, scipy_gaussian ]),"_Gaussian Blur", True)

plot_gaussian_results()

#py_ = pylab.array([ ])
#scipy_ = pylab.array([])
#cpp_ = pylab.array([])

#plot_compare(pylab.array([py_, cpp_, scipy_ ]),"title", True)


#yc = 10*pylab.rand(3)
#yr = 12*pylab.rand(3)
#plot_compare(yc, yr,"testing....", True)
