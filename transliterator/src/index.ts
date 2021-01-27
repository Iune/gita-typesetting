import { Telugu } from 'lipitva/dist/scripts/brahmic/Telugu';
import { Iast } from 'lipitva/dist/scripts/roman/Iast';
import { Itrans } from 'lipitva/dist/scripts/roman/Itrans';
import { ScriptMap, transliterate } from 'lipitva/dist/transliterate';
import { createWriteStream, readFileSync } from 'fs';
import * as yargs from 'yargs';

type Sloka = {
    lines: string[]
}

function loadSlokas(inputFilePath: string): Sloka[] {
    const lines = readFileSync(inputFilePath, 'utf-8')
        .split('\n')
        .filter((line: string) => !line.startsWith('#'));

    let slokas: Sloka[] = [];
    let currentLines: string[] = [];

    lines.forEach((line: string, idx: number) => {
        if (line.trim().length > 0) {
            currentLines.push(line.trim());
        }
        if (line.trim().length == 0 || idx == lines.length - 1) {
            slokas.push({ lines: currentLines });
            currentLines = [];
        }
    });

    return slokas;
}

function convertSlokas(slokas: Sloka[], scriptMap: ScriptMap, sanitize: boolean = false) {
    function sanitizeLine(line: string): string {
        if (sanitize) { return line.replace('-', '').replace('·', ' '); }
        else { return line; }
    }

    return slokas.map((sloka: Sloka) => {
        return {
            lines: sloka.lines.map((line: string) => {
                return transliterate({
                    data: sanitizeLine(line),
                    scriptMap: scriptMap
                });
            })
        }
    })
}

function writeTex(outputFilePath: string, slokas: Sloka[], latexCommand: string,
    chapter: string = '', displayHeaders: boolean = false, splitFirstSloka: boolean = false) {
    function lineToTex(iast: Sloka): string {
        let lines: string[] = [];
        for (let idx = 0; idx < iast.lines.length; idx++) {
            const line = iast.lines[idx].replace('~', '\\textasciitilde{}');

            let lineEnding: string;
            if (idx != iast.lines.length - 1) { lineEnding = ' \\\\'; }
            else { lineEnding = ''; }

            lines.push(`\\${latexCommand}{${line}}${lineEnding}`);
        }

        return lines.join('\n');
    }

    const file = createWriteStream(outputFilePath, { flags: 'w' });
    for (let idx = 0; idx < slokas.length; idx++) {
        if (displayHeaders && chapter.length > 0) {
            file.write(`\\subsection*{${chapter}.${idx}}\n`);
        }

        // Table header
        file.write(`\\begin{table}[H]\n`);
        file.write(`\\begin{tabular}{l}\n`)
        // Table rows
        file.write(`${lineToTex(slokas[idx])}\n`);
        // Table footer
        file.write(`\\end{tabular}\n`);
        file.write(`\\end{table}\n\n`);

        if (splitFirstSloka && idx == 0) {
            file.write(`\\newpage\n\n`);
        }
    }

    file.end();
}

function parseArgs() {
    return yargs
        .version()
        .option('slokas', {
            alias: 's',
            demandOption: true,
            description: 'Text file containing slokas',
            type: 'string'
        })
        .option('chapter', {
            alias: 'c',
            demandOption: true,
            description: 'Bhagavad Gita chapter',
            type: 'string'
        })
        .option('iast', {
            alias: 'i',
            demandOption: true,
            description: 'Output IAST .tex file path',
            default: 'output.iast.tex',
            type: 'string'
        })
        .option('telugu', {
            alias: 't',
            demandOption: true,
            description: 'Output Telugu .tex file path',
            default: 'output.telugu.tex',
            type: 'string'
        })
        .option('headers', {
            description: 'Disable sloka numbering',
            default: true,
            type: 'boolean'
        })
        .option('split-first-sloka', {
            description: 'Whether to add \\newline after first sloka',
            default: false,
            type: 'boolean'
        })
        .argv
}

function main() {
    const args = parseArgs();
    const slokas = loadSlokas(args.slokas);
    const iastSlokas = convertSlokas(slokas, new ScriptMap({ fromScript: Itrans, toScript: Iast }), false);
    const teluguSlokas = convertSlokas(slokas, new ScriptMap({ fromScript: Itrans, toScript: Telugu }), true);
    writeTex(args.telugu, teluguSlokas, 'natline', args.chapter, args['headers'], args['split-first-sloka']);
    writeTex(args.iast, iastSlokas, 'romline', args.chapter, args['headers'], args['split-first-sloka']);
}

main()