import pandas as pd

UNITS = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,

    # ✅ Added missing values (important fix)
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19
}

HUNDREDS = {
    "hundred": 100,
    "one hundred": 100,
    "two hundred": 200,
    "three hundred": 300,
    "four hundred": 400,
    "five hundred": 500,
    "six hundred": 600,
    "seven hundred": 700,
    "eight hundred": 800,
    "nine hundred": 900,
    "thousand": 1000,

    # ✅ Added lakh support
    "lakh": 100000,
    "one lakh": 100000
}

THOUSANDS = {
    "one thousand": 1000,
    "two thousand": 2000,
    "three thousand": 3000,
    "four thousand": 4000,
    "five thousand": 5000,
    "six thousand": 6000,
    "seven thousand": 7000,
    "eight thousand": 8000,
    "nine thousand": 9000,
    "ten thousand": 10000
}

TENS = {
    "twenty": 20,
    "thirty": 30,
    "forty": 40,
    "fifty": 50,
    "sixty": 60,
    "seventy": 70,
    "eighty": 80,
    "ninety": 90
}

TENTHOUANDS = {
    "twenty thousand": 20000,
    "thirty thousand": 30000,
    "forty thousand": 40000,
    "fifty thousand": 50000,
    "sixty thousand": 60000,
    "seventy thousand": 70000,
    "eighty thousand": 80000,
    "ninety thousand": 90000
}


def word_to_number(text):
    text = text.lower().strip().replace("-", " ")
    parts = text.split()

    total = 0
    current = 0

    for word in parts:

        if word in UNITS:
            current += UNITS[word]

        elif word in TENS:
            current += TENS[word]

        elif word == "hundred":
            if current == 0:
                return None
            current *= 100

        elif word == "thousand":
            if current == 0:
                return None
            total += current * 1000
            current = 0

        elif word == "lakh":
            if current == 0:
                return None
            total += current * 100000
            current = 0

        else:
            return None

    value = total + current

    # ✅ Enforce range (1 → 1 lakh)
    if 0 < value <= 100000:
        return value

    return None


def fix_datatypes(df):
    if df.empty:
        return df

    df = df.copy()

    for col in df.columns:
        if df[col].dtype == object:

            cleaned = df[col].astype(str).str.strip().str.lower()

            word_converted = cleaned.apply(word_to_number)
            numeric_converted = pd.to_numeric(cleaned, errors="coerce")

            combined = word_converted.combine_first(numeric_converted)

            numeric_ratio = combined.notna().sum() / len(df)

            if numeric_ratio >= 0.8:
                df[col] = combined

    return df