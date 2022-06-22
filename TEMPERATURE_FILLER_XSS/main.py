import time
import os
from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver

USERS = [
    # [name, userid, pin, start date, end date],
]
URL = 'https://temptaking.ado.sg/group/'

# Default start & end date
START_DATE = "08/25/2020"
END_DATE = "08/31/2020"

TEMP_WEIGHTS = """
  0:0.05,
  1:0.05,
  2:0.075,
  3:0.075,
  4:0.4,
  5:0.5,
  6:0.5,
  7:0.3,
  8:0.1,
  9:0.025,
"""
DELTA_TEMP_WEIGHT = """
  1:0.1,
  2:0.8,
  3:0.2,
  4:0.8,
  5:0.1,
"""

drivers = os.path("drivers")


def create_browser(browser: str) -> WebDriver:
    if browser == "chrome":
        return webdriver.Chrome(
            os.path.join("drivers", "chromedriver.exe")
        )
    elif browser == "firefox":
        return webdriver.Firefox(
            os.path.join("drivers", "geckodriver")
        )
    raise(f"Only chrome or firefox is supported, you provided: {browser}")


def quit_browser(driver: WebDriver) -> None:
    driver.close()


def handle_user(browser: WebDriver, name: str,
                userid: str, pin: str,
                start_date: str, end_date: str) -> None:

    print("Init", name + '(' + userid + ')', 'PIN: ' + pin)

    start_time = time.perf_counter()
    start_date = start_date and start_date or START_DATE
    end_date = end_date and end_date or END_DATE

    script = """
        var startDate = new Date("R_STARTDATE");
        var endDate = new Date("R_ENDSTART");

        function submitTemperature(date, meridies, temperature) {
            $.ajax({
                type: "post",
                url: "MemberSubmitTemperature",
                data: {
                    groupCode: "redacted",
                    date: date,
                    meridies: meridies,
                    memberId: R_MEMBERID,
                    temperature: temperature,
                    pin: R_PIN
                }
            }).done(function (results) {
                if (results === "OK") {
                    console.log("DONE", date, meridies, temperature);
                    $("#modal").modal("hide");
                    var dbleTemp = parseFloat(temperature);
                    if (dbleTemp >= 38.0) {
                        $("#main-content-with-title").hide();
                        $("#results-container").show();
                        $("#no-fever-container").hide();
                        $("#fever-container").show();
                    } else {
                        $("#main-content-with-title").hide();
                        $("#results-container").show();
                        $("#fever-container").hide();
                        $("#no-fever-container").show();
                    }
                } else {
                    document.getElementById(
                        "main-content-with-title").innerHTML = '<h1 style="color: #007BA4; margin: 10px 0px 20px 0px; font-weight: bold;" align="center">' + results + '</h1>'
                }
            });
        }

        function weightedRand(spec) {
          var i, j, table=[];
          for (i in spec) {
            for (j=0; j<spec[i]*10; j++) {
              table.push(i);
            }
          }
          return function() {
            return table[Math.floor(Math.random() * table.length)];
          }
        }

        var intialTemp = weightedRand({
          R_TEMP_WEIGHTS
        });

        var deltaTemp = weightedRand({
          R_DELTA_TEMP_WEIGHTS
        });

        var currDate = new Date(startDate);
        while(currDate <= endDate){
           var dateStr = Intl.DateTimeFormat("ca-ES").format(currDate);

           var tempA = 36 + 0.1 * intialTemp()
           var tempB = Math.round(10 * (tempA + (deltaTemp()-3) / 10))/10

           submitTemperature(dateStr, "PM", tempB)
           submitTemperature(dateStr, "AM", tempA)

           var newDate = currDate.setDate(currDate.getDate() + 1);
           currDate = new Date(newDate);
        }
    """
    script = script.replace("R_TEMP_WEIGHTS", TEMP_WEIGHTS)
    script = script.replace("R_DELTA_TEMP_WEIGHTS", DELTA_TEMP_WEIGHT)
    script = script.replace("R_MEMBERID", userid)
    script = script.replace("R_PIN", pin)
    script = script.replace("R_STARTDATE", start_date)
    script = script.replace("R_ENDSTART", end_date)

    browser.execute_script(script)

    print("Finished for " + name + " Time elapsed: " +
          str(time.perf_counter() - start_time - 1))


def main() -> None:
    driver = create_browser(browser="chrome")

    for user in USERS:
        driver.get()
        handle_user(
            driver,
            user[0], user[1], user[2], user[3], user[4]
        )
        time.sleep(1)

    quit_browser(driver=driver)
    print("Executed successfully")


if __name__ == "__main__":
    main()
