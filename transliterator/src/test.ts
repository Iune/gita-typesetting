import { Devanagari } from 'lipitva/dist/scripts/brahmic/Devanagari';
import { Hk } from 'lipitva/dist/scripts/roman/Hk';
import { Iast } from 'lipitva/dist/scripts/roman/Iast';
import { Itrans } from 'lipitva/dist/scripts/roman/Itrans';
import { Kolkata } from 'lipitva/dist/scripts/roman/Kolkata';
import { Titus } from 'lipitva/dist/scripts/roman/Titus';
import { Slp1 } from 'lipitva/dist/scripts/roman/Slp1';
import { Velthuis } from 'lipitva/dist/scripts/roman/Velthuis';
import { Wx } from 'lipitva/dist/scripts/roman/Wx';
import { ScriptMap, transliterate } from 'lipitva/dist/transliterate';
import { RomanScriptDefinition } from 'lipitva/dist/scripts/roman/base';

const toScripts = [
    Hk,
    Iast,
    Itrans,
    Kolkata,
    Slp1,
    Titus,
    Velthuis,
    Wx
]

toScripts.forEach((outputScript: RomanScriptDefinition) => {
    console.log(`Script: ${outputScript.name}: ${transliterate({
        data: 'अग्निमीळे पुरोहितं यज्ञस्य देवमृत्विजम् आदित्य डुरि सम्',
        scriptMap: new ScriptMap({
            fromScript: Devanagari,
            toScript: outputScript
        })
    })}`);
});