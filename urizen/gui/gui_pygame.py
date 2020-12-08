import random
import os
import pygame
import pygame_gui
from collections import deque

from pygame_gui import UIManager, PackageResource

from pygame_gui.elements import UIWindow
from pygame_gui.elements import UIButton
from pygame_gui.elements import UIHorizontalSlider
from pygame_gui.elements import UITextEntryLine
from pygame_gui.elements import UIDropDownMenu
from pygame_gui.elements import UIScreenSpaceHealthBar
from pygame_gui.elements import UILabel
from pygame_gui.elements import UIImage
from pygame_gui.elements import UIPanel
from pygame_gui.elements import UISelectionList

from pygame_gui.windows import UIMessageWindow
from pygame_gui.windows import UIFileDialog

import pygame

from urizen.core.utils import construct_generators_tree
from urizen.visualizers import vg_tiled, vg_pillow_pixelated


def construct_bounded_map_image(M, w, h):
    Mw, Mh = M.get_size()
    tile_scale = 1
    if Mw * 12 >= w or Mh * 12 >= h:
        viz_func = vg_pillow_pixelated
    else:
        viz_func = vg_tiled
        tile_scale = 12

    scale = 0
    for i in range(1, 100):
        if Mw * tile_scale * i >= w or Mh * tile_scale * i >= h:
            break
        scale = i
    
    image = viz_func(M, scale=scale, show=False)
    return image


class GUIOptions:
    def __init__(self):
        self.W = 1920
        self.H = 1080
        self.resolution = (1920, 1080)
        self.fullscreen = False


class GeneratorsState:
    def __init__(self):
        self.gen_tree = construct_generators_tree()
        self.explore_state = []
        self.search_string = ''
    
    def get_current_gen_list(self):
        if not len(self.explore_state):
            return sorted(self.gen_tree.keys())
        else:
            current_dict = self.gen_tree
            for subpath in self.explore_state:
                current_dict = current_dict[subpath]
            return ['..'] + sorted(current_dict.keys())
    
    def change_state(self, subpath):
        if subpath == '..':
            self.explore_state = self.explore_state[:-1]
        else:
            current_dict = self.gen_tree
            for _subpath in self.explore_state:
                current_dict = current_dict[_subpath]
            if type(current_dict.get(subpath)) == dict:
                self.explore_state.append(subpath)

    def is_generator(self, subpath):
        if subpath == '..':
            return False
        else:
            current_dict = self.gen_tree
            for _subpath in self.explore_state:
                current_dict = current_dict[_subpath]
            return not type(current_dict.get(subpath)) == dict

    def get_generator(self, subpath):
        if not self.is_generator(subpath):
            raise ValueError('Selected item is not generator:', subpath)
        current_dict = self.gen_tree
        for _subpath in self.explore_state:
            current_dict = current_dict[_subpath]
        return current_dict[subpath]


