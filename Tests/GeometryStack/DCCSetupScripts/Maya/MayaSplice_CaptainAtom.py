
import json
from maya import cmds

import os
if 'FABRIC_RIGGINGTOOLBOX_PATH' not in os.environ:
  raise Exception("Please set the rigging ")
toolboxPath = os.environ['FABRIC_RIGGINGTOOLBOX_PATH']

# cmds.file(new=True,f=True)
# cmds.file("D:/Resources/captainatom_project/scenes/captainatom_v1_geomStripped.mb", r=True);


##############################################
## Set up the loader node.

influenceGeoms_InitNode = cmds.createNode("spliceMayaNode", name = "captainAtom_InfluenceGeoms_Init")

cmds.fabricSplice('addInputPort', influenceGeoms_InitNode, json.dumps({'portName':'filePath', 'dataType':'String', 'addMayaAttr': True}))
cmds.fabricSplice('addOutputPort', influenceGeoms_InitNode, json.dumps({'portName':'stack', 'dataType':'GeometryStack', 'extension':'RiggingToolbox', 'addSpliceMayaAttr':True, 'autoInitObjects': True}))

cmds.setAttr(influenceGeoms_InitNode + '.filePath', toolboxPath+"/Tests/GeometryStack/Resources/CaptainAtom_Skinning.json", type="string");


cmds.fabricSplice('addKLOperator', influenceGeoms_InitNode, '{"opName":"captainAtom_InfluenceGeoms_Init"}', """

require RiggingToolbox;

operator captainAtom_InfluenceGeoms_Init(
  String filePath,
  io GeometryStack stack
) {

  report("Loading Character Definition:" + filePath);
  stack.loadJSONFile(filePath);
}
""")


##############################################
## Set up the skinning pose node.

influenceGeoms_Eval = cmds.createNode("spliceMayaNode", name = "captainAtom_InfluenceGeoms_Eval")

cmds.fabricSplice('addIOPort', influenceGeoms_Eval, json.dumps({'portName':'stack', 'dataType':'GeometryStack', 'extension':'RiggingToolbox', 'addSpliceMayaAttr':True, 'autoInitObjects': False }))
cmds.fabricSplice('addInputPort', influenceGeoms_Eval, json.dumps({'portName':'displaySkinningDebugging', 'dataType':'Boolean', 'addMayaAttr': True}))
cmds.fabricSplice('addInputPort', influenceGeoms_Eval, json.dumps({'portName':'iterations', 'dataType':'Integer', 'addMayaAttr': True}))
cmds.fabricSplice('addInputPort', influenceGeoms_Eval, json.dumps({'portName':'displayDeltaMushDebugging', 'dataType':'Boolean', 'addMayaAttr': True}))
cmds.fabricSplice('addInputPort', influenceGeoms_Eval, json.dumps({'portName':'useDeltaMushMask', 'dataType':'Boolean', 'addMayaAttr': True}))
cmds.fabricSplice('addInputPort', influenceGeoms_Eval, json.dumps({'portName':'displayDeltaMushMask', 'dataType':'Boolean', 'addMayaAttr': True}))


