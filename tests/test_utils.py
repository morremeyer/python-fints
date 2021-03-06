import pytest
from fints.utils import decode_phototan_image


# HITAN3:
#  'challenge' contains a HHD 1.3 code embedded in the normal text payload
#  field.
#  Example: 'CHLGUC  00312908881344731012345678900515,00CHLGTEXT0292Sie haben eine ...'
#    The code in NeedTANResponse._parse_tan_challenge extracts
#     '2908881344731012345678900515,00'
#    from this, as a version 1.3 code. parse() should accept it
#    (start code: '88134473', IBAN: '1234567890', amount: '15,00')

# HITAN6:
# 'challenge' contains 4 fields:
#   2 bytes: mime type length
#   x bytes (see above): mime type
#   2 bytes: data length
#   y bytes: image data

CHALLENGE = b'\x00\timage/png\x0e\x82\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\xc8\x00\x00\x00\xc8\x08\x06\x00\x00\x00\xadX\xae\x9e\x00\x00\x00\x06bKGD\x00\xff\x00\xff\x00\xff\xa0\xbd\xa7\x93\x00\x00\x02MIDATx\x9c\xed\xdd\xb1\r\xc40\x0c\x04A\xea\xe1\xfe[\xf6w\xb0\x89\x023\x98\xa9@ \xb0Pxgf\xdeY\xec}W?o\xce9_?!\xb9\xdf\x9d\xdf\xd7\x0f\x80\xcd\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x1e;\xdaw\xdc\xef\xce\xf6\xfb\xf9A \x08\x04\x82@ \x08\x04\x82@ \x08\x04\x82@ \x08\x04\x82@ \x08\x04\x82@ \x08\x04\x82@ \x08\x04\x82@ \x08\x04\x82@ \x08\x04\x82@ \x08\x04\x82@ \x08\x04\x82@ \x08\x04\x82@ \x08\x04\x82@ \x08\x04\x82@ \x08\x04\x82@ \x08\x04\x82@ \x08\x04\x82@ \x08\x04\x82@ \x08\x04\x82@ \x9c\x99Y=T\xbd}G\xdb\x0e\xf9\x9d\xed\xf7\xf3\x83@\x10\x08\x04\x81@\x10\x08\x04\x81@\x10\x08\x04\x81@\x10\x08\x04\x81@\x10\x08\x04\x81@\x10\x08\x04\x81@\x10\x08\x04\x81@\x10\x08\x04\x81@\x10\x08\x04\x81@\x10\x08\x04\x81@\x10\x08\x04\x81@\x10\x08\x04\x81@\x10\x08\x04\x81@\x10\x08\x04\x81@\x10\x08\x04\x81@\x10\x08\x04\x81@\x10\x08\x04\x81@\x10\x08\x04\x81@\x10\x08\x04\x81@x\xech\xdfq\xbf;\xdb\xef\xe7\x07\x81 \x10\x08\x02\x81 \x10\x08\x02\x81 \x10\x08\x02\x81 \x10\x08\x02\x81 \x10\x08\x02\x81 \x10\x08\x02\x81 \x10\x08\x02\x81 \x10\x08\x02\x81 \x10\x08\x02\x81 \x10\x08\x02\x81 \x10\x08\x02\x81 \x10\x08\x02\x81 \x10\x08\x02\x81 \x10\x08\x02\x81 \x10\x08\x02\x81 \x10\x08\x02\x81 \x10\x08\x02\x81 \x10\x08\x02\x81 \x10\x08\x02\x81pff\xf5P\xf5\xf6\x1dm;\xe4w\xb6\xdf\xcf\x0f\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02\xe1\x0fp-(\x89A#\xd8\xc6\x00\x00\x00\x00IEND\xaeB`\x82'

def test_decode_phototan_image():
    data = decode_phototan_image(CHALLENGE)

    assert data["mime_type"] == "image/png"
    assert data["image"] == b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\xc8\x00\x00\x00\xc8\x08\x06\x00\x00\x00\xadX\xae\x9e\x00\x00\x00\x06bKGD\x00\xff\x00\xff\x00\xff\xa0\xbd\xa7\x93\x00\x00\x02MIDATx\x9c\xed\xdd\xb1\r\xc40\x0c\x04A\xea\xe1\xfe[\xf6w\xb0\x89\x023\x98\xa9@ \xb0Pxgf\xdeY\xec}W?o\xce9_?!\xb9\xdf\x9d\xdf\xd7\x0f\x80\xcd\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x1e;\xdaw\xdc\xef\xce\xf6\xfb\xf9A \x08\x04\x82@ \x08\x04\x82@ \x08\x04\x82@ \x08\x04\x82@ \x08\x04\x82@ \x08\x04\x82@ \x08\x04\x82@ \x08\x04\x82@ \x08\x04\x82@ \x08\x04\x82@ \x08\x04\x82@ \x08\x04\x82@ \x08\x04\x82@ \x08\x04\x82@ \x08\x04\x82@ \x08\x04\x82@ \x08\x04\x82@ \x08\x04\x82@ \x08\x04\x82@ \x9c\x99Y=T\xbd}G\xdb\x0e\xf9\x9d\xed\xf7\xf3\x83@\x10\x08\x04\x81@\x10\x08\x04\x81@\x10\x08\x04\x81@\x10\x08\x04\x81@\x10\x08\x04\x81@\x10\x08\x04\x81@\x10\x08\x04\x81@\x10\x08\x04\x81@\x10\x08\x04\x81@\x10\x08\x04\x81@\x10\x08\x04\x81@\x10\x08\x04\x81@\x10\x08\x04\x81@\x10\x08\x04\x81@\x10\x08\x04\x81@\x10\x08\x04\x81@\x10\x08\x04\x81@\x10\x08\x04\x81@\x10\x08\x04\x81@x\xech\xdfq\xbf;\xdb\xef\xe7\x07\x81 \x10\x08\x02\x81 \x10\x08\x02\x81 \x10\x08\x02\x81 \x10\x08\x02\x81 \x10\x08\x02\x81 \x10\x08\x02\x81 \x10\x08\x02\x81 \x10\x08\x02\x81 \x10\x08\x02\x81 \x10\x08\x02\x81 \x10\x08\x02\x81 \x10\x08\x02\x81 \x10\x08\x02\x81 \x10\x08\x02\x81 \x10\x08\x02\x81 \x10\x08\x02\x81 \x10\x08\x02\x81 \x10\x08\x02\x81 \x10\x08\x02\x81pff\xf5P\xf5\xf6\x1dm;\xe4w\xb6\xdf\xcf\x0f\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02A \x10\x04\x02\xe1\x0fp-(\x89A#\xd8\xc6\x00\x00\x00\x00IEND\xaeB`\x82'
