from math import e, log, floor


async def return_level(xp: int) -> float:
    if xp == 0:
        return 0
    n = round((log(xp) / 1.6**e)**2, 2)
    y = math.floor(n)
    return int(y)
