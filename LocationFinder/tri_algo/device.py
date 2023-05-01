import tower
import trirf2d
import topography
import geo2d

class DistMethod:
    rsrp = 'rsrp'
    ta = 'ta'

max_steps = 100
step_size = 5

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
                radius = tow.get_ta_dist('5g', tow.timeAdvance)
            #print('lat:', lat_meters, 'long:', long_meters, 'dist:', radius) # DEBUG
            circles.append(geo2d.Circle((lat_meters, long_meters), radius))
        
        points = geo2d.get_min_points(*circles)
        print(points)
        print(geo2d.get_midpoint(*points))
    
    def estimate2DPos(self, method:DistMethod):
        anchor = self.towerAnchor()

        circles = []

        for tow in self.towers:
            lat_meters = topography.lat_to_dist(tow.latitude, tow.latitude - anchor[0])
            long_meters = topography.long_to_dist(tow.latitude, tow.longitude - anchor[1])
            radius = None
            if method == DistMethod.rsrp:
                radius = trirf2d.dist_from_rsrp(tow.rsrp)
            elif method == DistMethod.ta:
                radius = tow.get_ta_dist('5g', tow.timeAdvance)
            print('lat:', lat_meters, 'long:', long_meters, 'dist:', radius) # DEBUG
            circles.append(geo2d.Circle((lat_meters, long_meters), radius))
        
        return geo2d.estimate_intersection(circles[0], circles[1], circles[2])
    
    def estimateCoords(self, method:DistMethod):
        anchor = self.towerAnchor()
        coords_meters = self.estimate2DPos(method)

        lat_ang  = topography.ydist_to_lat(anchor[0], coords_meters[0])
        long_ang = topography.xdist_to_long(anchor[0], coords_meters[1])

        return (anchor[0] + lat_ang, anchor[1] + long_ang)
    
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