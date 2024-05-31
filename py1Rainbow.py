
import random

import maya.cmds as cmds
import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx

kPluginCmdName = "py1Rainbow"
kBoringFlag = "-b"
kBoringLongFlag = "-boring"

class Py1RainbowCmd(ompx.MPxCommand):
    """py1Rainbow command class."""
    def __init__(self) -> None:
        super(Py1RainbowCmd, self).__init__()
        self.boring: bool = False
        self.__dag_map: dict = dict()
        self.__iter: om.MItDag | om.MItSelectionList = None
    
    def doIt(self, args: om.MArgList):
        """Perform initial command operation.
        
        Retrieve any flags provided to command, set ocmmand iterator
        based on whether we're parsing a selection or the entire DAG, 
        iterate over relevant obects' registering themm within the command
        class and generating random colors for them to be assigned.

        Colors generated ahead of time to ensure similar values when redo-ing.

        Args:
            args: MArgList object storing optional args provided to command.
        """

        arg_data: om.MArgDatabase = om.MArgDatabase(self.syntax(), args)
        if arg_data.isFlagSet(kBoringFlag):
            self.boring = True
        
        self._set_iter()
        self._iterate()
        self.redoIt()
    
    def redoIt(self) -> None:
        """Assign new color to objects mapped by doIt()."""

        for name, colors in self.__dag_map.items():
            cmds.color(name, rgbColor=colors[1])
    
    def undoIt(self) -> None:
        """Assign old color to objects mapped by doIt()."""

        for name, colors in self.__dag_map.items():
            cmds.color(name, rgbColor=colors[0])
    
    def _set_iter(self) -> None:
        """Determine type of iterator based on command input."""

        selection_list: om.MSelectionList = om.MSelectionList()
        om.MGlobal.getActiveSelectionList(selection_list)
        if not selection_list.length():
            self.__iter: om.MItDag = om.MItDag(om.MItDag.kDepthFirst, om.MFn.kMesh)
        else:
            self.__iter: om.MItSelectionList = om.MItSelectionList(selection_list, om.MFn.kDagNode)
    
    def _register_dag_obj(self, dag_func: om.MFnDagNode) -> None:
        """Register current iterator item in command class.
        
        Maps object name to tuple containing old and new object color within
        __dag_map property. 
        New color optionally made grayscale if -boring flag provided.
        Colors stored as tuple3 RGB values from 0 - 1.

        Args:
            dag_func: MFnDagNode used to retrieve properties of current 
                      iterator item.
        """

        name: str = dag_func.name()
        obj_color: om.MColor = dag_func.objectColorRGB()
        old_clr: tuple[om.MColor] = (obj_color.r, obj_color.g, obj_color.b)
        new_clr: tuple[float] = random_grayscale() if self.boring else random_color()
        self.__dag_map[name] = (old_clr, new_clr)
    
    def _convert_path(self, dag_path: om.MDagPath) -> om.MObject:
        """Expand current MItSelectionList item to DAG object.
        
        Args:
            dag_path: By-reference MDagPath object storing the path of the
                      current item.
        """

        self.__iter.getDagPath(dag_path)
        return dag_path.node()
    
    def _iterate(self) -> None:
        """Iterate over relevant items, registering them within __dag_map.
        
        Iterates through items stored in __iter, registering them in__dag_map
        to be accesed by redoIt() and undoIt().
        """

        dag_path: om.DagPath = om.MDagPath()
        dag_func: om.MFnDagNode = om.MFnDagNode()
        convert: bool = False if isinstance(self.__iter, om.MItDag) else True

        while not self.__iter.isDone():
            dag_obj: om.MObject = self._convert_path(dag_path) if convert else self.__iter.currentItem()
            dag_func.setObject(dag_obj)
            self._register_dag_obj(dag_func)
            self.__iter.next()


def random_color() -> tuple[float]:
    """Make random tuple3 composed of floats from 0 - 1."""
    return tuple(random.random() for _ in range(3))


def random_grayscale() -> tuple[float]:
    """Make random tuple3 composed of a single float from 0 - 1."""
    val = random.random()
    return val, val, val


def isUndoable() -> bool:
    return True


def cmdCreator() -> ompx.pointer:
    return ompx.asMPxPtr(Py1RainbowCmd())


def syntaxCreator() -> om.MSyntax:
    syntax: om.MSyntax = om.MSyntax()
    syntax.addFlag(kBoringFlag, kBoringLongFlag)
    return syntax


def initializePlugin(plugin: om.MObject) -> None:
    plugin_func: om.MFnPlugin = ompx.MFnPlugin(plugin)
    try:
        plugin_func.registerCommand(
            kPluginCmdName, cmdCreator, syntaxCreator
        )
    except:
        print("Error occurred while registering Py1RainbowCmd")
        raise


def uninitializePlugin(plugin) -> None:
    plugin_func: ompx.MFnPlugin = ompx.MFnPlugin(plugin)
    try:
        plugin_func.deregisterCommand(kPluginCmdName)
    except:
        print("Error occurred while deregistering Py1RainbowCmd")
        raise
