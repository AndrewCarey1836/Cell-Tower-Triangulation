import requests
import rasterio
import math

DATA_FILE = 'data.txt'
TEMP_TIFF_FILE = 'temp.tif'

# earth radius based on WGS 84 ellipsoid
def get_earth_radius(latitude):
    semi_major = 6378137
    semi_minor = 6356752.314245

    return ((semi_major * semi_minor) / ((((semi_major * math.sin(latitude))**2) + ((semi_minor * math.cos(latitude))**2))**0.5))

def distance_to_angle(latitude, dist: float):
    ang2rad = 180 / math.pi
    earth_rad = get_earth_radius(latitude)

    return ((dist / earth_rad) * ang2rad)

def angle_to_dist(latitude, angle: float):
    rad2ang = math.pi / 180
    earth_rad = get_earth_radius(latitude)

    return (earth_rad * angle * rad2ang)

def lat_to_dist(latitude, degrees):
    lat_rad = math.radians(latitude)
    one_deg = 111132.92 - (559.82 * math.cos(2 * lat_rad)) + (1.175 * math.cos(4 * lat_rad)) - (0.0023 * math.cos(6 * lat_rad))

    return (one_deg * degrees)

def long_to_dist(latitude, degrees):
    lat_rad = math.radians(latitude)
    one_deg = (111412.84 * math.cos(lat_rad)) - (93.5 * math.cos(3 * lat_rad)) + (0.118 * math.cos(5 * lat_rad))

    return (one_deg * degrees)

def ydist_to_lat(latitude, dist):
    one_deg = lat_to_dist(latitude, 1)

    return (dist / one_deg)

def xdist_to_long(latitude, dist):
    one_deg = long_to_dist(latitude, 1)

    return (dist / one_deg)

def get_tiff_url(latitude, longitude):
    coords_str = None
    url_str = None

    if latitude < 0:
        coords_str = 's' + str(int(math.floor(abs(latitude))))
    else:
        coords_str = 'n' + str(int(math.ceil(abs(latitude))))
    
    if longitude < 0:
        coords_str += 'w'
        if abs(longitude) < 100: coords_str += '0'
        coords_str += str(int(math.ceil(abs(longitude))))
    else:
        coords_str += 'e'
        if abs(longitude) < 100: coords_str += '0'
        coords_str += str(int(math.floor(abs(longitude))))
    
    print('Checking "' + DATA_FILE + '" for URL...')

    with open(DATA_FILE, 'r') as file:
        for line in file:
            if coords_str in line:
                print('URL found.')
                url_str = line.strip()
                return url_str
    
    if url_str == None:
        print('ERROR: URL not found in dataset for specified coordinates.')
        return

def get_elevation(latitude, longitude):
    my_url = get_tiff_url(latitude=latitude, longitude=longitude)
    
    print('Downloading TIFF file...')
    response = requests.get(my_url)

    if response.status_code == 200:
        with open(TEMP_TIFF_FILE, 'wb') as file:
            file.write(response.content)
        print('Done.')
    else:
        print('ERROR: could not download TIFF file.')
    
    print('Processing TIFF data...')
    i, j = None, None

    with rasterio.open(TEMP_TIFF_FILE) as dataset:
        elevation_data = dataset.read(1)

        i, j = dataset.index(longitude, latitude)
    
    print('Done.')
    
    return elevation_data[i][j]