cmds.fabricSplice('addInputPort', influenceGeoms_Eval, json.dumps({'portName':'displayGeometries', 'dataType':'Boolean', 'addMayaAttr': True}))
cmds.fabricSplice('addInputPort', influenceGeoms_Eval, json.dumps({'portName':'deformers', 'dataType':'Mat44[]', 'addMayaAttr': True, 'arrayType':"Array (Multi)"}))
cmds.setAttr(influenceGeoms_Eval + '.iterations', 30);
deformers   = ["captainatom_hip_joint","captainatom_spine_ik_2_joint","captainatom_spine_ik_3_joint","captainatom_spine_ik_4_joint","captainatom_spine_ik_5_joint","captainatom_spine_ik_6_joint","captainatom_chest_joint","captainatom_L_main_thigh_joint","captainatom_L_main_knee_joint","captainatom_L_main_ankle_joint","captainatom_L_main_ball_joint","captainatom_R_main_thigh_joint","captainatom_R_main_knee_joint","captainatom_R_main_ankle_joint","captainatom_R_main_ball_joint","captainatom_L_thigh_bendy_joint","captainatom_L_knee_bendy_joint","captainatom_L_thighBase_joint","captainatom_L_kneeBase_joint","captainatom_R_thigh_bendy_joint","captainatom_R_knee_bendy_joint","captainatom_R_thighBase_joint","captainatom_R_kneeBase_joint","captainatom_neck_joint","captainatom_head_joint","captainatom_L_clavicle_joint","captainatom_R_clavicle_joint","captainatom_L_main_shoulder_joint","captainatom_L_main_elbow_joint","captainatom_L_main_wrist_joint","captainatom_L_finger_mid_base_joint","captainatom_L_finger_mid_1_joint","captainatom_L_finger_mid_2_joint","captainatom_L_finger_mid_3_joint","captainatom_L_finger_pointer_base_joint","captainatom_L_finger_pointer_1_joint","captainatom_L_finger_pointer_2_joint","captainatom_L_finger_pointer_3_joint","captainatom_L_finger_ring_base_joint","captainatom_L_finger_ring_1_joint","captainatom_L_finger_ring_2_joint","captainatom_L_finger_ring_3_joint","captainatom_L_finger_pinky_base_joint","captainatom_L_finger_pinky_cup_joint","captainatom_L_finger_pinky_1_joint","captainatom_L_finger_pinky_2_joint","captainatom_L_finger_pinky_3_joint","captainatom_L_finger_thumb_base_joint","captainatom_L_finger_thumb_1_joint","captainatom_L_finger_thumb_2_joint","captainatom_R_main_shoulder_joint","captainatom_R_main_elbow_joint","captainatom_R_main_wrist_joint","captainatom_R_finger_mid_base_joint","captainatom_R_finger_mid_1_joint","captainatom_R_finger_mid_2_joint","captainatom_R_finger_mid_3_joint","captainatom_R_finger_pointer_base_joint","captainatom_R_finger_pointer_1_joint","captainatom_R_finger_pointer_2_joint","captainatom_R_finger_pointer_3_joint","captainatom_R_finger_ring_base_joint","captainatom_R_finger_ring_1_joint","captainatom_R_finger_ring_2_joint","captainatom_R_finger_ring_3_joint","captainatom_R_finger_pinky_base_joint","captainatom_R_finger_pinky_cup_joint","captainatom_R_finger_pinky_1_joint","captainatom_R_finger_pinky_2_joint","captainatom_R_finger_pinky_3_joint","captainatom_R_finger_thumb_base_joint","captainatom_R_finger_thumb_1_joint","captainatom_R_finger_thumb_2_joint","captainatom_L_shoulder_bendy_joint","captainatom_L_shoulderBase_joint","captainatom_R_shoulder_bendy_joint","captainatom_R_shoulderBase_joint","captainatom_L_forearm_1_joint","captainatom_L_forearm_2_joint","captainatom_R_forearm_1_joint","captainatom_R_forearm_2_joint","captainatom_onFace_upperLip_joint","captainatom_onFace_lowerLip_joint","captainatom_L_onFace_upperLip_joint","captainatom_L_onFace_lowerLip_joint","captainatom_L_onFace_lip_joint","captainatom_R_onFace_upperLip_joint","captainatom_R_onFace_lowerLip_joint","captainatom_R_onFace_lip_joint","captainatom_L_onFace_nose_joint","captainatom_R_onFace_nose_joint","captainatom_L_onFace_cheek2_joint","captainatom_R_onFace_cheek2_joint","captainatom_L_onFace_eyeBrow1_joint","captainatom_L_onFace_eyeBrow2_joint","captainatom_L_onFace_eyeBrow3_joint","captainatom_R_onFace_eyeBrow1_joint","captainatom_R_onFace_eyeBrow2_joint","captainatom_R_onFace_eyeBrow3_joint","captainatom_jaw_joint","captainatom_L_onFace_cheek1_joint","captainatom_R_onFace_cheek1_joint","captainatom_L_onFace_upperLid_joint","captainatom_L_onFace_lowerLid_joint","captainatom_R_onFace_upperLid_joint","captainatom_R_onFace_lowerLid_joint"]

for i in range(len(deformers)):
  cmds.connectAttr(deformers[i]+'.worldMatrix[0]', influenceGeoms_Eval + '.deformers[' + str(i) + ']')

cmds.fabricSplice('addKLOperator', influenceGeoms_Eval, '{"opName":"captainAtom_InfluenceGeoms_Eval"}', """

require RiggingToolbox;

operator captainAtom_InfluenceGeoms_Eval(
  io GeometryStack stack,
  Mat44 deformers[],
  Boolean displaySkinningDebugging,
  Integer iterations,
  Boolean useDeltaMushMask,
  Boolean displayDeltaMushMask,
  Boolean displayDeltaMushDebugging,
  Boolean displayGeometries
) {
  if(stack.numGeometryOperators() > 1){
    SkinningModifier skinningModifier = stack.getGeometryOperator(1);
    skinningModifier.setPose(deformers);
    skinningModifier.setDisplayDebugging(displaySkinningDebugging);
  }
  if(stack.numGeometryOperators() > 3){
    WeightmapModifier weightmapModifier = stack.getGeometryOperator(2);
    weightmapModifier.setDisplay(displayDeltaMushMask);

    DeltaMushModifier deltaMushModifier = stack.getGeometryOperator(3);
    deltaMushModifier.setNumIterations(iterations);
    deltaMushModifier.setUseMask(useDeltaMushMask);
    deltaMushModifier.setDisplayDebugging(displayDeltaMushMask);
    deltaMushModifier.setDisplayDebugging(displayDeltaMushDebugging);
  }
  stack.setDisplayGeometries(displayGeometries);
  if(displayGeometries){
    EvalContext context();
    stack.evaluate(context);
  }
}
""")

