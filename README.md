# Traveling Politician Project 

### Description
The objective is to find the most efficient route for a politician to travel to every state capital once,
starting in Iowa, and ending in Washington, DC.


### Example Output
```
Optimized Route (Not including Alaska and Hawaii)

   1. Iowa (Des Moines)
   2. Nebraska (Lincoln)
   3. South Dakota (Pierre)
   4. North Dakota (Bismarck)
   5. Montana (Helena)
...
   46. Connecticut (Hartford)
   47. New Jersey (Trenton)
   48. Delaware (Dover)
   49. Maryland (Annapolis)
   50. Virginia (Richmond)
   51. Washington DC (Washington)

Total distance: 17,183.6 miles

```

### Assumptions / Limitations
- Distance is calculated as the crow flies (straight line distance)
- Doesn't account for actual travel paths

### How it works
1. Calculates distance from each capitol using coordinates and the haversine formula and creates a matrix with each capitol and its distance from each other
2. It first creates a route just by mapping out each capitols closest unvisted neighbor
3. It modifies the original route by improving any capitols whos paths cross over each other
