# -*- coding: utf-8 -*-
import hou


def start_work():
    plan = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    pos = plan.selectPosition()
    up_node = plan.pwd()
    try:
        scene_geo_node = up_node.createNode('geo', 'scene_component')
        scene_geo_node.setPosition(pos)
    except:
        pass
