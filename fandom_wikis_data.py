def get_fandom_wikis_earning_data(get_new_data: bool, create_EarningRates_file: bool):
    import json
    
    if get_new_data:
        import requests
        response = requests.get('https://dragonvale.fandom.com/wiki/Data:EarningRates.json?action=raw')
        response.raise_for_status()
        EarningRates = json.loads(response.text)
    else:
        with open('EarningRates.json') as file:
            EarningRates = json.load(file)
    
    # fixing error is the data set
    # Note: Yolkwing, Holly, and Procyon all have incorrect earning tables at this point in time, but they aren't fixed here.
    earning_tuple_correction = {
        (6, 10, 13, 17, 21, 24, 28, 32, 35, 39, 42, 46, 50, 53, 57, 61, 64, 69, 72, 76): (6, 10, 13, 17, 21, 24, 28, 32, 35, 39, 42, 46, 50, 53, 57, 61, 64, 68, 72, 75), # Lotus, Smoulderbrush
        (6, 10, 13, 17, 21, 24, 28, 32, 35, 39, 43, 46, 50, 54, 57, 61, 65, 69, 73, 77): (6, 10, 13, 17, 21, 24, 28, 32, 35, 39, 43, 46, 50, 54, 57, 61, 65, 68, 72, 76), # Wraith
        (6, 10, 14, 17, 21, 25, 29, 32, 36, 40, 44, 47, 51, 55, 59, 63, 66, 70, 74, 77): (6, 10, 14, 17, 21, 25, 29, 33, 36, 40, 44, 47, 51, 55, 59, 63, 66, 70, 74, 78), # Acid
        (8, 12, 17, 21, 26, 30, 34, 39, 44, 48, 53, 57, 61, 66, 70, 75, 80, 84, 89, 93): (8, 12, 17, 21, 26, 30, 35, 39, 44, 48, 53, 57, 61, 66, 71, 75, 80, 84, 89, 93), # Arbor, Bouldershock, Crystal, Geode, Pollen, Sakura, Sonic, Soriak, Sumi, Willow
        (8, 12, 17, 21, 26, 30, 34, 39, 44, 48, 53, 57, 61, 66, 70, 75, 80, 84, 89, 93, 98): (8, 12, 17, 21, 26, 30, 35, 39, 44, 48, 53, 57, 61, 66, 71, 75, 80, 84, 89, 93, 98), # Fire, Ghostly Fire
        (8, 13, 18, 23, 27, 32, 37, 42, 47, 52, 56, 61, 66, 70, 75, 80, 85, 90, 94, 99): (8, 13, 18, 23, 27, 32, 37, 42, 47, 52, 56, 61, 66, 71, 76, 81, 85, 90, 95, 100), # Gamma
        (9, 14, 20, 25, 30, 36, 41, 47, 52, 57, 63, 68, 73, 78, 84, 89, 94, 100, 105, 110): (9, 14, 20, 25, 30, 36, 41, 47, 52, 57, 63, 68, 73, 79, 84, 90, 95, 100, 106, 111), # Daffadowndilly
        (10, 16, 21, 27, 33, 39, 45, 51, 57, 62, 68, 74, 80, 86, 90, 95, 104, 110, 116, 122): (10, 15, 21, 27, 32, 38, 44, 50, 55, 61, 67, 72, 78, 84, 90, 95, 101, 107, 112, 118), # Humuhumu
        (10, 16, 21, 27, 33, 39, 45, 51, 57, 62, 68, 74, 80, 86, 92, 98, 104, 110, 116, 122): (10, 16, 21, 27, 33, 39, 45, 51, 57, 62, 68, 74, 80, 86, 92, 98, 103, 109, 115, 121), # Cuddlewing, Honuhonu
        (11, 18, 25, 31, 38, 45, 52, 58, 65, 72, 79, 85, 92, 99, 105, 112, 119, 126, 133, 139): (11, 18, 25, 31, 38, 45, 52, 58, 65, 72, 79, 85, 92, 99, 105, 112, 119, 126, 132, 139), # Rosegold
        (13, 20, 28, 35, 43, 50, 57, 65, 73, 80, 88, 95, 102, 110, 117, 125, 133, 140, 148, 155): (13, 20, 28, 35, 43, 50, 57, 65, 73, 80, 88, 95, 103, 110, 118, 125, 133, 140, 148, 155), # Tulip
        (20, 32, 44, 56, 68, 80, 92, 104, 116, 128, 140, 152, 164, 176, 188, 201, 212, 224, 236, 248): (20, 32, 44, 56, 68, 80, 92, 104, 116, 128, 140, 153, 165, 177, 189, 201, 213, 225, 237, 249), # Fates, Mylio
        (32, 51, 69, 89, 107, 126, 145, 164, 183, 202, 221, 240, 259, 278, 297, 316, 335, 354, 373, 392): (32, 51, 69, 88, 107, 126, 145, 164, 183, 202, 221, 240, 259, 278, 297, 316, 335, 354, 373, 392), # Alayzem, Aquatech, Basket, Elegant, Euryale, Faux, Ichigo, Leviathan, Lightmare, Lightmatter, Lumineux, Lunis, Moriante, Nimue, Solis, Sprite
        (32, 52, 71, 91, 110, 130, 149, 169, 188, 208, 227, 246, 305, 266, 285, 324, 344, 363, 383, 402): (32, 52, 71, 91, 110, 130, 149, 169, 188, 208, 227, 246, 266, 285, 305, 324, 344, 363, 383, 402), # Chikipea, Corsair, Oasian, Regal, Rhinotorch
        (35, 56, 78, 99, 120, 141, 162, 184, 205, 226, 247, 268, 289, 311, 322, 353, 374, 395, 416, 438): (35, 56, 78, 99, 120, 141, 162, 184, 205, 226, 247, 268, 289, 311, 332, 353, 374, 395, 416, 438), # Bumi, Kann, Pollenizer, Zumi
        (38, 60, 83, 105, 128, 150, 172, 195, 218, 240, 263, 285, 307, 330, 352, 375, 398, 420, 443, 465): (38, 60, 83, 105, 127, 150, 173, 195, 217, 240, 263, 285, 308, 330, 353, 375, 398, 420, 443, 465), # Blossom, Burglehoo, Grace, Libretto, Lunk, Mantasu, Sugarplum, Sunscorch, Verglace, Yanghis
        (55, 87, 120, 153, 185, 218, 251, 284, 316, 249, 382, 415, 447, 480, 513, 545, 578, 611, 644, 676): (55, 87, 120, 153, 185, 218, 251, 284, 316, 349, 382, 415, 447, 480, 513, 545, 578, 611, 644, 676), # Alure, Crackle, Cupido, Elkar, Fuefuego, Fury, Glitz, Luck, Misfortune, Ocular, Redbeard, Tutan, Zipzap
        (63, 100, 138, 175, 213, 250, 288, 325, 363, 400, 438, 475, 512, 550, 587, 625, 663, 700, 738, 775): (63, 100, 138, 175, 213, 250, 288, 325, 363, 400, 438, 475, 512, 550, 588, 625, 663, 700, 738, 775), # Leap Year, Rainbow
        (63, 101, 139, 177, 215, 253, 291, 328, 366, 404, 442, 480, 518, 536, 594, 632, 669, 707, 745, 783): (63, 101, 139, 177, 215, 253, 291, 328, 366, 404, 442, 480, 518, 556, 594, 632, 669, 707, 745, 783), # Cherrie, Quaa, Singularity
    }
    
    for name, data in EarningRates['earningRates'].items():
        if data['Currency'] == 'DragonCash':
            earning_tuple = tuple(data['Rates'])
            if earning_tuple in earning_tuple_correction.keys(): EarningRates['earningRates'][name]['Rates'] = list(earning_tuple_correction[earning_tuple])
    
    if create_EarningRates_file:
        with open('EarningRates.json', 'w+') as file:
            json.dump(EarningRates, file, indent=4, separators=(',', ': '), sort_keys=True)
    
    return EarningRates