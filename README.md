# hsrankedsim
## Introduction  
Greetings! This is a very simple Python simulation of Hearthstone® ranked matches I created with the purpose of learning and practicing some new things. As the final result might interest Hearthstone players or beginner developers like myself, I decided to leave it public.

The simulation source code is in [hsrankedsim.py](hsrankedsim.py). It was developed in Python 3.8 and uses the following modules/libraries:
* random
* csv
* matplotlib (for graph plots in the [Jupyter Notebook discussion](discussion.ipynb))
* statistics  (for calculations in the [Jupyter Notebook discussion](discussion.ipynb))

## How to use  
*class* hsrankedsim.**Player**(*name, star_bonus, deck_winrate, internal_rank, current_stars*):  
Instantiates a player object. This object will carry all the information throughout the simulation. The class has a few auxiliary methods (that I'm lot listing here)       and one main method: 

**play_season**(*self*, *tgt_internal_rank*, *csv_file*=False):  
Plays matches in a loop untill *self.internal_rank* == *tgt_internal_rank* and returns a list of dictionaries containing ordered information about the matches, where each dictionary corresponds to a match.
Here is how the list structure will look like:   

<p>[ {<i> 'player_name': self.name,<br>
'status': status,<br>
'accum_victories': accum_victories,<br>
'league': league,<br>
'rank': rank,<br>
'internal_rank': self.internal_rank,<br>
'stars': self.current_stars,<br>
'star_bonus': self.star_bonus,<br>
'total_matches': total_matches,<br>
'total_victories': total_victories,<br>
'total_defeats': total_defeats </i>},<br>
{<i> 'player_name': self.name,<br>
'status': status,<br>
'accum_victories': accum_victories,<br>
(...) </i>} ]</p>

The variable *internal_rank* is a mix of League and Rank to simplify the simulations and turn these two variables into a single one. It goes from 50 to 0, where:  

50 to 41 = Bronze 10 to Bronze 1  
40 to 31 = Silver 10 to Silver 1  
30 to 21 = Gold 10 to Gold 1  
20 to 11 = Platinum 10 to Platinum 1  
10 to 1  = Diamond 10 to Diamond 1  
0        = Legend  

The *csv_file* is an optional argument, with False as default value. If *csv_file* == True, the method saves in the current directory a csv file, the name of which being '*self.name*', with the data gathered from the simulations, instead of returning the list of dictionaries.

## Check the Jupyter Notebook
I made a discussion [here](discussion.ipynb), explaining a bit about how the ranks system work for those not familiar with it, running a few example simulations and extracting some interesting data from them. Check it out!
