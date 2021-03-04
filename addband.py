#!/usr/bin/bash

import binascii
import PN532

nfc = PN532.PN532("/dev/ttyAMA0", 115200)
nfc.begin()
nfc.SAM_configuration()

print("Place a band to add it to the registered bands list")

file = open("bands.txt", "a")

while True:
    uid = nfc.read_passive_target()
    if uid is "no_card":
        continue
    else:
        print("Found " + binascii.hexlify(uid))
        file.write(binascii.hexlify(uid) + "\n")

        x = str(input("Add another card? [Y/N] "))

        if x.lower() == "y":
            continue
        else:
            file.close()
            break