class UrizenGuiApp:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Urizen 0.2.0')
        self.opt = GUIOptions()
        self.gen_state = GeneratorsState()
        if self.opt.fullscreen:
            self.window_surface = pygame.display.set_mode(
                self.opt.resolution,
                pygame.FULLSCREEN
            )
        else:
            self.window_surface = pygame.display.set_mode(
                self.opt.resolution,
                pygame.RESIZABLE
            )

        self.background_surface = None

        self.ui_manager = UIManager(
            self.opt.resolution,
            'urizen/data/themes/gui_theme.json'
        )
        self.ui_manager.preload_fonts([
            {'name': 'fira_code', 'point_size': 10, 'style': 'bold'},
            {'name': 'fira_code', 'point_size': 10, 'style': 'regular'},
            {'name': 'fira_code', 'point_size': 10, 'style': 'italic'},
            {'name': 'fira_code', 'point_size': 14, 'style': 'italic'},
            {'name': 'fira_code', 'point_size': 14, 'style': 'bold'}
        ])

        self.panel = None

        self.message_window = None

        self.active_panel = None
        self.recreate_ui()

        self.clock = pygame.time.Clock()
        self.time_delta_stack = deque([])

        self.button_response_timer = pygame.time.Clock()
        self.running = True

    def recreate_ui(self):
        self.ui_manager.set_window_resolution(self.opt.resolution)
        self.ui_manager.clear_and_reset()

        self.background_surface = pygame.Surface(self.opt.resolution)
        self.background_surface.fill(self.ui_manager.get_theme().get_colour('dark_bg'))

        self.btn_gen_explore = UIButton(
            pygame.Rect(5, 5, 48, 48),
            '',
            manager=self.ui_manager,
            container=None,
            object_id='#btn_gen_explore',
        )
        self.btn_gen_search = UIButton(
            pygame.Rect(5, 58, 48, 48),
            '',
            manager=self.ui_manager,
            container=None,
            object_id='#btn_gen_search',
            tool_tip_text='Not yet implemented',
        )
        self.btn_tiles_explore = UIButton(
            pygame.Rect(5, 111, 48, 48),
            '',
            manager=self.ui_manager,
            container=None,
            object_id='#btn_tiles_explore',
            tool_tip_text='Not yet implemented',
        )
        self.btn_tiles_search = UIButton(
            pygame.Rect(5, 164, 48, 48),
            '',
            manager=self.ui_manager,
            container=None,
            object_id='#btn_tiles_search',
            tool_tip_text='Not yet implemented',
        )

        self.main_area = pygame.Rect(
            5 + 48 + 5,
            5,
            self.opt.W - (5 + 48 + 5 + 5),
            self.opt.H - (5 + 5)
        )
        self.pnl_empty = UIPanel(
            self.main_area,
            starting_layer_height=1,
            manager=self.ui_manager
        )

        self.construct_gen_explore()
        self.construct_gen_search()
        self.btn_gen_search.disable()
        self.construct_tiles_explore()
        self.btn_tiles_explore.disable()
        self.construct_tiles_search()
        self.btn_tiles_search.disable()

        if self.active_panel:
            self.active_panel.show()

    def construct_gen_explore(self):
        #self.gen_explore_bg_surface = pygame.Surface(self.opt.resolution)
        #self.gen_explore_bg_surface.fill(self.ui_manager.get_theme().get_colour('dark_bg'))
        self.pnl_gen_explore = UIPanel(
            self.main_area,
            starting_layer_height=0,
            manager=self.ui_manager
        )
        
        self.gen_explore_label = UILabel(
            pygame.Rect(5, 5, 350, 35),
            'Explore generators',
            self.ui_manager,
            container=self.pnl_gen_explore,
        )
        self.gen_list = UISelectionList(
            relative_rect=pygame.Rect(5, 75, 350, self.opt.H - 95),
            item_list=self.gen_state.get_current_gen_list(),
            manager=self.ui_manager,
            container=self.pnl_gen_explore,
            allow_multi_select=False,
            object_id='#gen_list',
        )
        self.btn_gen_explore_save_as_png = None
        self.gen_explore_map_image = None
        self.gen_explore_image = None
        self.file_dialog_gen_explore_save_as_png = None
        self.pnl_gen_explore.hide()

    def construct_gen_search(self):
        self.pnl_gen_search = UIPanel(
            self.main_area,
            starting_layer_height=0,
            manager=self.ui_manager
        )
        self.pnl_gen_search.hide()

    def construct_tiles_explore(self):
        self.pnl_tiles_explore = UIPanel(
            self.main_area,
            starting_layer_height=0,
            manager=self.ui_manager
        )
        self.pnl_tiles_explore.hide()

    def construct_tiles_search(self):
        self.pnl_tiles_search = UIPanel(
            self.main_area,
            starting_layer_height=0,
            manager=self.ui_manager
        )
        self.pnl_tiles_search.hide()

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.ui_manager.process_events(event)

            if event.type == pygame.VIDEORESIZE:
                self.opt.W = event.w
                self.opt.H = event.h
                self.opt.resolution = (event.w, event.h)
                self.recreate_ui()

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.btn_gen_explore:
                        self.pnl_gen_explore.show()
                        self.pnl_gen_search.hide()
                        self.pnl_tiles_explore.hide()
                        self.pnl_tiles_search.hide()
                        self.active_panel = self.pnl_gen_explore
                    elif event.ui_element == self.btn_gen_search:
                        self.pnl_gen_explore.hide()
                        self.pnl_gen_search.show()
                        self.pnl_tiles_explore.hide()
                        self.pnl_tiles_search.hide()
                        self.active_panel = self.btn_gen_search
                    elif event.ui_element == self.btn_tiles_explore:
                        self.pnl_gen_explore.hide()
                        self.pnl_gen_search.hide()
                        self.pnl_tiles_explore.show()
                        self.pnl_tiles_search.hide()
                        self.active_panel = self.btn_tiles_explore
                    elif event.ui_element == self.btn_tiles_search:
                        self.pnl_gen_explore.hide()
                        self.pnl_gen_search.hide()
                        self.pnl_tiles_explore.hide()
                        self.pnl_tiles_search.show()
                        self.active_panel = self.pnl_tiles_search
                    elif event.ui_element == self.btn_gen_explore_save_as_png:
                        self.file_dialog_gen_explore_save_as_png = UIFileDialog(
                            pygame.Rect(
                                self.opt.W // 4,
                                self.opt.H // 4,
                                self.opt.W // 2,
                                self.opt.H // 2
                            ),
                            self.ui_manager,
                            window_title='Save as PNG',
                            initial_file_path='map.png',
                            object_id='#file_dialog_gen_explore_save_as_png'
                        )

                if event.user_type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED:
                    if event.ui_element == self.file_dialog_gen_explore_save_as_png:
                        self.gen_explore_image.save(event.text)
                
                if event.user_type == pygame_gui.UI_WINDOW_CLOSE:
                    if event.ui_element == self.file_dialog_gen_explore_save_as_png:
                        self.file_dialog_gen_explore_save_as_png = None

                if event.user_type == pygame_gui.UI_SELECTION_LIST_DOUBLE_CLICKED_SELECTION:
                    if event.ui_element == self.gen_list:
                        if self.gen_state.is_generator(event.text):
                            M = self.gen_state.get_generator(event.text)()
                            surface_w = self.opt.W - 435
                            surface_h = self.opt.H - 95
                            self.gen_explore_image = construct_bounded_map_image(M, surface_w, surface_h)
                            image_bytes = self.gen_explore_image.tobytes()
                            im_w, im_h = self.gen_explore_image.size
                            shift_x = (surface_w - im_w) // 2
                            shift_y = (surface_h - im_h) // 2
                            if not self.gen_explore_map_image:
                                self.gen_explore_map_image = UIImage(
                                    relative_rect=pygame.Rect(360 + shift_x, 75 + shift_y, im_w, im_h),
                                    image_surface=pygame.image.fromstring(
                                        image_bytes,
                                        self.gen_explore_image.size,
                                        self.gen_explore_image.mode
                                    ),
                                    manager=self.ui_manager,
                                    container=self.pnl_gen_explore,
                                    object_id='#gen_explore_map_image',
                                )
                            else:
                                self.gen_explore_map_image.set_relative_position(
                                    pygame.Rect(360 + shift_x, 75 + shift_y, im_w, im_h)
                                )
                                self.gen_explore_map_image.image = pygame.image.fromstring(
                                    image_bytes,
                                    self.gen_explore_image.size,
                                    self.gen_explore_image.mode
                                )
                            if not self.btn_gen_explore_save_as_png:
                                self.btn_gen_explore_save_as_png = UIButton(
                                    pygame.Rect(self.opt.W - 265, 5, 190, 50),
                                    'Save as PNG',
                                    manager=self.ui_manager,
                                    container=self.pnl_gen_explore,
                                    object_id='#btn_gen_explore_save_as_png',
                                    starting_height=10,
                                )
                        else:
                            self.gen_state.change_state(event.text)
                            self.gen_list.set_item_list(self.gen_state.get_current_gen_list())

    def run(self):
        while self.running:
            time_delta = self.clock.tick() / 1000.0
            self.time_delta_stack.append(time_delta)
            if len(self.time_delta_stack) > 2000:
                self.time_delta_stack.popleft()

            # check for input
            self.process_events()

            # respond to input
            self.ui_manager.update(time_delta)

            # draw graphics
            self.window_surface.blit(self.background_surface, (0, 0))
            self.ui_manager.draw_ui(self.window_surface)

            pygame.display.update()


def main():
    app = UrizenGuiApp()
    app.run()


if __name__ == '__main__':
    main()
