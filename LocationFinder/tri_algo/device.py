import tower
import trirf2d
import topography
import geo2d
from scipy.optimize import least_squares

class DistMethod:
    rsrp = 'rsrp'
    ta = 'ta'

class Device:
    def __init__(self):
        self.towers: list[tower.Tower] = []

    def addTower(self, _tower: tower.Tower, timeAdvance:int=None, rsrp:int=None):
        _tower.timeAdvance = timeAdvance
        _tower.rsrp = rsrp
        self.towers.append(_tower)
    
    def towerAnchor(self):
        points = []

        for tow in self.towers:
            points.append((tow.latitude, tow.longitude))
        
        return geo2d.get_midpoint(*points)

    def get2DPosition(self, method:DistMethod):
        anchor = self.towerAnchor()

        circles = []

        for tow in self.towers:
            lat_meters = topography.lat_to_dist(tow.latitude, tow.latitude - anchor[0])
            long_meters = topography.long_to_dist(tow.latitude, tow.longitude - anchor[1])
            radius = None
            if method == DistMethod.rsrp:
                radius = trirf2d.dist_from_rsrp(tow.rsrp)
            elif method == DistMethod.ta:
                radius = tow.get_ta_dist('lte', tow.timeAdvance)
            #print('lat:', lat_meters, 'long:', long_meters, 'dist:', radius) # DEBUG
            circles.append(geo2d.Circle((lat_meters, long_meters), radius))
        
        points = geo2d.get_min_points(*circles)
        print(points)
        print(geo2d.get_midpoint(*points))
    
    def estimate2DPos(self, method:DistMethod):
        anchor = self.towerAnchor()

        circles = []

        for tow in self.towers:
            radius = None
            if method == DistMethod.rsrp:
                radius = trirf2d.dist_from_rsrp(tow.rsrp)
            elif method == DistMethod.ta:
                radius = tower.Tower.get_ta_dist('5g', tow.timeAdvance)
            #print('lat:', tow.latitude, 'long:', tow.longitude, 'dist:', radius) # DEBUG
            circles.append(geo2d.Circle((tow.latitude, tow.longitude), radius))
        
        return geo2d.estimate_intersection(circles[0], circles[1], circles[2])
    
    def estimateCoords(self, method:DistMethod):
        anchor = self.towerAnchor()
        coords_meters = self.estimate2DPos(method)

        lat_ang  = topography.ydist_to_lat(anchor[0], coords_meters[0])
        long_ang = topography.xdist_to_long(anchor[0], coords_meters[1])

        return (anchor[0] + lat_ang, anchor[1] + long_ang)
    
    def ellipsoidal2DPos(self, method:DistMethod):
        anchor = self.towerAnchor()

        lat_deg = topography.lat_to_dist(anchor[0], 1)
        long_deg = topography.long_to_dist(anchor[0], 1)

        min_tow = self.towers[0]

        for tow in self.towers:
            if method == DistMethod.ta:
                if tow.timeAdvance < min_tow.timeAdvance:
                    min_tow = tow
            elif method == DistMethod.rsrp:
                if tow.rsrp < min_tow.rsrp:
                    min_tow = tow
        
        guess = (min_tow.latitude, min_tow.longitude)

        def eq(g):
            my_lat, my_long = g

            towerList = []

            for tow in self.towers:
                if method == DistMethod.ta:
                    towerList.append(
                        ((my_lat - tow.latitude) * lat_deg)**2 + ((my_long - tow.longitude) * long_deg)**2 - tower.Tower.get_ta_dist('5g', tow.timeAdvance)**2
                    )
                elif method == DistMethod.rsrp:
                    towerList.append(
                        ((my_lat - tow.latitude) * lat_deg)**2 + ((my_long - tow.longitude) * long_deg)**2 - trirf2d.dist_from_rsrp(tow.rsrp)**2
                    )

            return tuple(towerList)

        val = least_squares(eq, guess, method='lm')

        return tuple(val.x)
    
    def getExact2DPosition(self):
        if len(self.towers) < 3:
            print('ERROR: at least 3 towers required')
            return

        x1 = self.towers[0][0].longitude
        y1 = self.towers[0][0].latitude
        d1 = self.towers[0][1]
        x2 = self.towers[1][0].longitude
        y2 = self.towers[1][0].latitude
        d2 = self.towers[1][1]
        x3 = self.towers[2][0].longitude
        y3 = self.towers[2][0].latitude
        d3 = self.towers[2][1]

        X12 = 2 * (x2 - x1)
        X23 = 2 * (x3 - x2)
        Y12 = 2 * (y2 - y1)
        Y23 = 2 * (y3 - y3)
        D12 = (d1**2) - (d2**2) + (x2**2) - (x1**2) + (y2**2) - (y1**2)
        D23 = (d2**2) - (d3**2) + (x3**2) - (x2**2) + (y3**2) - (y2**2)
        
        denom = (X12 * Y23) - (X23 * Y12)

        return (((Y23 * D12) - (Y12 * D23))/denom, ((X12 * D23) - (X23 * D12))/denom)