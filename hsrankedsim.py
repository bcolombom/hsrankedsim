import random
import csv

class Player:
    def __init__(self, name, star_bonus, deck_winrate, internal_rank, current_stars):
        self.name = name
        self.star_bonus = star_bonus
        self.deck_winrate = deck_winrate
        self.internal_rank = internal_rank
        self.current_stars = current_stars

    #Auxiliary methods------------------------------------------------------------
    def match_win(self):
        if random.random() < self.deck_winrate:
            return True
        else:
            return False


    def floor_brz(self):
        if (self.internal_rank % 5) == 0 and self.current_stars == 0:
            return True
        elif self.internal_rank > 40:   #Players can't lose stars at Bronze league
            return True
        else:
            return False


    def rank_up(self, stars):       #For a fixed 3 star slots, in all ranks
        star_sum = stars + self.current_stars
        if star_sum <= 3:
            rank_gain = 0
            star_rest = star_sum
        elif (star_sum % 3 == 0):
            rank_gain = star_sum // 3 - 1
            star_rest = 3
        else:
            rank_gain = star_sum // 3
            star_rest = star_sum % 3
        return rank_gain, star_rest


    def rank_down(self):           #For a fixed 3 star slots, in all ranks
        if self.floor_brz():
            rank_loss = 0
            star_rest = self.current_stars
        elif (self.current_stars - 1) < 0:
            rank_loss = 1
            star_rest = 2
        else:
            rank_loss = 0
            star_rest = (self.current_stars - 1)
        return rank_loss, star_rest


    def convert_internal_rank(self):
        if self.internal_rank > 40 and self.internal_rank <= 50:
            league = 'Bronze'
            rank = self.internal_rank - 40
        elif self.internal_rank > 30 and self.internal_rank <= 40:
            league = 'Silver'
            rank = self.internal_rank - 30
        elif self.internal_rank > 20 and self.internal_rank <= 30:
            league = 'Gold'
            rank = self.internal_rank - 20
        elif self.internal_rank > 10 and self.internal_rank <= 20:
            league = 'Platinum'
            rank = self.internal_rank - 10
        elif self.internal_rank > 0 and self.internal_rank <= 10:
            league = 'Diamond'
            rank = self.internal_rank
        elif self.internal_rank <= 0:
            league = 'Legend'
            rank = 'Legend'
        return league, rank


    def winstreak(self, accum_victories):       #Winstreak is defined as 3, or more, consecutive victories.
        if accum_victories > 2:
            return True
        else:
            return False


    def check_next_floor(self):
        next_rank_floor = self.internal_rank
        if next_rank_floor % 5 == 0:
            next_rank_floor -= 1
        while next_rank_floor % 5 != 0:
            next_rank_floor -= 1
        return next_rank_floor


    def update_star_bonus(self, previous_floor):
        next_floor = self.check_next_floor()
        if previous_floor != next_floor and self.star_bonus > 1:
            self.star_bonus -= 1

    #End of auxiliary methods-----------------------------------------------------
    
    def play_season(self, tgt_internal_rank, csv_file=False):
        if self.internal_rank == tgt_internal_rank:
            return None
        
        accum_victories = 0     #Always starts without a winstreak
        total_matches, total_victories, total_defeats = 0, 0, 0
        season_log = []

        while self.internal_rank > tgt_internal_rank:
            total_matches += 1
            if self.match_win():    #Match victory condition
                status = 'V'
                total_victories += 1
                previous_floor = self.check_next_floor()
                accum_victories += 1
                winstreak = self.winstreak(accum_victories)
                if winstreak and self.internal_rank > 5:    #Winstreak bonus stars are disabled past rank 5
                    star_balance = 2 * self.star_bonus
                else:
                    star_balance = self.star_bonus
                r, s = self.rank_up(star_balance)
                self.internal_rank -= r
                self.current_stars = s
                self.update_star_bonus(previous_floor)
            else:   #Match defeat condition
                status = 'D'
                total_defeats += 1
                accum_victories = 0
                r, s = self.rank_down()
                self.internal_rank += r
                self.current_stars = s

            league, rank = self.convert_internal_rank()
            match_log = {'player_name': self.name,
                         'status': status,
                         'accum_victories': accum_victories,
                         'league': league,
                         'rank': rank,
                         'internal_rank': self.internal_rank,
                         'stars': self.current_stars,
                         'star_bonus': self.star_bonus,
                         'total_matches': total_matches,
                         'total_victories': total_victories,
                         'total_defeats': total_defeats}
            season_log.append(match_log)

        if csv_file == True:
            with open(f'{self.name}.csv', 'w', newline='') as new_file:
                fieldnames = ['Player name', 'Status', 'Accumulated victories', 'League', 'Rank', 'Internal rank', 'Stars', 'Star bonus',
                'Total matches', 'Total victories', 'Total defeats']
                csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames, delimiter=',')
                csv_writer.writeheader()

                for match in season_log:
                    csv_writer.writerow({'Player name': match['player_name'],
                    'Status': match['status'],
                    'Accumulated victories': match['accum_victories'],
                    'League': match['league'],
                    'Rank': match['rank'],
                    'Internal rank': match['internal_rank'],
                    'Stars': match['stars'],
                    'Star bonus': match['star_bonus'],
                    'Total matches': match['total_matches'],
                    'Total victories': match['total_victories'],
                    'Total defeats': match['total_defeats']})
            return None
        else:
            return season_log