def map_range(val, in_min, in_max, out_min, out_max):
    return out_min + (out_max - out_min) * (val - in_min) / (in_max - in_min)

class GestureMapper:
    def position_to_sound(self, x, y):
        freq = map_range(x, 0, 1, 60, 500)
        volume = map_range(y, 0, 1, 200, 2000)
        return freq, volume