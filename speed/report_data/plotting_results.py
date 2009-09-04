#!/usr/bin/env python

"""

Notes and code for plotting and testing the apps

Brian
"""
import pylab




def plot_compare(data, title, show=False):
    try:
        python_data, c_data, scipy_data = data
    except:
        python_data, c_data = data
        
    x = 1 + pylab.arange(len(c_data))
    #pylab.figure()
    pylab.title(title)
    all_data = pylab.array(data).flatten()
    
    bars = pylab.bar(x, python_data, width=0.4,color='#88aa33', align='center')
    bars2 = pylab.bar(x+0.4, c_data, width=0.4, color='#774499', align='center')
    bars3 = pylab.bar(x+0.2, scipy_data, width=0.4, color='red', align='center')
    
    pylab.legend((bars[0], bars2[0], bars3[0]), ('Python OpenCV', 'C++ OpenCV', 'SciPy'))
    
    pylab.xlabel('Test run')
    pylab.xticks(x+0.2,x)
    pylab.ylabel('Frames Per Second')
    ymin = all_data.min() - 2*all_data.std()
    if ymin < 0:ymin=0
    yaxis = pylab.linspace(ymin,all_data.max() + 1*all_data.std(),10)
    
    pylab.ylim(ymin, all_data.max() + 2*all_data.std())
    pylab.yticks(yaxis,["%.3f" % i for i in yaxis])
    pylab.savefig("%s.png" % "_".join(title.lower().split(" ")), transparent=True)

    if show:
        pylab.show()

#py_webcam_stream = pylab.array([15.0073, 15.0033,	15.0072]) #, 15.005808])
#cpp_webcam_stream = pylab.array([15.0170, 15.0092,	15.0101])#, 15.0177])
#plot_compare(py_webcam_stream, cpp_webcam_stream,"_Streaming from webcam in OpenCV", True)


#py_gaussian = pylab.array([ 14.555189, 14.736740, 13.988899])  # mean 14.4269, std: 0.318
#scipy_gaussian = pylab.array([4.374094, 4.388574, 4.336574])   # mean: 4.3664, std: 0.021912
#cpp_gaussian = pylab.array([14.7219, 14.6268, 14.6117])    # mean: 14.6534, std: 0.048780
#plot_compare(pylab.array([py_gaussian, cpp_gaussian, scipy_gaussian ]),"_Gaussian Blur", True)

py_ = pylab.array([ ])
scipy_ = pylab.array([])
cpp_ = pylab.array([])

plot_compare(pylab.array([py_, cpp_, scipy_ ]),"title", True)


#yc = 10*pylab.rand(3)
#yr = 12*pylab.rand(3)
#plot_compare(yc, yr,"testing....", True)
