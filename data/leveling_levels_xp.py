from math import e, log


async def return_level(xp: int) -> float:
    if xp == 0:
        return 0
    n = round((log(xp) / 1.6**e)**2, 2)
    y = str(n).split('.')
    return int(y[0])