cmds.connectAttr(influenceGeoms_InitNode + '.stack', influenceGeoms_Eval + '.stack')


##############################################
## Set up the loader node for the render geoms

renderGeoms_InitNode = cmds.createNode("spliceMayaNode", name = "captainAtom_RenderGeoms_Init")

cmds.fabricSplice('addInputPort', renderGeoms_InitNode, json.dumps({'portName':'filePath', 'dataType':'String', 'addMayaAttr': True}))
cmds.fabricSplice('addOutputPort', renderGeoms_InitNode, json.dumps({'portName':'stack', 'dataType':'GeometryStack', 'extension':'RiggingToolbox', 'addSpliceMayaAttr':True, 'autoInitObjects': True}))

cmds.setAttr(renderGeoms_InitNode + '.filePath', toolboxPath+"/Tests/GeometryStack/Resources/CaptainAtom_Wrapped.json", type="string");


cmds.fabricSplice('addKLOperator', renderGeoms_InitNode, '{"opName":"captainAtom_RenderGeoms_Init"}', """

require RiggingToolbox;

operator captainAtom_RenderGeoms_Init(
  String filePath,
  io GeometryStack stack
) {
  //StartFabricProfiling();

  report("Loading Character Definition:" + filePath);
  stack.loadJSONFile(filePath);
}
""")

##############################################
## Set up the eval/render node.

renderGeoms_EvalNode = cmds.createNode("spliceMayaNode", name = "captainAtom_RenderGeoms_Eval")

cmds.fabricSplice('addInputPort', renderGeoms_EvalNode, json.dumps({'portName':'stack', 'dataType':'GeometryStack', 'extension':'RiggingToolbox', 'addSpliceMayaAttr':True, 'autoInitObjects': False}))
cmds.fabricSplice('addInputPort', renderGeoms_EvalNode, json.dumps({'portName':'srcstack', 'dataType':'GeometryStack', 'extension':'RiggingToolbox', 'addSpliceMayaAttr':True, 'autoInitObjects': False}))
cmds.fabricSplice('addInputPort', renderGeoms_EvalNode, json.dumps({'portName':'displayDebugging', 'dataType':'Boolean', 'addMayaAttr': True}))
cmds.fabricSplice('addInputPort', renderGeoms_EvalNode, json.dumps({'portName':'displayGeometries', 'dataType':'Boolean', 'addMayaAttr': True}))
cmds.fabricSplice('addOutputPort', renderGeoms_EvalNode, json.dumps({'portName':'eval', 'dataType':'Scalar', 'addMayaAttr': True}))
cmds.setAttr(renderGeoms_EvalNode + '.displayGeometries', 1);


cmds.connectAttr(renderGeoms_InitNode + '.stack', renderGeoms_EvalNode + '.stack')
cmds.connectAttr(influenceGeoms_Eval + '.stack', renderGeoms_EvalNode + '.srcstack')

cmds.fabricSplice('addKLOperator', renderGeoms_EvalNode, '{"opName":"captainAtom_RenderGeoms_Eval"}', """

require RiggingToolbox;

operator captainAtom_RenderGeoms_Eval(
  io GeometryStack stack,
  io GeometryStack srcstack,
  Boolean displayDebugging,
  Boolean displayGeometries,
  EvalContext context,
  Scalar eval
) {
  if(stack.numGeometryOperators() > 1){
    WrapModifier wrapModifier = stack.getGeometryOperator(1);
    wrapModifier.setSourceGeomStack(srcstack);
    wrapModifier.setDisplayDebugging(displayDebugging);
  }
  stack.setDisplayGeometries(displayGeometries);

  //UInt64 start = getCurrentTicks();

  //StartFabricProfiling();

  stack.evaluate(context);

  //StopFabricProfiling();
  //report( GetProfilingReport() );

  // UInt64 end = getCurrentTicks();
  // report("Eval Fps: " + String(1.0 / getSecondsBetweenTicks(start, end)));

  //report(stack.getDesc());
}
""")

##############################################
## Set up the eval locator.

forceEvalLocator = cmds.createNode("locator", name = "forceEval")
cmds.connectAttr(renderGeoms_EvalNode + '.eval', forceEvalLocator + '.localPosition.localPositionY')
