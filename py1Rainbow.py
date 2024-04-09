
import random

import maya.cmds as cmds
import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx

kPluginCmdName = "py1Rainbow"
kBoringFlag = "-b"
kBoringLongFlag = "-boring"

class Py1RainbowCmd(ompx.MPxCommand):
    """py1Rainbow command class."""
    def __init__(self):
        super(Py1RainbowCmd, self).__init__()
        self.boring = False
        self.__dag_map = dict()
        self.__iter = None
    
    def doIt(self, args):
        """Perform initial command operation.
        
        Retrieve any flags provided to command, set ocmmand iterator
        based on whether we're parsing a selection or the entire DAG, 
        iterate over relevant obects' registering themm within the command
        class and generating random colors for them to be assigned.

        Colors generated ahead of time to ensure similar values when redo-ing.

        Args:
            args: MArgList object storing optional args provided to command.
        """

        arg_data = om.MArgDatabase(self.syntax(), args)
        if arg_data.isFlagSet(kBoringFlag):
            self.boring = True
        
        self._set_iter()
        self._iterate()
        self.redoIt()
    
    def redoIt(self):
        """Assign new color to objects mapped by doIt()."""

        for name, colors in self.__dag_map.items():
            cmds.color(name, rgbColor=colors[1])
    
    def undoIt(self):
        """Assign old color to objects mapped by doIt()."""

        for name, colors in self.__dag_map.items():
            cmds.color(name, rgbColor=colors[0])
    
    def _set_iter(self):
        """Determine type of iterator based on command input."""

        selection_list = om.MSelectionList()
        om.MGlobal.getActiveSelectionList(selection_list)
        if not selection_list.length():
            self.__iter = om.MItDag(om.MItDag.kDepthFirst, om.MFn.kMesh)
        else:
            self.__iter = om.MItSelectionList(selection_list, om.MFn.kDagNode)
    
    def _register_dag_obj(self, dag_func):
        """Register current iterator item in command class.
        
        Maps object name to tuple containing old and new object color within
        __dag_map property. 
        New color optionally made grayscale if -boring flag provided.
        Colors stored as tuple3 RGB values from 0 - 1.

        Args:
            dag_func: MFnDagNode used to retrieve properties of current 
                      iterator item.
        """

        name = dag_func.name()
        obj_color = dag_func.objectColorRGB()
        old_clr = (obj_color.r, obj_color.g, obj_color.b)
        new_clr = random_grayscale() if self.boring else random_color()
        self.__dag_map[name] = (old_clr, new_clr)
    
    def _convert_path(self, dag_path):
        """Expand current MItSelectionList item to DAG object.
        
        Args:
            dag_path: By-reference MDagPath object storing the path of the
                      current item.
        """

        self.__iter.getDagPath(dag_path)
        return dag_path.node()
    
    def _iterate(self):
        """Iterate over relevant items, registering them within __dag_map.
        
        Iterates through items stored in __iter, registering them in__dag_map
        to be accesed by redoIt() and undoIt().
        """

        dag_path = om.MDagPath()
        dag_func = om.MFnDagNode()
        convert = False if isinstance(self.__iter, om.MItDag) else True

        while not self.__iter.isDone():
            dag_obj = self._convert_path(dag_path) if convert else self.__iter.currentItem()
            dag_func.setObject(dag_obj)
            self._register_dag_obj(dag_func)
            self.__iter.next()


def random_color():
    """Make random tuple3 composed of floats from 0 - 1."""
    return tuple(random.random() for _ in range(3))


def random_grayscale():
    """Make random tuple3 composed of a single float from 0 - 1."""
    val = random.random()
    return val, val, val


def isUndoable():
    return True


def cmdCreator():
    return ompx.asMPxPtr(Py1RainbowCmd())


def syntaxCreator():
    syntax = om.MSyntax()
    syntax.addFlag(kBoringFlag, kBoringLongFlag)
    return syntax


def initializePlugin(plugin):
    plugin_func = ompx.MFnPlugin(plugin)
    try:
        plugin_func.registerCommand(
            kPluginCmdName, cmdCreator, syntaxCreator
        )
    except:
        print("Error occurred while registering Py1RainbowCmd")
        raise


def uninitializePlugin(plugin):
    plugin_func = ompx.MFnPlugin(plugin)
    try:
        plugin_func.deregisterCommand(kPluginCmdName)
    except:
        print("Error occurred while deregistering Py1RainbowCmd")
        raise
