#!/usr/bin/python

## @file
# Contains class Slot.

# import avango-guacamole libraries
import avango
import avango.gua

## Internal representation of a display slot. A Slot is one rendering output that can be handled
# by a display. User can have multiple slots to obtain a brighter image.
class Slot:

  ## Custom constructor.
  # @param DISPLAY Display instance for which this slot is being created.
  # @param SLOT_ID Identification number of the slot within the display.
  # @param SCREEN_NUM Number of the screen / display on the platform.
  # @param STEREO Boolean indicating if the slot to be created is a stereo one.
  # @param PLATFORM_NODE Scenegraph transformation node of the platform where the slot is to be appended to.
  def __init__(self, DISPLAY, SLOT_ID, SCREEN_NUM, STEREO, PLATFORM_NODE):

    ## @var slot_id
    # Identification number of the slot within the display.
    self.slot_id = SLOT_ID

    ## @var screen_num
    # Number of the screen / display on the platform.
    self.screen_num = SCREEN_NUM

    ## @var stereo
    # Boolean indicating if this slot is a stereo one.
    self.stereo = STEREO

    ## @var PLATFORM_NODE
    # Scenegraph transformation node of the platform where the slot is appended to.
    self.PLATFORM_NODE = PLATFORM_NODE

    ## @var assigned_user
    # User instance which was assigned to this Slot by the SlotManager.
    self.assigned_user = None

    ## @var shutter_timing
    # A list of opening and closing times of shutter glasses for this slot.
    if self.stereo:
      self.shutter_timing = DISPLAY.shutter_timings[SLOT_ID]
    else:
      self.shutter_timing = None

    ## @var shutter_value
    # A list of hexadecimal commands for shutter glasses associated with the timings for this slot.
    if self.stereo:
      self.shutter_value = DISPLAY.shutter_values[SLOT_ID]
    else:
      self.shutter_value = None

    # append nodes to platform transform node

    ## @var slot_node
    # Scenegraph transformation node of this slot.
    self.slot_node = avango.gua.nodes.TransformNode(Name = "s" + str(SCREEN_NUM) + "_slot" + str(SLOT_ID))
    self.PLATFORM_NODE.Children.value.append(self.slot_node)

    ## @var information_node
    # Node which name is set to the headtracking target name of the current user. Used for the local
    # headtracking update on client side.
    self.information_node = avango.gua.nodes.TransformNode(Name = "None")
    self.slot_node.Children.value.append(self.information_node)

    if self.stereo:
      # create the eyes
      ## @var left_eye
      # Representation of the slot's user's left eye.
      self.left_eye = avango.gua.nodes.TransformNode(Name = "eyeL")
      self.left_eye.Transform.value = avango.gua.make_identity_mat()
      self.slot_node.Children.value.append(self.left_eye)

      ## @var right_eye
      # Representation of the slot's user's right eye.
      self.right_eye = avango.gua.nodes.TransformNode(Name = "eyeR")
      self.right_eye.Transform.value = avango.gua.make_identity_mat()
      self.slot_node.Children.value.append(self.right_eye)

      self.set_eye_distance(0.06)
    else:
      ## create the eye
      # Representation of the slot's user's eye.
      self.eye = avango.gua.nodes.TransformNode(Name = "eye")
      self.eye.Transform.value = avango.gua.make_identity_mat()
      self.slot_node.Children.value.append(self.eye)


  ## Sets the transformation values of left and right eye.
  # @param VALUE The eye distance to be applied.
  def set_eye_distance(self, VALUE):
    self.left_eye.Transform.value  = avango.gua.make_trans_mat(VALUE * -0.5, 0.0, 0.0)
    self.right_eye.Transform.value = avango.gua.make_trans_mat(VALUE * 0.5, 0.0, 0.0)

  ## Assigns a user to this slot. Therefore, the slot_node is connected with the user's headtracking matrix.
  # @param USER_INSTANCE An instance of User which is to be assigned.
  def assign_user(self, USER_INSTANCE):
    # connect tracking matrix
    self.slot_node.Transform.connect_from(USER_INSTANCE.headtracking_reader.sf_abs_mat)
    self.assigned_user = USER_INSTANCE
 
    # set information node
    if USER_INSTANCE.headtracking_target_name == None:
      self.information_node.Name.value = "None"
    else:
      self.information_node.Name.value = USER_INSTANCE.headtracking_target_name

  ## Clears the user assignment.
  def clear_user(self):
    if self.assigned_user != None:
      self.slot_node.Transform.disconnect_auditors()
      self.slot_node.Transform.value = avango.gua.make_identity_mat()
      self.assigned_user = None
      self.information_node.Name.value = "None"
