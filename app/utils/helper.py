
def convert_mktcap_to_number(mktcap: str) -> float:
    """
    Convert mktcap from caategories to number
    """
    if mktcap == "mega":
        mktcap_thres = 200e3 # 200 billion
    elif mktcap == "large":
        mktcap_thres = 10e3 # 10 billion
    elif mktcap == "mid":
        mktcap_thres = 2e3 # 2 billion
    else:
        raise ValueError(f"Invalid market cap category: {mktcap}")
    return mktcap_thres