

def inch_to_mm(inch: float) -> float:
    return round(inch * 25.4, 2)

def mm_to_inch(mm: float) -> float:
    return round(mm / 25.4, 2)



from fractions import Fraction

def float_to_mixed_fraction(value: float) -> str:
    """
    Converts a float into a string with the closest mixed fraction using denominator 16.
    e.g. 1.5 -> '1 1/2', 0.75 -> '3/4', 2.1875 -> '2 3/16'
    
    Args:
        value (float): The input float value.
        
    Returns:
        str: Mixed fraction string.
    """
    if value < 0:
        raise ValueError("Negative values not supported")
    
    # Whole number part
    whole = int(value)
    frac = value - whole

    # Closest fraction with denominator 16
    nearest_frac = Fraction(round(frac * 16), 16)

    # Simplify the fraction
    nearest_frac = nearest_frac.limit_denominator(16)

    # Assemble the string
    if nearest_frac.numerator == 0:
        return str(whole)
    elif whole == 0:
        return f"{nearest_frac}"
    else:
        return f"{whole} {nearest_frac}"


if __name__ == "__main__":
    print(f"inch_to_mm(1.0) = {inch_to_mm(1.0)}")  # Should print 25.4
    print(f"mm_to_inch(25.4) = {mm_to_inch(25.4)}")  # Should print 1.0
    print(f"float_to_mixed_fraction(1.5) = {float_to_mixed_fraction(1.5)}")  # Should print '1 1/2'
    print(f"float_to_mixed_fraction(0.75) = {float_to_mixed_fraction(0.75)}")  # Should print '3/4'
    print(f"float_to_mixed_fraction(2.1875) = {float_to_mixed_fraction(2.1875)}")  # Should print '2 3/16'

