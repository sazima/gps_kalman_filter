from decimal import Decimal


class GpsKalman(object):
    def __init__(self):
        self.variance = Decimal('-1')
        self.longitude, self.latitude = None, None
        self.time_stamp = None
        self.accuracy = None

    def set_state(self, coordinate: str, time_stamp: float, accuracy: Decimal):
        self.longitude, self.latitude = self._split_coordinate(coordinate)
        self.time_stamp = time_stamp
        self.accuracy = accuracy
        self.variance = accuracy * accuracy

    def process(self, speed: Decimal, coordinate: str, time_stamp: float, accuracy: Decimal):
        longitude, latitude = self._split_coordinate(coordinate)
        if self.variance < 0:
            # 初始状态
            self.set_state(coordinate, time_stamp, accuracy)
        else:
            duration = Decimal(time_stamp - self.time_stamp)
            if duration > 0:
                self.variance += duration * speed * speed / Decimal('1000')
                self.time_stamp = time_stamp
            k = self.variance / (self.variance + accuracy * accuracy)
            # 计算位置
            self.latitude += k * (latitude - self.latitude)
            self.longitude += k * (longitude - self.longitude)
            # 方差
            self.variance = (1 - k) * self.variance
            coordinate = self._join_longitude_latitude(self.longitude, self.latitude)
            return coordinate

    @staticmethod
    def _split_coordinate(coordinate: str):
        longitude, latitude = coordinate.split(',')
        return Decimal(longitude), Decimal(latitude)

    @staticmethod
    def _join_longitude_latitude(longitude, latitude):
        return f'{round(longitude, 6)},{round(latitude, 6)}'


# if __name__ == '__main__':
#     gps_kalman = GpsKalman()
#     gps_data = []
