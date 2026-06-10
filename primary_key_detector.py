def detect_primary_key(df):
    best_candidate = None
    best_score = 0

    for col in df.columns:
        col_name = col.lower().replace(" ", "").replace("_", "")

        # Name score
        name_score = 0
        if "id" in col_name:
            name_score = 3
        elif "roll" in col_name or "reg" in col_name:
            name_score = 2
        elif "number" in col_name:
            name_score = 1

        if name_score == 0:
            continue

        total_rows = len(df)
        non_null = df[col].notna().sum()
        unique_vals = df[col].nunique(dropna=True)

        uniqueness_ratio = unique_vals / total_rows if total_rows else 0
        null_ratio = 1 - (non_null / total_rows) if total_rows else 1

        # Scoring logic
        score = 0
        score += name_score * 2
        if uniqueness_ratio >= 0.95:
            score += 3
        if null_ratio <= 0.05:
            score += 2

        if score > best_score:
            best_score = score
            best_candidate = col

    # Minimum confidence threshold
    return best_candidate if best_score >= 5 else None
