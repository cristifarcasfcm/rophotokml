#!/usr/bin/env python3
"""Configurează proiectul iOS (idempotent): Info.plist, iPhone-only, PrivacyInfo.xcprivacy în proiectul Xcode.
Rulare din rădăcină:  python3 scripts/configure_ios.py
"""
import os, plistlib, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PLIST = os.path.join(ROOT, "ios/App/App/Info.plist")
PBX = os.path.join(ROOT, "ios/App/App.xcodeproj/project.pbxproj")

with open(PLIST, "rb") as f:
    pl = plistlib.load(f)

pl["CFBundleDisplayName"] = "ROPhotoKml"
pl["NSCameraUsageDescription"] = "Camera este folosită pentru fotografierea parcelelor agricole în timpul controlului pe teren."
pl["NSLocationWhenInUseUsageDescription"] = "Locația este folosită pentru a afișa poziția ta pe hartă, a verifica apropierea de parcelă și a înscrie coordonatele GPS în fotografii."
pl["NSPhotoLibraryAddUsageDescription"] = "Aplicația salvează în galeria telefonului fotografiile făcute cu ROPhotoKml, pentru rapoartele de control."
pl["NSPhotoLibraryUsageDescription"] = "Aplicația salvează în galeria telefonului fotografiile făcute cu ROPhotoKml, pentru rapoartele de control."
pl["NSMotionUsageDescription"] = "Senzorii de mișcare sunt folosiți pentru busolă (direcția în care este făcută fotografia)."
pl["ITSAppUsesNonExemptEncryption"] = False  # doar HTTPS standard -> fără declarații suplimentare de export
pl["UIRequiredDeviceCapabilities"] = ["arm64"]
pl["UISupportedInterfaceOrientations"] = ["UIInterfaceOrientationPortrait"]
pl.pop("UISupportedInterfaceOrientations~ipad", None)

kml_uti = "com.google.earth.kml"
pl["UTImportedTypeDeclarations"] = [{
    "UTTypeIdentifier": kml_uti,
    "UTTypeDescription": "Fișier KML (Google Earth)",
    "UTTypeConformsTo": ["public.xml", "public.data"],
    "UTTypeTagSpecification": {
        "public.filename-extension": ["kml"],
        "public.mime-type": ["application/vnd.google-earth.kml+xml"],
    },
}]
pl["CFBundleDocumentTypes"] = [{
    "CFBundleTypeName": "KML",
    "CFBundleTypeRole": "Viewer",
    "LSHandlerRank": "Alternate",
    "LSItemContentTypes": [kml_uti],
}]
pl["LSSupportsOpeningDocumentsInPlace"] = False

with open(PLIST, "wb") as f:
    plistlib.dump(pl, f)
print("Info.plist actualizat")

pbx = open(PBX, encoding="utf-8").read()
pbx = re.sub(r'TARGETED_DEVICE_FAMILY = "1,2";', 'TARGETED_DEVICE_FAMILY = 1;', pbx)

REF, BUILD = "A1B2C3D4E5F6071829384A01", "A1B2C3D4E5F6071829384A02"
if "PrivacyInfo.xcprivacy" not in pbx:
    pbx = pbx.replace("/* End PBXBuildFile section */",
        f"\t\t{BUILD} /* PrivacyInfo.xcprivacy in Resources */ = {{isa = PBXBuildFile; fileRef = {REF} /* PrivacyInfo.xcprivacy */; }};\n/* End PBXBuildFile section */")
    pbx = pbx.replace("/* End PBXFileReference section */",
        f"\t\t{REF} /* PrivacyInfo.xcprivacy */ = {{isa = PBXFileReference; lastKnownFileType = text.xml; path = PrivacyInfo.xcprivacy; sourceTree = \"<group>\"; }};\n/* End PBXFileReference section */")
    pbx = pbx.replace("\t\t\t\t2FAD9762203C412B000D30F8 /* config.xml */,\n\t\t\t\t50B271D01FEDC1A000F3C39B /* public */,",
        f"\t\t\t\t2FAD9762203C412B000D30F8 /* config.xml */,\n\t\t\t\t{REF} /* PrivacyInfo.xcprivacy */,\n\t\t\t\t50B271D01FEDC1A000F3C39B /* public */,")
    # Resources build phase
    m = re.search(r"(/\* Resources \*/ = \{\s*isa = PBXResourcesBuildPhase;\s*buildActionMask = \d+;\s*files = \(\n)", pbx)
    assert m, "Resources phase negăsit"
    pbx = pbx[:m.end()] + f"\t\t\t\t{BUILD} /* PrivacyInfo.xcprivacy in Resources */,\n" + pbx[m.end():]
    print("PrivacyInfo.xcprivacy adăugat în proiect")
open(PBX, "w", encoding="utf-8").write(pbx)
