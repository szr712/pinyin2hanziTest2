def tone_equal(pred_tones, inp_tones):
    if len(pred_tones) != len(inp_tones):
        return False

    for x, y in zip(pred_tones, inp_tones):
        if x != 0 and x != y:
            return False
    return True