# -*- coding: UTF-8 -*-

"""
__Author__ = "MakiNaruto"
__Mail__: "become006@gmail.com"
__Version__ = "1.0.1"
__Created__ = "2024/10/11"
__Description__ = ""
"""
import pyautogui


class MouseController:
    def mouseMoveToPosition(self, position, duration=0.2):
        """ 鼠标移动到指定位置 """
        pyautogui.moveTo(position, duration=duration, tween=pyautogui.easeInOutElastic)

    def mouseDragToPosition(self, position, duration=0.2):
        """ 鼠标在当前位置点击不放并移动到指定位置松开 """
        pyautogui.dragTo(position, duration=duration, tween=pyautogui.easeInOutElastic, button='left')

    def mouseClickPosition(self, position):
        """ 鼠标移动到指定位置并点击一次 """
        self.mouseMoveToPosition(position)
        pyautogui.click(position)

    def mouseRightClickPosition(self, position):
        """ 鼠标移动到指定位置并点击一次 """
        self.mouseMoveToPosition(position)
        pyautogui.rightClick(position)

    def positionClickPosition(self, servant_pos, enemy_pos):
        self.mouseClickPosition(servant_pos)
        self.mouseClickPosition(enemy_pos)


if __name__ == '__main__':
    m = MouseController()
    pyautogui.moveTo([100, 100], duration=1.5, tween=pyautogui.easeInOutElastic)