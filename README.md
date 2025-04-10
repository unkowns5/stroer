#### Currency Api

- With fawazahmed0's exchange api, I decided to cache the result since it provides all the rates, so as long as the base currency doesn't change it only requires one call
- Frankfurter on the other hand, since the api accepts selective symbols, I opt into using that since its a lighter response to consume. If I had more time I would've build an additive dictionary instead of only caching each request results. e.g. USD and USD,GBP would be stored as one instead of separately.
- I decided to do the metric count since its simple enough where a library is a bit excessive
- If I had more time, improvements I would've added
    - testing
    - more safety incase the requests fails
    - clean up so its easier to add in new apis for the average
