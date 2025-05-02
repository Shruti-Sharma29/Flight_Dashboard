import mysql.connector

class mydb:
    def __init__(self):
        self.conn = mysql.connector.connect(host = "localhost", username = "root", password = "Python@0929", database = "flight_data")

        self.csr = self.conn.cursor()
    
    def get_cities(self):
        
        self.csr.execute("select distinct(Source) from flightsdata")

        cities = []
        for i in self.csr.fetchall():
            cities.append(i[0])
        # print(cites)
        return cities

    def get_destination_cities(self):

        self.csr.execute("select distinct(Destination) from flightsdata")
        dstn_cities = []
        for i in self.csr.fetchall():
            dstn_cities.append(i[0])
    
        return dstn_cities

    def get_flights_data(self, src, dstn):

        self.csr.execute(f"SELECT Airline, Source, Destination, Total_Stops, Price FROM flightsdata where Source = '{src}' and Destination = '{dstn}'")
       
        flights = self.csr.fetchall()

        return flights
    
    def airlines_flights(self):
        self.csr.execute("SELECT Airline, count(*) as x FROM flightsdata group by Airline order by x desc")
        data = self.csr.fetchall()
        airline_name = []
        flight_count = []

        for i in data:
            airline_name.append(i[0])
            flight_count.append(i[1])

        return airline_name, flight_count
    
    def buziest_airports(self):
        self.csr.execute("SELECT Source, count(*)as q FROM (SELECT source FROM flightsdata union all SELECT Destination FROM flightsdata) t group by t.source order by q desc")
        
        data = self.csr.fetchall()

        airport = []
        cty = []

        for i in data:
            airport.append(i[0])
            cty.append(i[1])

        return airport, cty

obj = mydb()
obj.airlines_flights()
