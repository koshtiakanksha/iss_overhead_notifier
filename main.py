import requests
import datetime as dt
import smtplib

lat = 1.34565
lng = 6.23456
my_email = "*****"
my_password = "*****"


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    latitude = float(data["iss_position"]["latitude"])
    longitude = float(data["iss_position"]["latitude"])
    if lat-5 <= latitude <= lat+5 and lng-5 <= longitude <= lng+5:
        return True


def is_night():
    parameters = {
        "lat": lat,
        "lng": lng,
        "formatted": 0
    }

    response2 = requests.get(url=f"https://api.sunrise-sunset.org/json", params=parameters)
    response2.raise_for_status()
    data2 = response2.json()
    sunrise = int(data2["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data2["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = dt.datetime.now().hour
    if time_now >= sunset or time_now <= sunrise:
        return True


if is_iss_overhead() and is_night():
    connection = smtplib.SMTP("smtp.gmail.com", 587)
    connection.starttls()
    connection.login(my_email, my_password)
    connection.sendmail(
        from_addr=my_email,
        to_addrs="*****",
        msg="Subject:Look up!\n\nThe ISS is above you in the sky."
    )
