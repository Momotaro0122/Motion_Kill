import maya.cmds as cmds
import maya.mel as mel
from attr_lib.attr_preset_io import save_attrPreset,apply_attrPreset

def create(ns=None):
    ns = cmds.ls(sl=1,l=1)[0].split(':')[0].split('|')[1]
    root = cmds.ls(sl=1,l=1)[0].split('|')[1]
    ran = False
    for cog in ['COG_Ctrl','Cog_Ctrl']:
        if cmds.objExists(ns+':ABC:'+cog):
            lco = cmds.spaceLocator(n=ns+'_MK_LOC_FOLLOW')
            trange = (int(cmds.playbackOptions(q=1,min=1)),int(cmds.playbackOptions(q=1,max=1))+1)
            cmds.parentConstraint(ns+':ABC:'+cog,lco[0])

            mult = cmds.createNode('multiplyDivide',n=ns+'_MK_Inverse')

            cmds.connectAttr(lco[0]+'.t',mult+'.input1')
            cmds.setAttr(mult+'.input2',*(-1,-1,-1))
            lcoinverted = cmds.spaceLocator(n=ns+'_MK_LOC_UNFOLLOW')
            cmds.connectAttr(mult+'.output',lcoinverted[0]+'.t')
            cmds.currentTime(trange[0])
            #cmds.parentConstraint(lcoinverted[0],ns+':DYN:nClothRig',mo=1)
            cmds.parentConstraint(lcoinverted[0],root,mo=1)
            cmds.camera()
            inv_cam = [cmds.rename(ns+'_MK_InverseCamera')]
            inv_cam +=  cmds.listRelatives(ns+'_MK_InverseCamera',s=1)
            cam_offsetA = cmds.group(inv_cam,n=ns+'_MK_InvertCameraOffsetA')
            cam_offsetB = cmds.group(cam_offsetA,n=ns+'_MK_InvertCameraOffsetB')
            if not cmds.objExists('cam_follow'):
                cmds.spaceLocator(n='cam_follow')
                cmds.parentConstraint('RENDER','cam_follow',mo=1)

            cmds.matchTransform(inv_cam[0],'RENDER')
            cmds.parentConstraint(lcoinverted[0],cam_offsetB,mo=1)
            cmds.connectAttr('cam_follow.t',cam_offsetA+'.t')
            cmds.connectAttr('cam_follow.r',cam_offsetA+'.r')
            rendshape = cmds.listRelatives('RENDER',s=1)
            cam_attr = save_attrPreset(rendshape[0],'MK_render_cam_attr')
            apply_attrPreset(inv_cam[-1],cam_attr)

            for bs in cmds.ls(ns+':*Input_BS*',type='blendShape'):
                cmds.setAttr(bs+'.origin',1)

            for j in cmds.ls(ns+':*:*',type='jiggle'):
                cmds.setAttr(j+'.ignoreTransform',0)

            for nuc in cmds.ls(ns+':*:*',type='nucleus'):
                cmds.setAttr(nuc+'.useTransform',0)
                cmds.setAttr(nuc+'.usePlane',0)

            ran = True
    if ran:
        cmds.currentTime(trange[0])
        cmds.currentTime(trange[0])
        cmds.setAttr(inv_cam[-1]+'.coi',l=1)
        [cmds.setAttr(inv_cam[0]+'.'+a,l=1) for a in cmds.listAttr(inv_cam[0],k=1)]


def remove(ns=None):
    ns = cmds.ls(sl=1)[0].split(':')[0]
    cmds.delete(ns+'_MK_InverseCamera',ns+'_MK_LOC_UNFOLLOW',ns+'_MK_Inverse',ns+'_MK_LOC_FOLLOW')
    for bs in cmds.ls(ns+':*Input_BS*',type='blendShape'):
        cmds.setAttr(bs+'.origin',0)

    for j in cmds.ls(ns+':*:*',type='jiggle'):
        cmds.setAttr(j+'.ignoreTransform',1)

    for nuc in cmds.ls(ns+':*:*',type='nucleus'):
        cmds.setAttr(nuc+'.useTransform',1)

