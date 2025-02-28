# essense-trade-helper
This is a tool designed to assist with Essence trading in Path of Exile. Essences are a currency item within the game that you can trade to other players. There are currently a lot of issues with trying to sell essences on your own without bulk selling your entire inventory tab of them. Selling your inventory tab of essences in bulk to another player to sell has the upside of convenience and one sale, with the downside of taking a variable percentage loss on the total value of the tab if you had sold them yourself. You are just paying a middle man essentially. I have long paid someone else to do my selling because of how annoying it is to do it yourself. But no longer! This tool tackles the root problems associated with trying to sell them on your own.

Issues:
1. POE trade api rate limiting - Due to path of exile(POE)'s trade api restrictions, you cannot price check frequently without getting rate limited. This prevents you from price checking all of the individual essences and their tiers without wasting an extreme amount of time. It is also extremely tedious to sit there and price check each essence.
2. Keeping track of your prior sales - Currently if you run out of the type of essence you are selling , the value tied to the trade listing is removed. This causes you to relist your trade when you have the essences again which means you need to repeat the process of price checking them. Keep in mind when you price check the individual essences you need to account for the price of the sale when you sell a bunch of essences of one type in bulk. Ex. selling 100 Shrieking Essences of Loathing instead of just 1-10 of them. The price per essence can be drastically different if you are only trying to sell a couple of them.
3. Knowing which essences you should "3 to 1" - Three to one is a vendor recipe that you can do to trade in 3 essences of 1 tier to get one essence of the same type but of a tier higher. Knowing which essences to do this vendor recipe on requires more individual price checking.

Solution:
This tool scrapes essence price data from a popular poe economy website, POE Ninja, and stores the information in a dictionary which can then be called on using the CLI options below that aim to fix the prior noted issues.

1. Instead of having to price check essences individually, you can get a price sheet that will tell you what the bulk listing should be for each essence and a quick look at what value you are getting per essence with the bulk trade if you are curios. Currently the bulk listing always assumes a supply of at least 27 of that type of essence. It accomplishes this by taking the price from POE Ninja and applying a multiplier to the individual price of the essence to get the bulk sale pricing. This is because the price on POE Ninja doesn't account for selling large amounts of the same type of essence. Players will pay more per essence in the sale if it means they dont need to make multiple trades with different people. This multiplier is just an estimate as it varies with each essence (it starts at 3x for each essence). This multiplier can be updated using the second option of the tool. See below.
2. Updates the multiplier associated with the essence of your choice. You will be prompted for the essence name and what your last successful listing was for the essences you sold (ex. 65/14). It does the math and stores the new multiplier so that the next time you need to get the listing value its there. You won't need to manually remember each change you make to a specific essence. This allows the tool to stay customizable and aligned with your actual sales.
3. If you want to get the most recent value of the essences, you can use this option and it will get the newest data from POE Ninja. NOTE!: This data doesn't change the multiplier associated with the underlying dictionary. This stays the same as it will more than likely still be the most appropriate multiplier to get your bulk price listing.
4. This option allows you to get a list of the suggested 3 to 1 essences. It gives you a list based on a comparison of the values between the screaming, shrieking, and deafening tiers of each essence. If you would get more value by upgrading the essence, it will be on the list of suggestions for an upgrade. 
5. Exits the program


How to run this program:
Need Python installed
Need to pip install selenium, beautifulsoup4, lxml
Depending on what environment you are running this from you will need to make sure that you have chrome installed on it, and the chrome webdriver. The location of webdriver needs to be put in /usr/local/bin/.
git clone the repository
The program can then be run directly by python3 main.py (NOTE: If the essenceinfo.txt file already exists in the project directory then delete it).

