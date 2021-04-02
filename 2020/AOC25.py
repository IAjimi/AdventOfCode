''' Can't complete part 2 because did not get all 50 stars!'''

def calc_public_key(sn, public_key):
    val = 1
    n = 0
    
    while n >= 0:
        n += 1
        val = val * sn % 20201227
        
        if val == public_key:
            return n
    
def calc_encryption_key(sn, loopsize):
    val = 1
    
    for n in range(loopsize):
        val = val * sn % 20201227
        
    return val

def get_encryption_key(sn, card_pk, door_pl):
    card_loopsize = get_public_key(sn, card_pk) # 17188728 
    door_loopsize = get_public_key(sn, door_pl) # 8419519
    encryption_key = calc_encryption_key(card_loopsize, door_pl)
    return encryption_key

if __name__ == "__main__":
    print("PART 1")
    encryption_key = get_encryption_key(7, 14082811, 5249543) # 3217885
    print("")
    print("PART 2")

