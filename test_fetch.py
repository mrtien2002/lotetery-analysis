from datetime import date 

from fetch_xsmb import fetch_for_date 

 

# Test 2 ngày gần nhất 

for d in [date(2025, 9, 7), date(2025, 9, 6)]: 

    print(d, fetch_for_date(d)) 
