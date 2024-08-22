def mpq_to_bpm(mpq: int) -> int:
    return round((1000000 * 60)/mpq)

t500000 = mpq_to_bpm(500000)
msg = f"{t500000} is not correct"
assert t500000 == 120, msg

def bpm_to_mpq(bpm: int) -> int:
    return round((60 * 1000000)/bpm)

t120 = bpm_to_mpq(120)
msg = f"{t120} is not correct"
assert t120 == 500000, msg

assert mpq_to_bpm(bpm_to_mpq(50)) == 50
assert bpm_to_mpq(mpq_to_bpm(1000000)) == 1000000
