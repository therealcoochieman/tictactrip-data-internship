# tictactrip-data-internship
Data exercise for Tictactrip using python, pandas, and other libraries! Uploaded on Monday 01/05/2023. The deadline is tomorrow, always right on time. 😎

## My technical background
  As you will see in the code, I use extensively (almost exclusively) dictionaries. This is mainly due to my life motto, "*If you don't know how to solve a problem, throw a HashMap at it*."
 
 ## Classes, IDs, and more Dictionnaries
  
  After modelling my classes (cities, stations, ticket_data, providers), I use Pandas to load up the CSV files - which can be found in the **Resources** directory - into dictionaries, using their ID columns as key, and as value the object holding all the other information. 
    
Throughout the whole project, I have decided to only use the IDs to navigate as it allowed me to use int (not too heavy on memory when passed as function arguments and such). Everytime I would need more information, Dictionaries allowed me to access them in O(1).

Most of the sub-dictionaries I use (as when I need to re-arrange tickets by distance intervals) are using lists as values. I thought of using NumPy to accelerate calculations the most I could, but decided it would not be necessary. (NumPy stores its arrays in contiguous memory spaces, which kind of hurts sometimes)

## Implementation

Most of the algorithms used followed the same principle, iterate through the ticket_data dict in order to filter/compute the interesting metric at hand. I used this method to compute route prices & durations. As you will see in the code, the computation changes a little when the user chooses specific places because then we need to filter through the tickets to get the interesting ones before iterating through them.

Computing prices and durations depending on distance intervals was quite fun as I had to take multiple things into account. I split the data into 4 categories, each representing a transportation method. This allowed me, for each interval (200km, 800km, 2000km, > 2000km) to get more specific in my averages.

Predicting prices was the most fun part overall. Mainly thanks to the fact that I used Tictactrip's website to see if my predictions were correct. Most of the time, they were! Of course it depends on when we are trying to plan the trip, I used non-holiday time periods as reference. I feel like I kind of cheated for the prediction part, as I am only using the split intervals from before to compute my predictions. Working on predictions also obligated me to work on user inputs. The more interactive the merrier, am I right?

User inputs made me rework the way I was treating the city CSV file. I created another dictionaries of cities - which, all in all, contains the same information as the original dict, just rearranged. This new and fresh dictionary was layed out to resemble a map. The key is a string, representing the name of a country (France, Spain, Portugal, ...), its value was another dict! This one used as keys the regions of before-chosen country, and had as values the IDs of the city in that region, which was in that country. This was quite a knot but in the end, I think it works well (even if it might be a bit janky? I did not find any other way to make it work so logically)

Then, I let myself go on a Terminal User Interface rampage and implemented a little dashboard to navigate the whole project a little better. I also added a few cute/fun/whatever-you-want-to-call-it messages here and there.

## Comments, limitations

I am quite afraid I missed chunks of the real purpose of the exercise, I feel like I did not use all the data I had in the provided files, but I did not really know what to do with them. Information such as Search dates were not useful in any of my crunching, I feel like I could have used it to predict prices according to search dates, but it became quite a lot when providers and different transportation types also came into play. I would love to talk this over, as I am sure you guys had some uses for the data that I did not use and I would love to know how you use them.

I found a lot of uh... *funny business* going on in the data? I found countries duplicated, like we had "Spain" and "Espana", "Allemagne" and "Germany". I did not manage to merge them but in order to be able to type them in my UI thingy, I used the unidecode function (from the unidecode package) to remove all accents. Overall, my favorite shenanigans definitely were the "OMG WTF" city (I googled it afterwards, very cute place if you ask me), or the 124 country (maybe that is a thing and I am uncultured?). But the creme, the cherry on top, the bestest jankiest thing I found: the ", , " city, and its cousin ", , United Kingdom". I actually am glad to have had them in my data as they allowed me to filter things out much better.

I am sure I missed some other, but still, pretty funny to see.

## Conclusion
This was a fun project to go through! You guys said that the more bonus things the better, so I kind of let myself go and tried things out. I am glad I had the chance to see something less "academic-y." School is fun but it is a pain. I took this exercise as a cool "summer" project I was doing during my holidays. (I did take it very seriously though!!! I loooove serious stuff.)

Thank you for the opportunity and I hope I will hear from you soon!

Théo De Magalhaes.
