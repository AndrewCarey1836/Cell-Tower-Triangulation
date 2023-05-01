
# based on data from https://en.wikipedia.org/wiki/LTE_frequency_bands
LTE_M_BAND_FREQ = { # measured in MHz
    'b1'    : 2100,
    'b2'    : 1900,
    'b3'    : 1800,
    'b4'    : 1700,
    'b5'    : 850,
    'b7'    : 2600,
    'b8'    : 900,
    'b11'   : 1500,
    'b12'   : 700,
    'b13'   : 700,
    'b14'   : 700,
    'b17'   : 700,
    'b18'   : 850,
    'b19'   : 850,
    'b20'   : 800,
    'b21'   : 1500,
    'b24'   : 1600,
    'b25'   : 1900,
    'b26'   : 850,
    'b28'   : 700,
    'b29'   : 700,
    'b30'   : 2300,
    'b31'   : 450,
    'b32'   : 1500,
    'b34'   : 2000,
    'b37'   : 1900,
    'b38'   : 2600,
    'b39'   : 1900,
    'b40'   : 2300,
    'b41'   : 2500,
    'b42'   : 3500,
    'b43'   : 3700,
    'b46'   : 5200,
    'b47'   : 5900,
    'b48'   : 3500,
    'b50'   : 1500,
    'b51'   : 1500,
    'b53'   : 2400,
    'b54'   : 1600,
    'b65'   : 2100,
    'b66'   : 1700,
    'b67'   : 700,
    'b69'   : 2600,
    'b70'   : 1700,
    'b71'   : 600,
    'b72'   : 450,
    'b73'   : 450,
    'b74'   : 1500,
    'b75'   : 1500,
    'b76'   : 1500,
    'b85'   : 700,
    'b87'   : 410,
    'b88'   : 410,
    'b103'  : 700
}

def get_rsrp_dbm(in_rsrp):
    return abs(in_rsrp - 140)

def dist_from_rsrp(in_rsrp):
    rsrp = get_rsrp_dbm(in_rsrp)
    distance = 10**((rsrp - 25) / (10 * 2))

    return distance

def dist_from_hata(band:str, mobile_height:float, base_height:float):
    pass