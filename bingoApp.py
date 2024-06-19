# Check diagonal lines (top-left to bottom-right)
if all((j, j) in marked_positions for j in range(max_feld)):
    return True

# Check diagonal lines (top-right to bottom-left)
if all((j, max_feld - 1 - j) in marked_positions for j in range(max_feld)):
    return True

return False