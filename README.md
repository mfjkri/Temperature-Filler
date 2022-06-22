### ⚠️ This project was made and used for only a short span of time hence does not include the best practices.

### ⚠️ The temperature filling website is no longer up, hence why I deemed it alright to upload this repo.

### ❗️ DO NOT USE THIS REPO WITH MALICIOUS INTENT.

---

&nbsp;

## An old project I made in 2020 to help me mass-fill missing daily temperature taking for the past 6 months.

Temperatures filled are randomly generated and not actual temperatures.

### Includes two modes for filling up temperatures

- Web mode:

  This mode uses the website interface and automates clicking of buttons.

  It was still heavily limited by the rate at which the website updates and the efficiency of `selenium` in finding and clicking the relevant buttons.

- XSS mode:

  This mode executes a script on the browser that sends a POST request to the server with the relevant data fields.

  It is able to send out multiple requests per second without being rate-limited.
