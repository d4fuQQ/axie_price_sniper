An axie price sniper that actively searches for targetted price of the axies from the user's query.
The code is a mess, bear with me. I did this in a single afternoon.

Be aware that:
1. This is not made for public use, but if you want to, go ahead.
2. I didn't hygienize enough the queries, so bear in mind you could fuck up if you don't follow it properly.
3. There are probably better ways to make this and to organize the code.


Once found a cheap axie, it will open the link to the marketplace and play a sound. 
It doesn't buy the axie for you because the only way I could think of making something like this would be through an extension and, personally, it would also become a market bot instead of just price sniping.

-price [value] is **needed** for every query. 

A command example would be:

```
add -class beast -hp 27 32 -speed 43 50 -price 300
```

Once all your queries are listed, you can just save and load every run for QoL.
