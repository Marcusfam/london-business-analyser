import googlemaps
import geopandas
from shapely.geometry import Polygon, LineString, Point
import matplotlib.pyplot as plt
import pandas as pd


def getAPI():
    with open("apikey.txt","r") as api_file:
        API_KEY=api_file.read()    #first line
        api_file.close()
        return API_KEY


#gmap api places call for every ward to find num instititutions fitting inside ward
def getNumOfInsitutions(ward,institutionType,WARDS_SEARCH_RADIUS):
    gmaps=googlemaps.Client(getAPI())
    location = str(ward[1].geometry.centroid.y)+"," +str(ward[1].geometry.centroid.x)
    institutions=gmaps.places_nearby(location=location ,radius=WARDS_SEARCH_RADIUS, open_now=False, type=institutionType)
    num_of_institutions=0
    for institutions in institutions["results"]:
        if fitsInside(ward,institutions["geometry"]["location"]):
            num_of_institutions=num_of_institutions+1
    return num_of_institutions


#finds wards in users range by parsing wards dataset
def find_WARDS_InRadius(centre,radius=2000):
    #open shapefile
    shapefile = geopandas.read_file("London_Ward_CityMerged.shp")
    points = shapefile.copy()
    # set the geometry column as centroids with 4326 projection
    points['tempGeo'] = points['geometry'].to_crs(epsg=27700)#tmp store of geometries whilst geometry column is converted to centroids
    points['geometry'] = points['geometry'].to_crs(epsg=27700).centroid
    #define radius/circle to consider wards in
    circle=centre.geometry.to_crs(epsg=7855).buffer(radius).to_crs(epsg=27700)
    #convert circle into dataframe
    circle_df=geopandas.GeoDataFrame(geometry=circle)
    #identify wards within radius/circle
    wards=geopandas.overlay(points,circle_df,how="intersection")
    wards['geometry'] =wards["tempGeo"]
    #plot wards on matplotlib map (for debugging/trivia)
    wards.plot()
    plt.show()
    print("Please Wait...")
    return wards


#trivial function to find if an institution fits within a ward's perimeter
def fitsInside(ward,institution):
    if Point(institution["lng"],institution["lat"]).within(ward[1].geometry):
        return True
    else:
        return False

#TODO check is __name__=main needed?????
if __name__ == '__main__':
    WARDS_SEARCH_RADIUS=1000 #Radius around the centroid of an ward to search for matches
   #
    with open("placeTypes.txt") as f:
        validInputs=(f.read())
    # Taking user inputs:
    while True:
        institutionType=input("Enter the type of institution you would like to inspect"
                          " \nEnter 'LIST' for list of allowed entries \n")
        if institutionType=="LIST":
                print(validInputs)

        else:
            if institutionType not in validInputs:
                continue
            else:
                break


    address = input("Enter address to centre your search from")

    while True:
        try:
            SEARCH_RADIUS = int(input("Enter radius of your search in metres (wards outside this will be ignored)"))
        except ValueError:
            print("Not valid entry")
            continue
        else:
            break


    # convert address entered into coordinates
    centre = pd.Series([address], name='address')
    centreCoded = geopandas.tools.geocode(centre, provider='nominatim', user_agent='ummm', timeout=4)

    #finds all wards in radius
    wards=find_WARDS_InRadius(centreCoded , int(SEARCH_RADIUS))
    wards4326=wards["geometry"].to_crs('EPSG:4326')
    list={}


    for ward in wards.to_crs('EPSG:4326').iterrows():
        #number of institutions matching criteria
        matches=getNumOfInsitutions(ward, institutionType, WARDS_SEARCH_RADIUS)
        #get population of the ward
        df = pd.read_excel('LONDON_WARD_DETAIL.xls',sheet_name="iadatasheet")

        #extract population of wards that are in the specified area from dataset
        popTemp=df.loc[df["Unnamed: 1"] == ward[1].GSS_CODE,["Unnamed: 12"]]
        # convert from geoseries to integer value
        pop=popTemp["Unnamed: 12"]
        pop=pop.array[0]
        # to avoid storing infinite values in dictionary and having to sort them
        if matches==0:
            ratio=0         #set ratio 0 rather than infinity when there is no matches in a ward so that it can be printed
        else:
            ratio = pop / matches
        list[ward[1].NAME]=ratio


    # sort desc order, so large ratios first
    sort_list = sorted(list.items(), key=lambda x: x[1], reverse=True)
    #move items to front of list if ratio is set to 0 (signifying no institutions)
    for index,x in enumerate(sort_list):
        if x[1]==0:
            sort_list.insert(0, sort_list.pop(index))


    #output results
    print("Area:      Ratio of people to institutions:     (Higher=>better)")
    index=1
    for i in sort_list:
        if i[1]==0:
            print(index, i[0], "-----"," No matching institutions in this area")
        else:
            print(index, i[0],"-----", i[1],": 1")
        index=index+1



