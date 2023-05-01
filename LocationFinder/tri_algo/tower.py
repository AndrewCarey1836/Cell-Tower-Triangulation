import math
import topography

TA_DIST = {
    'lte' : 78.125,
    '5g' : 4.88
}

class Tower:
    def __init__(self, latitude: float, longitude: float):
        self.longitude  = longitude
        self.latitude   = latitude
        self.timeAdvance = None
        self.rsrp = None
    
    def getCoordinates(self):
        return (self.longitude, self.latitude)
    
    def distanceFrom(self, x, y):
        a_squared = math.pow(self.longitude - x, 2)
        b_squared = math.pow(self.latitude - y, 2)

        return math.sqrt(a_squared + b_squared)
    
    def getPosMeters(self, anchor:tuple[float, float]):
        pos_lat  = topography.lat_to_dist(self.latitude, self.latitude - anchor[0])
        pos_long = topography.long_to_dist(self.longitude, self.longitude - anchor[1])

        return (pos_lat, pos_long)
    
    # This is a static method which returns the distance corresponding to the timing advance
    @staticmethod
    def get_ta_dist(tower_type: str, ta: int):
        return (ta * TA_DIST[tower_type])