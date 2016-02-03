from collections import defaultdict
from itertools import groupby


month_to_code = {1: 'jan', 2: 'feb', 3: 'mar', 4: 'april', 5: 'may', 6: 'jun',
                 7: 'jul', 8: 'aug', 9: 'sep', 10: 'oct', 11: 'nov', 12: 'dec'}

code_to_month = dict(zip(month_to_code.values(), month_to_code.keys()))