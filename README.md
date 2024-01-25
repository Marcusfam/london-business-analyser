# London-Business-Analyser

Program that predicts demand for types of business.

Data from the ONS and the Google Maps API are used to calculate the optimal location for different retail insitutions

Ratio of population density to the number of matching institutions is outputted for each area to find areas with most demand

## Sample
Attempt to find the best location to place a bar within 5km of east acton

https://user-images.githubusercontent.com/68549890/190403307-06f405b1-e560-4b93-bbb2-d61029483061.mp4

## Usage
Must create text file called apikey.txt with a valid api key before running program

Filter businesses by "Type". Enter "LIST" to inspect options

Enter area you would like to inspect 

Enter a certain radius (below 3000 metres to avoid too many api calls)

## Limitations & Warnings
Reckless use of the Google Maps api can amount to a costly bill.

Multiple scans of the whole london are not recommended.

Review spending on the google maps platform regularly


## Future developments
Program will be modified to filter population densities based on **multiple** data points such as religion and age which are already included in the LONDON_WARD_DETAIL.xls file.

In other words, only populations who fit a certain criteria will be considered when comparing the number of people to macthing institutions for each area

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.






