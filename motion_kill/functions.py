import re
import maya.cmds as cmds


class motion_killer:
    def __init__(self):
        self.sel = cmds.ls(sl=True)[0] or []
        self.name_space = cmds.ls(self.sel, l=1)[0].split(':')[0].split('|')[1][0]
        all_objects = cmds.ls(self.name_space + ':Cloth:*')
        self.cog = [obj for obj in all_objects if re.search(r'cog_ctrl$', obj, re.IGNORECASE)][0]
        self.nucleus = [obj for obj in all_objects if re.search(r'nCloth_nucleus$', obj, re.IGNORECASE)][0]
        self.flw_loc = self.name_space + ':Cloth:Nucleus_Follow'
        self.org_loc = self.name_space + ':Cloth:Nucleus_Origin'

    def create_kill_nodes(self):
        # Follow_loc
        if not cmds.objExists(self.flw_loc):
            cmds.spaceLocator(n=self.flw_loc)
        # Origin_loc
        if not cmds.objExists(self.org_loc):
            cmds.spaceLocator(n=self.org_loc)
        cmds.shadingNode('reverse', au=1, n=self.name_space + ':Cloth:Nucleus_pos_RV')
        cmds.shadingNode('reverse', au=1, n=self.name_space + ':Cloth:Nucleus_rot_RV')
        if not cmds.objExists(self.nucleus + '.follow_char_pos'):
            cmds.addAttr(self.nucleus, longName='follow_char_pos', attributeType='float', k=1, max=1, min=0)
        if not cmds.objExists(self.nucleus + '.follow_char_rot'):
            cmds.addAttr(self.nucleus, longName='follow_char_rot', attributeType='float', k=1, max=1, min=0)

    def disconnect_nucleus(self):
        [disconnect_attr('{}.{}{}'.format(self.nucleus, op, axis)) for axis in ['x', 'y', 'z'] for op in
         ['t', 'r']]

    def connection_setup(self, flw_point=False):
        if flw_point:
            target = self.sel
            if cmds.filterExpand(target, sm=31):
                # Move follow loc and constraint to point.
                cmds.pointOnPolyConstraint(target, self.flw_loc)
            else:
                cmds.error('Hey! Are you sure you selected a vertex...?')
        else:
            target = self.cog
            # Move follow loc and constraint to COG.
            cmds.parentConstraint(target, self.flw_loc)
        p_con = cmds.parentConstraint(self.flw_loc, self.org_loc, self.nucleus)[0]
        for op in ['pos', 'rot']:
            cmds.connectAttr(p_con + '.Nucleus_FollowW0', self.name_space + ':Cloth:Nucleus_{}_RV.inputX'.format(op),
                             f=1)
            cmds.connectAttr(self.name_space + ':Cloth:Nucleus_{}_RV.outputX'.format(op), p_con + '.Nucleus_OriginW1',
                             f=1)
            cmds.connectAttr(self.nucleus + '.follow_char_{}'.format(op), p_con + '.Nucleus_FollowW0', f=1)
            cmds.setAttr(self.nucleus + '.follow_char_{}'.format(op), 1)
            cmds.select(cl=True)

    def run_steps(self):
        if ':Cloth:' in self.sel:
            self.create_kill_nodes()
            self.disconnect_nucleus()
            self.connection_setup()
        else:
            cmds.error('Plz select character obj with ":Cloth:" in it...')


# Core.
def disconnect_attr(plug):
    if cmds.connectionInfo(plug, isDestination=True):
        plug = cmds.connectionInfo(plug, getExactDestination=True)
        readOnly = cmds.ls(plug, ro=True)
        # delete -icn doesn't work if destination attr is readOnly
        if readOnly:
            source = cmds.connectionInfo(plug, sourceFromDestination=True)
            cmds.disconnectAttr(source, plug)
        else:
            cmds.delete(plug, icn=True)


