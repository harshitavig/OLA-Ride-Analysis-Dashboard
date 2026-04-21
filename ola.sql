CREATE DATABASE ola_project;
USE ola_project;
CREATE TABLE bookings (
    Date DATETIME,
    Time TIME,
    Booking_ID VARCHAR(50),
    Booking_Status VARCHAR(50),
    Customer_ID VARCHAR(50),
    Vehicle_Type VARCHAR(50),
    Pickup_Location VARCHAR(100),
    Drop_Location VARCHAR(100),
    V_TAT FLOAT,
    C_TAT FLOAT,
    Canceled_Rides_by_Customer VARCHAR(255),
    Canceled_Rides_by_Driver VARCHAR(255),
    Incomplete_Rides VARCHAR(10),
    Incomplete_Rides_Reason VARCHAR(255),
    Booking_Value FLOAT,
    Payment_Method VARCHAR(50),
    Ride_Distance FLOAT,
    Driver_Ratings VARCHAR(20),
    Customer_Rating VARCHAR(20)
);

select * from bookings;

# 1. Retrieve all successful bookings
SELECT *
FROM bookings
WHERE Booking_Status = 'Success'

#2. Find the average ride distance for each vehicle type
 SELECT Vehicle_Type,
       AVG(Ride_Distance) AS avg_distance
 FROM bookings
 GROUP BY Vehicle_Type;
 
#3. Get the total number of cancelled rides by customers:
SELECT COUNT(*) AS cancelled_by_customers
FROM bookings
WHERE Booking_Status = 'Canceled by customer'

#4. List the top 5 customers who booked the highest number of rides:
SELECT Customer_ID,
       COUNT(Booking_ID) AS total_rides
FROM bookings
GROUP BY Customer_ID
ORDER BY total_rides DESC
LIMIT 5;

#5. Get the number of rides cancelled by drivers due to personal and car-related issues:
SELECT 
    Canceled_Rides_by_Driver,
    COUNT(*) as cancelled_rides
FROM bookings
WHERE Canceled_Rides_by_Driver='Personal & Car related issue';

#6. Find the maximum and minimum driver ratings for Prime Sedan bookings:
SELECT 
    MAX(Driver_Ratings) AS max_rating,
    MIN(Driver_Ratings) AS min_rating
FROM bookings
WHERE Vehicle_Type = 'Prime Sedan';

#7. Retrieve all rides where payment was made using UPI:
SELECT *
FROM bookings
WHERE Payment_Method = 'UPI';

#8. Find the average customer rating per vehicle type:
SELECT Vehicle_Type,
       AVG(Customer_Rating) AS avg_customer_rating
FROM bookings
GROUP BY Vehicle_Type;

#9. Calculate the total booking value of rides completed successfully:
SELECT SUM(Booking_Value) AS total_success_revenue
FROM bookings
WHERE Booking_Status = 'Success';

#10.List all incomplete rides along with the reason
SELECT 
    Booking_ID,
    Customer_ID,
    Vehicle_Type,
    Incomplete_rides,
    Incomplete_Rides_Reason
FROM bookings
WHERE Incomplete_rides = 'Yes';