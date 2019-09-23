import math
import bpy

class BlenderHelper:
    maxValueOfRotation = 120

    @staticmethod
    def getObject(name):
        return bpy.data.objects[name]

    @staticmethod
    def getObjectLocation(name):
        return BlenderHelper.getObject(name).matrix_world.to_translation()

    @staticmethod
    def getObjectRotation(name):
        rotationEuler = BlenderHelper.getObject(name).rotation_euler
        return math.degrees(rotationEuler.x), math.degrees(rotationEuler.y), math.degrees(rotationEuler.z)

    @staticmethod
    def setObjectRotation(name, rotationVector = (0, 0, 0)):
        rotationDegrees = (math.radians(rotationVector[0]), math.radians(rotationVector[1]), math.radians(rotationVector[2]))
        BlenderHelper.getObject(name).rotation_euler = rotationDegrees

    @staticmethod
    def get3DCursorPosition():
        # in Blender 2.79, this is should be:
        # bpy.context.scene.cursor_location
        return bpy.context.scene.cursor.location

    @staticmethod
    def getMinMax(value):
        value = abs(value)
        return value if value < BlenderHelper.maxValueOfRotation else BlenderHelper.maxValueOfRotation