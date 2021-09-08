An axie price sniper that actively searches for targetted price of the axies from the user's query.
The code is a mess, bear with me. I did this in a single afternoon.

Once found a cheap axie, it will open the link to the marketplace and play a sound. 
It doesn't buy the axie for you because the only way I could think of making something like this would be through an extension and, personally, it would also become a market bot instead of just price sniping.

-price [value] is **needed** for every query. 

A command example would be:

```
add -class beast -speed 43 50 -price 300
```

Once all your queries are listed, you can just save and load every run for QoL.
