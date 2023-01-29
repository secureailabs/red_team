import numpy as np
import pandas as pd
from scipy.stats import truncnorm

us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
}

states = [
    "California",
    "Texas",
    "Florida",
    "New York",
    "Pennsylvania",
    "Illinois",
    "Ohio",
    "Georgia",
    "North Carolina",
    "Michigan",
    "New Jersey",
    "Virginia",
    "Washington",
    "Arizona",
    "Massachusetts",
    "Tennessee",
    "Indiana",
    "Maryland",
    "Missouri",
    "Colorado",
    "Wisconsin",
    "Minnesota",
    "South Carolina",
    "Alabama",
    "Louisiana",
    "Kentucky",
    "Oregon",
    "Oklahoma",
    "Connecticut",
    "Utah",
    "Iowa",
    "Nevada",
    "Arkansas",
    "Kansas",
    "Mississippi",
    "New Mexico",
    "Nebraska",
    "Idaho",
    "West Virginia",
    "Hawaii",
    "New Hampshire",
    "Maine",
    "Montana",
    "Rhode Island",
    "Delaware",
    "South Dakota",
    "North Dakota",
    "Alaska",
    "Vermont",
    "Wyoming",
]
states.reverse()

for i in range(len(states)):
    states[i] = us_state_to_abbrev[states[i]]

gender = ["male", "female"]

questions = [
    "Did you experience occasional depression?",
    "Did you experience frequent mood swings?",
    "Did you experience changes in sleeping habits?",
    "Did you experience unawared wandering at night?",
    "Do you have a general feeling of distrust on other people?",
]
symptoms = [
    "Depression",
    "Moode swing",
    "Change in sleeping habits",
    "Unawared wandering at night",
    "Distrust on other people",
]
answer_for_question = ["yes", "no"]


def draw_random_normal_int(low: int, high: int):
    scale = 5.0
    range = (high - low) / 2
    size = 10000

    X = truncnorm(a=-range / scale, b=+range / scale, scale=scale).rvs(size=size)
    X = X.round().astype(int)
    return X + int((high + low) / 2)


def draw_random_gamma_int(k, theta, cutoff):
    gamma = np.random.gamma(k, theta, 10000)
    gamma[gamma < cutoff] = 0
    gamma[gamma > cutoff] = 1
    return gamma


def draw_decrease_prob(weights):
    tot = np.sum(weights)
    return weights / tot


number_states = len(states)
weights = np.exp(np.arange(0, 7.5, 0.15)) + 50 + np.random.uniform(-50, 50, 50)
prob = draw_decrease_prob(weights)
data_states = np.random.choice(
    a=states,
    size=10000,
    p=prob,
)

data_age = draw_random_normal_int(42, 95)

data_gender = np.random.choice(
    a=["male", "female"],
    size=10000,
    p=[0.5, 0.5],
)

data_question = [
    draw_random_gamma_int(1, 2, 6),
    draw_random_gamma_int(2, 2, 2),
    draw_random_gamma_int(9, 0.5, 3),
    draw_random_gamma_int(2, 2, 8),
    draw_random_gamma_int(5, 1, 6),
]

data_year = np.random.choice(
    a=[2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022],
    size=10000,
    p=[0.078, 0.082, 0.09, 0.07, 0.085, 0.075, 0.08, 0.14, 0.15, 0.15],
)

df = pd.DataFrame()
df["age"] = data_age
df["gender"] = data_gender
df["state"] = data_states
df["year"] = data_year
for i in range(5):
    df[symptoms[i]] = data_question[i]

PATIENT_DF = df

# print(df["age"].value_counts())
# print(df["gender"].value_counts())
# print(list(df["state"].value_counts().keys()))
# print(df["diagnosis_year"].value_counts())
# for i in range(5):
#     print(df[symptoms[i]].value_counts())
