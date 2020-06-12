import os
import time

from PIL import Image, ImageDraw

from config import *

def project_to_mapspace(coords_global: tuple) -> tuple:
    assert len(coords_global) == 2
    assert all(map(lambda c: isinstance(c, float), coords_global)), f'--> {type(coords_global[0])}, {type(coords_global[-1])}'
    (lon, lat) = coords_global
    print(lon, lat)
    x_ms = round(lon * PIXELS_PER_LONGITUDE + MAPSPACE_0_0[0])
    y_ms = round(-lat * PIXELS_PER_LATITUDE + MAPSPACE_0_0[1])
    print(x_ms, y_ms)
    assert 0 <= x_ms and x_ms <= SIZE_IMAGE[0], str(x_ms)
    assert 0 <= y_ms and y_ms <= SIZE_IMAGE[1], str(y_ms)
    return (x_ms, y_ms)

class Color:
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)#127) REVIEW
    blue = (0, 0, 255)

def point_to_xy_list(point: tuple) -> list:
    (x, y) = point
    # i_terms = []
    # for i in range(20): # REVIEW
    #     j_terms = []
    #     for j in range(20): # REVIEW
    #         j_terms.append((i + x // 2, j + y // 2))
    #     i_terms.append(j_terms)
    # print(i_terms)
    # return i_terms
    xy = []
    for i in range(10): # REVIEW
        for j in range(10): # REVIEW
            xy.append((i + x - 5, j + y - 5)) # REVIEW
    # print(xy)
    return xy
class Map:
    def __init__(self):
        assert os.path.isfile(PATH_MAP)
        _im = None
        with Image.open(PATH_MAP) as im:
            _im = im.convert('RGB')
        assert _im is not None
        self._im = _im
        self._draw = ImageDraw.Draw(self._im)
    def get_size(self) -> tuple:
        return self._im.size
    def add_route_point(self, p: tuple, color: tuple=Color.black) -> None:
        assert len(p) == 2
        assert len(color) in [3, 4]
        assert all(map(lambda c: 0 <= c and c <= 255, color))
        p_ms = project_to_mapspace(p)
        print('Adding point', p_ms, 'to map.')
        xy = point_to_xy_list(p_ms)
        self._draw.point(xy, fill=color)
    def add_route_segment(self, a: tuple, b: tuple, color: tuple=Color.black) -> None:
        assert len(a) == 2
        assert len(b) == 2
        assert len(color) in [3, 4]
        assert all(map(lambda c: 0 <= c and c <= 255, color))
        # self._draw.line((0, 0) + self._im.size, fill=128)
        # self._draw.line((0, self._im.size[1], self._im.size[0], 0), fill=128)
        # self._draw.line((0, self._im.size[1], self._im.size[0], 0), fill=color, width=10)
        # self._draw.line(a + b, fill=color, width=10)
        a_ms = project_to_mapspace(a)
        b_ms = project_to_mapspace(b)
        print('Adding route segment from', a_ms, 'to', b_ms, 'to map.')
        self._draw.line(a_ms + b_ms, fill=color, width=3) # REVIEW
    def save(self) -> None:
        (basename, _) = os.path.splitext(PATH_MAP)
        path = f'{basename}-{FILE_SUFFIX}.png'
        if os.path.isfile(path):
            os.remove(path)
        self._im.save(path)
        assert os.path.isfile(path)

if __name__ == '__main__':
    
    # im_rgba = None
    # with Image.open(PATH_MAP) as im:
    #     im_rgba = im.convert('RGBA')
    # assert im_rgba is not None
    # (basename, _) = os.path.splitext(PATH_MAP)
    # im_rgba.save(f'{basename}-rgba.png')

    # map_ = Map()
    # me = (-122.73049195386251, 45.38097445)
    # sydney_uni = (151.18943366192494, -33.88890695)
    # map_.add_route_segment(me, sydney_uni)
    # map_.add_route_point(me, Color.blue)
    # map_.add_route_point(sydney_uni, Color.green)
    # map_.save()

    trouble = (47.6859573, -122.1920249)
    
