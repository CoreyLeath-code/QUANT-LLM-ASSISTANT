from scipy.stats import ks_2samp

def detect_embedding_drift(reference, live):
    stat, p_value = ks_2samp(reference, live)
    return p_value < 0.05
