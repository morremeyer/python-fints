import time

from fints.utils import fints_escape

from . import FinTS3SegmentOLD, FinTS3Segment
from fints.formals import ReferenceMessage, SecurityProfile, SecurityRole, SecurityIdentificationDetails, SecurityDateTime, EncryptionAlgorithm, KeyName, CompressionFunction, Certificate, SecurityApplicationArea, HashAlgorithm, SignatureAlgorithm, UserDefinedSignature
from fints.fields import DataElementGroupField, DataElementField, ZeroPaddedNumericField, CodeField, SegmentSequenceField

class HNHBK3(FinTS3Segment):
    "Nachrichtenkopf"
    message_size = ZeroPaddedNumericField(length=12, _d="Größe der Nachricht (nach Verschlüsselung und Komprimierung)")
    hbci_version = DataElementField(type='num', max_length=3, _d="HBCI-Version")
    dialogue_id = DataElementField(type='id', _d="Dialog-ID")
    message_number = DataElementField(type='num', max_length=4, _d="Nachrichtennummer")
    reference_message = DataElementGroupField(type=ReferenceMessage, required=False, _d="Bezugsnachricht")

class HNHBS1(FinTS3Segment):
    "Nachrichtenabschluss"
    message_number = DataElementField(type='num', max_length=4, _d="Nachrichtennummer")


class HNHBK(FinTS3SegmentOLD):
    """
    HNHBK (Nachrichtenkopf)
    Section B.5.2
    """
    type = 'HNHBK'
    version = 3

    HEADER_LENGTH = 29

    def __init__(self, msglen, dialogid, msgno):

        if len(str(msglen)) != 12:
            msglen = str(int(msglen) + self.HEADER_LENGTH + len(str(dialogid)) + len(str(msgno))).zfill(12)

        data = [
            msglen,
            300,
            dialogid,
            msgno
        ]
        super().__init__(1, data)


class HNSHK(FinTS3SegmentOLD):
    """
    HNSHK (Signaturkopf)
    Section B.5.1
    """
    type = 'HNSHK'
    version = 4

    SECURITY_FUNC = 999
    SECURITY_BOUNDARY = 1  # SHM
    SECURITY_SUPPLIER_ROLE = 1  # ISS

    def __init__(self, segno, secref, blz, username, systemid, profile_version, security_function=SECURITY_FUNC):
        data = [
            ':'.join(['PIN', str(profile_version)]),
            security_function,
            secref,
            self.SECURITY_BOUNDARY,
            self.SECURITY_SUPPLIER_ROLE,
            ':'.join(['1', '', fints_escape(str(systemid))]),
            1,
            ':'.join(['1', time.strftime('%Y%m%d'), time.strftime('%H%M%S')]),
            ':'.join(['1', '999', '1']),  # Negotiate hash algorithm
            ':'.join(['6', '10', '16']),  # RSA mode
            ':'.join([str(self.country_code), blz, username, 'S', '0', '0']),
        ]
        super().__init__(segno, data)


class HNVSK(FinTS3SegmentOLD):
    """
    HNVSK (Verschlüsslungskopf)
    Section B.5.3
    """
    type = 'HNVSK'
    version = 3

    COMPRESSION_NONE = 0
    SECURITY_SUPPLIER_ROLE = 1  # ISS

    def __init__(self, segno, blz, username, systemid, profile_version):
        data = [
            ':'.join(['PIN', str(profile_version)]),
            998,
            self.SECURITY_SUPPLIER_ROLE,
            ':'.join(['1', '', fints_escape(str(systemid))]),
            ':'.join(['1', time.strftime('%Y%m%d'), time.strftime('%H%M%S')]),
            ':'.join(['2', '2', '13', '@8@00000000', '5', '1']),  # Crypto algorithm
            ':'.join([str(self.country_code), blz, username, 'S', '0', '0']),
            self.COMPRESSION_NONE
        ]
        super().__init__(segno, data)


class HNVSD(FinTS3SegmentOLD):
    """
    HNVSD (Verschlüsselte Daten)
    Section B.5.4
    """
    type = 'HNVSD'
    version = 1

    def __init__(self, segno, encoded_data):
        self.encoded_data = encoded_data
        data = [
            '@{}@{}'.format(len(encoded_data), encoded_data)
        ]
        super().__init__(segno, data)

    def set_data(self, encoded_data):
        self.encoded_data = encoded_data
        self.data = [
            '@{}@{}'.format(len(encoded_data), encoded_data)
        ]


