# This file was automatically generated by SWIG (http://www.swig.org).
# Version 1.3.36
#
# Don't modify this file, modify the SWIG interface instead.
# This file is compatible with both classic and new-style classes.

import _ransacEllipse
import new
new_instancemethod = new.instancemethod
try:
    _swig_property = property
except NameError:
    pass # Python < 2.2 doesn't have 'property'.
def _swig_setattr_nondynamic(self,class_type,name,value,static=1):
    if (name == "thisown"): return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'PySwigObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    if (not static) or hasattr(self,name):
        self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)

def _swig_setattr(self,class_type,name,value):
    return _swig_setattr_nondynamic(self,class_type,name,value,0)

def _swig_getattr(self,class_type,name):
    if (name == "thisown"): return self.this.own()
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError,name

def _swig_repr(self):
    try: strthis = "proxy of " + self.this.__repr__()
    except: strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

import types
try:
    _object = types.ObjectType
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0
del types


class PySwigIterator(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, PySwigIterator, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, PySwigIterator, name)
    def __init__(self, *args, **kwargs): raise AttributeError, "No constructor defined"
    __repr__ = _swig_repr
    __swig_destroy__ = _ransacEllipse.delete_PySwigIterator
    __del__ = lambda self : None;
    def value(*args): return _ransacEllipse.PySwigIterator_value(*args)
    def incr(*args): return _ransacEllipse.PySwigIterator_incr(*args)
    def decr(*args): return _ransacEllipse.PySwigIterator_decr(*args)
    def distance(*args): return _ransacEllipse.PySwigIterator_distance(*args)
    def equal(*args): return _ransacEllipse.PySwigIterator_equal(*args)
    def copy(*args): return _ransacEllipse.PySwigIterator_copy(*args)
    def next(*args): return _ransacEllipse.PySwigIterator_next(*args)
    def previous(*args): return _ransacEllipse.PySwigIterator_previous(*args)
    def advance(*args): return _ransacEllipse.PySwigIterator_advance(*args)
    def __eq__(*args): return _ransacEllipse.PySwigIterator___eq__(*args)
    def __ne__(*args): return _ransacEllipse.PySwigIterator___ne__(*args)
    def __iadd__(*args): return _ransacEllipse.PySwigIterator___iadd__(*args)
    def __isub__(*args): return _ransacEllipse.PySwigIterator___isub__(*args)
    def __add__(*args): return _ransacEllipse.PySwigIterator___add__(*args)
    def __sub__(*args): return _ransacEllipse.PySwigIterator___sub__(*args)
    def __iter__(self): return self
PySwigIterator_swigregister = _ransacEllipse.PySwigIterator_swigregister
PySwigIterator_swigregister(PySwigIterator)

PI = _ransacEllipse.PI
class stuDPoint(_object):
    """Proxy of C++ stuDPoint class"""
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, stuDPoint, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, stuDPoint, name)
    __repr__ = _swig_repr
    __swig_setmethods__["x"] = _ransacEllipse.stuDPoint_x_set
    __swig_getmethods__["x"] = _ransacEllipse.stuDPoint_x_get
    if _newclass:x = _swig_property(_ransacEllipse.stuDPoint_x_get, _ransacEllipse.stuDPoint_x_set)
    __swig_setmethods__["y"] = _ransacEllipse.stuDPoint_y_set
    __swig_getmethods__["y"] = _ransacEllipse.stuDPoint_y_get
    if _newclass:y = _swig_property(_ransacEllipse.stuDPoint_y_get, _ransacEllipse.stuDPoint_y_set)
    def __init__(self, *args): 
        """__init__(self) -> stuDPoint"""
        this = _ransacEllipse.new_stuDPoint(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _ransacEllipse.delete_stuDPoint
    __del__ = lambda self : None;
stuDPoint_swigregister = _ransacEllipse.stuDPoint_swigregister
stuDPoint_swigregister(stuDPoint)


def get_5_random_num(*args):
  """get_5_random_num(int max_num, int rand_num)"""
  return _ransacEllipse.get_5_random_num(*args)

def solve_ellipse(*args):
  """solve_ellipse(double conic_param, double ellipse_param) -> bool"""
  return _ransacEllipse.solve_ellipse(*args)

def pupil_fitting_inliers(*args):
  """
    pupil_fitting_inliers(unsigned char pupil_image, int ?, int ?, int return_max_inliers, 
        int valid_point_calc) -> int
    """
  return _ransacEllipse.pupil_fitting_inliers(*args)

def normalize_edge_point(*args):
  """normalize_edge_point(double dis_scale, stuDPoint nor_center, int ep_num) -> stuDPoint"""
  return _ransacEllipse.normalize_edge_point(*args)

def denormalize_ellipse_param(*args):
  """
    denormalize_ellipse_param(double par, double normailized_par, double dis_scale, 
        stuDPoint nor_center)
    """
  return _ransacEllipse.denormalize_ellipse_param(*args)

def destroy_edge_point(*args):
  """destroy_edge_point()"""
  return _ransacEllipse.destroy_edge_point(*args)

def starburst_pupil_contour_detection(*args):
  """
    starburst_pupil_contour_detection(unsigned char pupil_image, int width, int height, int edge_thresh, 
        int N, int minimum_cadidate_features, 
        int valid_point_calc)
    """
  return _ransacEllipse.starburst_pupil_contour_detection(*args)

def locate_edge_points(*args):
  """
    locate_edge_points(unsigned char image, int width, int height, double cx, 
        double cy, int dis, double angle_step, double angle_normal, 
        double angle_spread, int edge_thresh)
    """
  return _ransacEllipse.locate_edge_points(*args)

def get_edge_mean(*args):
  """get_edge_mean() -> stuDPoint"""
  return _ransacEllipse.get_edge_mean(*args)

def normalize_point_set(*args):
  """
    normalize_point_set(stuDPoint point_set, double dis_scale, stuDPoint nor_center, 
        int num) -> stuDPoint
    """
  return _ransacEllipse.normalize_point_set(*args)

cvar = _ransacEllipse.cvar
