# NADEEF contraints

We leveraged both functional dependencies and denial constraints to detect errors with NADEEF. 
Here is the list of constraints that we leveraged for each dataset:

## Beers:
```
rules.append(UDF('ibu', 'value.equals("N/A")'))
rules.append(UDF('abv', '(value != null && !isNumeric(value))'))
rules.append(UDF('city', '((String)tuple.get("state") == null)'))
rules.append(UDF('state', '(value == null)'))
```

## Address:
```
rules.append(UDF('state', 'value != null && value.length() != 2'))
rules.append(UDF('zip', '(value != null && value.length() != 5)'))
rules.append(UDF('ssn', '(value != null && !isNumeric(value))'))
rules.append(UDF('city', 'value != null && value.equals("SAN")'))
rules.append(UDF('city', 'value != null && value.equals("SANTA")'))
rules.append(UDF('city', 'value != null && value.equals("LOS")'))
rules.append(UDF('city', 'value != null && value.equals("EL")'))
rules.append(UDF('city', 'value != null && value.equals("NORTH")'))
rules.append(UDF('city', 'value != null && value.equals("PALM")'))
rules.append(UDF('city', 'value != null && value.equals("WEST")'))
```

The following functional dependencies only lowered the F1-score. Therefore, we did not use them:
```
rules.append(FD(Set(["ZIP"]), "State"))
rules.append(FD(Set(["Address"]), "State"))
```

## Citations:
```
rules.append(UDF('article_jissue', 'value == null'))
rules.append(UDF('article_jvolumn', 'value == null'))
rules.append(FD(Set(['jounral_abbreviation']), 'journal_issn'))
```

## Flights:
```
rules.append(UDF('sched_dep_time', 'value == null || (value != null && value.length() > 10)'))
rules.append(UDF('act_dep_time', 'value == null || (value != null && value.length() > 10)'))
rules.append(UDF('sched_arr_time', 'value == null || (value != null && value.length() > 10)'))
rules.append(UDF('act_arr_time', 'value == null || (value != null && value.length() > 10)'))
```

## Hospital:
```
rules.append(UDF('provider_number', '(value != null && !isNumeric(value))'))
rules.append(UDF('zip_code', '(value != null && !isNumeric(value))'))
rules.append(UDF('phone_number', '(value != null && !isNumeric(value))'))
rules.append(UDF('emergency_service', '!(value.equals("Yes") || value.equals("No"))'))
rules.append(UDF('state', '!(value.equals("AL") || value.equals("AK"))'))
```

## Movies:
```
rules.append(UDF('Year', 'value != null && value.length() != 4'))
rules.append(UDF('RatingValue', 'value != null && value.length() != 3'))
rules.append(UDF('Id', 'value != null && value.length() != 9'))
rules.append(UDF('Duration', 'value != null && value.length() > 7'))
```

## Restaurants:
No constraints

## Salary:
```
rules.append(UDF('totalpay', 'Double.parseDouble(value) < 0'))
```





