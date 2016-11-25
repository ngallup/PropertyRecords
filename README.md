# PropertyRecords
Prototype scraper written in Python for locating potential leads for motivated sellers in the Tulsa real estate market

Function is currently useable but not user-friendly.  Current development goals are to finish construction of a basic Google Maps-like UI that link the current utilities together for quick visualization of important data that could be relevant to a real estate investor looking for leads on potential motivated sellers.

Immediate goals are to complete this UI.  Upon clicking an individual property, a streamlined embedded window should pop up over the map with details about the property.  Immediate goals for these details include:
1. Property address, bed/bath, SF
2. Property owner(s)
3. Latest purchase year and price
4. Status on foreclosure and eviction records related to the owner (links to court docs)
5. Projected owner equity % (extrapolated from purchase year, average interest rates of that year, and predicted minimum payments)
6. Tax status (current on property taxes?)
7. Owner-occupied?

Longer term goals are to allow the user to highlight an area or type in a zipcode and gather a large list/table of sortable data with the above parameters.

Extra-long term goals are to implement a network-based actor model analysis for predicting the trajectory of crime densities across the Tulsa city based on research done by faculty in criminology and anthropology at UCLA for preempting long-term property value increases.

Some workflow ideas for going from map UI to data
click geocoded image --> get long/lat --> feed into geocode services --> get address (clean if necessary) --> feed address into TulsaAssessor object --> process and get owners --> feed owners into OkCourt object --> get records --> display formatted data on map and wait for new click
