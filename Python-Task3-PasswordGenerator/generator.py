# """Password generation logic using the secrets module."""

# import secrets
# import string

# AMBIGUOUS = set("0O1lI|`'\"")
# SYMBOLS = "!@#$%^&*()-_=+[]{};:,.<>?"


# def build_pools(use_upper, use_lower, use_digits, use_symbols, exclude_ambiguous):
#     """Return a list of character pools (one per selected type)."""
#     pools = []

#     def clean(chars):
#         return [c for c in chars if not (exclude_ambiguous and c in AMBIGUOUS)]

#     if use_upper:
#         pools.append(clean(string.ascii_uppercase))
#     if use_lower:
#         pools.append(clean(string.ascii_lowercase))
#     if use_digits:
#         pools.append(clean(string.digits))
#     if use_symbols:
#         pools.append(clean(SYMBOLS))

#     return [p for p in pools if p]  # drop empty pools


# def generate_password(length, pools):
#     """Return a password of `length` chars, guaranteeing one char per pool."""
#     if not pools:
#         raise ValueError("Select at least one character type.")
#     if length < len(pools):
#         raise ValueError(
#             f"Length must be at least {len(pools)} for the selected types."
#         )

#     # 1. One guaranteed char from each pool
#     pwd = [secrets.choice(pool) for pool in pools]

#     # 2. Fill remaining length from the combined pool
#     combined = [c for pool in pools for c in pool]
#     pwd += [secrets.choice(combined) for _ in range(length - len(pools))]

#     # 3. Cryptographically secure shuffle
#     for i in range(len(pwd) - 1, 0, -1):
#         j = secrets.randbelow(i + 1)
#         pwd[i], pwd[j] = pwd[j], pwd[i]

#     return "".join(pwd)


# def strength_label(length, num_types):
#     """Return (label, color_hex) based on length and character diversity."""
#     score = 0
#     if length >= 8:  score += 1
#     if length >= 12: score += 1
#     if length >= 16: score += 1
#     if num_types >= 3: score += 1
#     if num_types == 4: score += 1

#     if score <= 1:
#         return "Very Weak", "#e74c3c"
#     if score == 2:
#         return "Weak", "#e67e22"
#     if score == 3:
#         return "Medium", "#f1c40f"
#     if score == 4:
#         return "Strong", "#2ecc71"
#     return "Very Strong", "#27ae60"