class HNSHA(FinTS3SegmentOLD):
    """
    HNSHA (Signaturabschluss)
    Section B.5.2
    """
    type = 'HNSHA'
    version = 2

    SECURITY_FUNC = 999
    SECURITY_BOUNDARY = 1  # SHM
    SECURITY_SUPPLIER_ROLE = 1  # ISS
    PINTAN_VERSION = 1  # 1-step

    def __init__(self, segno, secref, pin, tan=None):
        pintan = fints_escape(pin)
        if tan:
            pintan += ':' + fints_escape(tan)
        data = [
            secref,
            '',
            pintan,
        ]
        super().__init__(segno, data)


class HNHBS(FinTS3SegmentOLD):
    """
    HNHBS (Nachrichtenabschluss)
    Section B.5.3
    """
    type = 'HNHBS'
    version = 1

    def __init__(self, segno, msgno):
        data = [
            str(msgno)
        ]
        super().__init__(segno, data)

class HNVSK3(FinTS3Segment):
    """Verschlüsselungskopf, version 3

    Source: FinTS Financial Transaction Services, Sicherheitsverfahren HBCI"""
    security_profile = DataElementGroupField(type=SecurityProfile, _d="Sicherheitsprofil")
    security_function = DataElementField(type='code', max_length=3, _d="Sicherheitsfunktion, kodiert")
    security_role = CodeField(SecurityRole, max_length=3, _d="Rolle des Sicherheitslieferanten, kodiert")
    security_identification_details = DataElementGroupField(type=SecurityIdentificationDetails, _d="Sicherheitsidentifikation, Details")
    security_datetime = DataElementGroupField(type=SecurityDateTime, _d="Sicherheitsdatum und -uhrzeit")
    encryption_algorithm = DataElementGroupField(type=EncryptionAlgorithm, _d="Verschlüsselungsalgorithmus")
    key_name = DataElementGroupField(type=KeyName, _d="Schlüsselname")
    compression_function = CodeField(CompressionFunction, max_length=3, _d="Komprimierungsfunktion")
    certificate = DataElementGroupField(type=Certificate, required=False, _d="Zertifikat")

class HNVSD1(FinTS3Segment):
    """Verschlüsselte Daten, version 1

    Source: FinTS Financial Transaction Services, Sicherheitsverfahren HBCI"""
    data = SegmentSequenceField(_d="Daten, verschlüsselt")

class HNSHK4(FinTS3Segment):
    """Signaturkopf, version 4

    Source: FinTS Financial Transaction Services, Sicherheitsverfahren HBCI"""
    security_profile = DataElementGroupField(type=SecurityProfile, _d="Sicherheitsprofil")
    security_function = DataElementField(type='code', max_length=3, _d="Sicherheitsfunktion, kodiert")
    security_reference = DataElementField(type='an', max_length=14, _d="Sicherheitskontrollreferenz")
    security_application_area = CodeField(SecurityApplicationArea, max_length=3, _d="Bereich der Sicherheitsapplikation, kodiert")
    security_role = CodeField(SecurityRole, max_length=3, _d="Rolle des Sicherheitslieferanten, kodiert")
    security_identification_details = DataElementGroupField(type=SecurityIdentificationDetails, _d="Sicherheitsidentifikation, Details")
    security_reference_number = DataElementField(type='num', max_length=16, _d="Sicherheitsreferenznummer")
    security_datetime = DataElementGroupField(type=SecurityDateTime, _d="Sicherheitsdatum und -uhrzeit")
    hash_algorithm = DataElementGroupField(type=HashAlgorithm, _d="Hashalgorithmus")
    signature_algorithm = DataElementGroupField(type=SignatureAlgorithm, _d="Signaturalgorithmus")
    key_name = DataElementGroupField(type=KeyName, _d="Schlüsselname")
    certificate = DataElementGroupField(type=Certificate, required=False, _d="Zertifikat")

class HNSHA2(FinTS3Segment):
    """Signaturabschluss, version 2

    Source: FinTS Financial Transaction Services, Sicherheitsverfahren HBCI"""
    security_reference = DataElementField(type='an', max_length=14, _d="Sicherheitskontrollreferenz")
    validation_result = DataElementField(type='bin', max_length=512, required=False, _d="Validierungsresultat")
    user_defined_signature = DataElementGroupField(type=UserDefinedSignature, required=False, _d="Benutzerdefinierte Signatur")

