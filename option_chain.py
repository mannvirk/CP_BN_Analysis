
def analyze_oi(df, spot):
    ce = df[df["instrument_type"] == "CE"]
    pe = df[df["instrument_type"] == "PE"]

    pcr = pe["open_interest"].sum() / ce["open_interest"].sum()

    itm_ce = ce[ce["strike"] < spot]["open_interest"].sum()
    itm_pe = pe[pe["strike"] > spot]["open_interest"].sum()

    return {
        "Total CE OI": int(ce["open_interest"].sum()),
        "Total PE OI": int(pe["open_interest"].sum()),
        "PCR": round(pcr, 2),
        "ITM CE OI": int(itm_ce),
        "ITM PE OI": int(itm_pe)
    }
