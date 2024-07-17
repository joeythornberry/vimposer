def is_multiple(possible_multiple: int, possible_factor: int, tolerance: int) -> tuple[int, bool]:
    """Return multiplier, True if possible_multiple is within tolerance of possible_factor * multiplier."""
    multiplier = 1
    while possible_factor * multiplier < possible_multiple + tolerance:
        distance_between_times = abs(possible_factor * multiplier - possible_multiple)
        if distance_between_times < tolerance:
            return multiplier, True
        multiplier += 1

    print(f"MF {possible_multiple} is not a multiple of {possible_factor} with tolerance {tolerance}")
    return 0, False

def is_fraction(possible_fraction: int, possible_multiple: int, tolerance: int, denominators: list[int]) -> tuple[int, bool]:
    """Return denominator, True if possible_fraction is within tolerance of possible_multiple / denominator."""
    for denominator in denominators:
        possible_fraction_of_existing_delta_time = int(possible_multiple / denominator)
        distance_between_times = abs(possible_fraction_of_existing_delta_time - possible_fraction)
        if distance_between_times < tolerance:
            return denominator, True

    return 0, False

def assign_delta_time(
        existing_delta_times: list[int],
        new_delta_time: int,
        tolerance: int) -> tuple[int, bool]:
    """Return the processed delta time and True if the processed delta time should be added to the list of delta times."""

    if new_delta_time < tolerance:
        return 0, False

    for existing_delta_time in existing_delta_times:
        multiplier, new_delta_time_is_multiple = is_multiple(new_delta_time, existing_delta_time, tolerance)
        if new_delta_time_is_multiple:
            print(f"MS selecting {new_delta_time} as instance of {existing_delta_time} * {multiplier} = {existing_delta_time * multiplier}")
            return existing_delta_time * multiplier, False

    for existing_delta_time in existing_delta_times:
        denominator, new_delta_time_is_fraction = is_fraction(new_delta_time, existing_delta_time, tolerance, [2,3,4,5,8])
        if new_delta_time_is_fraction:
            print(f"DS selecting {new_delta_time} as instance of {existing_delta_time} / {denominator} = {existing_delta_time / denominator}")
            return int(existing_delta_time / denominator), True


    print(f"selecting {new_delta_time} as a unique delta time")
    return new_delta_time, True

