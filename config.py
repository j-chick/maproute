# traceroute
MAX_TTL = 25
WAIT = 3

# template image
PATH_MAP = '/Users/jessechick/School/s20/cs312/final/maproute/world-map-latitude.png' # FIXME
SIZE_IMAGE = (3900, 1820)

# global coordinates
MIN_LONGITUDE = -180.0
MAX_LONGITUDE = 180.0
MIN_LATITUDE = -60.0
MAX_LATITUDE = 90.0
WIDTH_MAP_GRID_CELL = 106
HEIGHT_MAP_GRID_CELL = 110
LONGITUDE_PER_GRID_CELL = 10
LATITUDE_PER_GRID_CELL = 10
PIXELS_PER_LONGITUDE = WIDTH_MAP_GRID_CELL / LONGITUDE_PER_GRID_CELL
PIXELS_PER_LATITUDE = HEIGHT_MAP_GRID_CELL / LATITUDE_PER_GRID_CELL
assert isinstance(PIXELS_PER_LONGITUDE, float)
assert isinstance(PIXELS_PER_LATITUDE, float)

# in mapspace
MAPSPACE_0_0 = (1950, 1091)

# output image
DIR_TEMP_FILES = './temp'
FILE_SUFFIX = 'LATEST'
