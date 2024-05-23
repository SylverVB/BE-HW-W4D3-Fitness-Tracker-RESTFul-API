CREATE DATABASE fitness_tracker;

USE fitness_tracker;

DROP TABLE Members;

CREATE TABLE Members (
    member_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(150),
    phone_number VARCHAR(150),
    credit_card VARCHAR(30)
);

INSERT INTO Members (name, email, phone_number, credit_card)
VALUES ("Ace Ventura", "petdetective@gmail.com", "6309286808", "4300123456785622"),
		("Lando Calrissian", "lando@gmail.com", "63092864651", "4300123456788701"),
        ("Johnny Depp", "actor@gmail.com", "2156743456", "4300123456783729");

Select *
FROM Members;

CREATE TABLE Workouts (
	workout_id INT AUTO_INCREMENT PRIMARY KEY,
    session VARCHAR(150) NOT NULL, 
    date DATE NOT NULL, 
    time TIME NOT NULL,
    member_id INT,
    FOREIGN KEY (member_id) REFERENCES Members(member_id)
);

DROP TABLE Workouts;
        
INSERT INTO Workouts (session, date, time, member_id)
VALUES ("Aerobic", "2024-05-25", "08:30:00", 1),
		("Cycling", "2024-05-26", "10:00:00", 1),
        ("Cardio", "2024-05-27", "9:00:00", 1);
        
SELECT * 
FROM Workouts;