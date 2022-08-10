from distances.usecases.GetDistances.interactor import GetDistancesUCI


def get_distances_controller(account_id: int) -> GetDistancesUCI:
    return GetDistancesUCI(account_id=account_id)
