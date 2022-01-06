UBX_NAV = {
    b"\x01": "NAV-POSECEF",
    b"\x02": "NAV-POSLLH",
    b"\x07": "NAV-PVT",
    b"\x3c": "NAV-RELPOSNED"
}

UBX_RXM = {
    b"\x02": "RXM-MEASX",
    b"\x32": "RXM-RTCM"
}

UBX_ESF = {
    b"\x02": "ESF-MEAS",
    b"\x10": "ESF-STATUS"
}

UBX_SEC = {
    b"\x03": "SEC-UNIQID"
}