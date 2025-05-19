* ~~Validate if old API integration can still function with new libraries~~
* ~~Return dummy responses from Chopbot for a valid Slack payload~~
* ~~Redirect slack to this machine and validate they can talk (or to AWS?)~~
* ~~Work locally and get familiar with debugging process~~
* ~~Cannibalize code from old chopbot~~
  * Determine new frameworks to replace old stuff
* ~~Push to new repo~~
* ~~Finish enabling API gateway to respond immediately and have lambda follow async~~
  * ~~Need to track API Gateway config changes in template~~
      * ~~Permissions isn't being allocated to API GW correctly~~
      * ~~text/html mapping isn't able to be defined~~
* Save secrets in secrets manager
  * (What secrets?) API token that slack passes
  * Figure out how to put this in template

* Add API authorization
* ~~Refactor storage mechanism to respond within needed timeframe~~
* Clean up readme