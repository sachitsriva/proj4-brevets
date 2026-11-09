"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow

#  Note for CIS 322 Fall 2016:
#  You MUST provide the following two functions
#  with these signatures, so that I can write
#  automated tests for grading.  You must keep
#  these signatures even if you don't use all the
#  same arguments.  Arguments are explained in the
#  javadoc comments.
#

DISTANCES = (200, 300, 400, 600, 1000)

SEGMENTS = (
    (200, 34, 15),
    (200, 32, 15),
    (200, 30, 15),
    (400, 28, 11.428),
)

FINISH = {
   200: 13.5,
    300: 20,
    400: 27,
    600: 40,
    1000: 75,
}



def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
       brevet_dist_km: number, the nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """

    distance = float(control_dist_km)
    brevet = float(brevet_dist_km)

    if brevet not in DISTANCES:
        raise ValueError(
            "Choose a 200, 300, 400, 600, or 1000 km brevet"
        )

    start = arrow.get(brevet_start_time)
    remaining = min(distance, brevet)
    hours = 0

    for length, maximum, minimum in SEGMENTS:
        portion = min(remaining, length)
        hours += portion / maximum
        remaining -= portion

        if remaining == 0:
            break

    minutes = int(round(hours * 60, 8) + 0.5)
    control = start.shift(minutes=minutes)

    return control.isoformat()


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
          brevet_dist_km: number, the nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    distance = float(control_dist_km)
    brevet = float(brevet_dist_km)
    if brevet not in DISTANCES:
        raise ValueError(
            "Choose a 200, 300, 400, 600, or 1000 km brevet"
        )
    
    start = arrow.get(brevet_start_time)
    distance = min(distance, brevet)

    if distance == brevet:
        hours = FINISH[brevet]

    elif distance < 60:
        hours = 1 + distance / 20

    else:
        remaining = distance
        hours = 0

        for length, maximum, minimum in SEGMENTS:
            portion = min(remaining, length)
            hours += portion / minimum
            remaining -= portion

            if remaining == 0:
                break

    minutes = int(round(hours * 60, 8) + 0.5)
    control = start.shift(minutes=minutes)

    return control.isoformat()
