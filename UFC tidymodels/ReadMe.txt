URL: https://www.kaggle.com/datasets/remypereira/mma-dataset-2023-ufc?resource=download

MMA Dataset 2023 (UFC)
Dataset of UFC fights, fighters, and fight stats from 1994-2023.

About Dataset

Description

This is a dataset of every UFC fight from the first UFC event in 1994 to the most recent UFC event in 2023 (at the time of writing). It contains data on the events, the fighters, the fight, and a number of key fight stats.

The dataset can be used for fight predictions, exploratory data analyses, classification models, etc.

While there are other datasets on Kaggle that scrape similar data from ufcstats.com (see acknowledgements), what makes this dataset unique is that the data has been normalised to include primary and secondary keys. Each fight, event, fighter, and fight stat has a primary key in its respective table, which acts as a secondary key in the other tables.

This is my first attempt at creating a dataset from Kaggle, so all feedback is appreciated!

Source

All data was scraped from ufcstats.com using this web-scraping script: https://github.com/remypereira99/UFC-Web-Scraping

Column Definitions

ufc_events

    event_id - Primary key for ufc_events, unique for each event
    event_name - Name of the event, e.g. UFC 267
    event_date - Date of the event (YYYY-MM-DD)
    event_city - City the event was hosted
    event_state - State the event was hosted (if applicable)
    event_country - Country the event was hosted
    event_url - URL used to scrape event data from ufcstats.com

ufc_fights

    fight_id - Primary key for ufc_fights, unique for each fight
    event_id - Secondary key from ufc_events
    referee - Referee of the fight
    f_1 - Fighter 1
    f_2 - Fighter 2
    winner - Winner of the fight
    num_rounds - Number of rounds
    title_fight - Boolean for whether fight is a title fight or not
    weight_class - Weight class of the fight
    gender - Male or female fight
    result - How did the fight end, e.g. decision, KO
    result_details - Specific details of how the fight ended, e.g. KO by elbows, split decision
    finish_round - What round did the fight finish
    finish_time - What minute and second did the fight finish in that round (m:ss)
    fight_url - URL used to scrape fight data from ufcstats.com

ufc_fight_stats

    fight_stat_id - Primary key for ufc_fight_stats, unique for each fighter of each fight
    fight_id - Foreign key from ufc_fights
    fighter_id - Foreign key from ufc_fighters
    knockdowns - No. of knockdowns landed
    total_strikes_att - No. of strikes attempted
    total_strikes_succ - No. of successful strikes
    sig_strikes_att - No. of significant strikes attempted
    sig_strikes_succ - No. of significant strikes successful
    takedown_att - No. of takedown attempts
    takedown_succ - No. of successful takedowns
    submission_att - No. of submission attempts
    reversals - No. of reversals
    ctrl_time - Control time
    fighter_age - Age of the fighter
    winner - Boolean for whether fighter won or lost

ufc_fighters

    fighter_id - Primary key for ufc_fighters, unique for each fighter
    fighter_f_name - Fighter first name
    fighter_l_name - Fighter last name
    fighter_nickname - Fighter nickname
    fighter_height_cm - Fighter height in cm
    fighter_weight_lbs - Fighter weight in lbs
    fighter_reach_cm - Fighter reach in cm
    fighter_stance - Fighter stance - e.g. southpaw, orthodox
    fighter_dob - Fighter date of birth
    fighter_w - No. of wins (at the time of scraping)
    fighter_l - No. of losses (at the time of scraping)
    fighter_d - No. of draws (at the time of scraping)
    fighter_nc_dq - No. of no contests or disqualifications (at the time of scraping)
    fighter_url - URL used to scrape fighter data from ufcstats.com

Authors

Remy Pereira

Acknowledgements
MDABBERT's UFC Dataset
KARMANYA AGGARWAL's UFC Dataset
RAJEEV WARRIER's UFC Dataset
FATBARDH SMAJLI's UFC Dataset and web-scraping code