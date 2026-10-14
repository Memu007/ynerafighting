// Portable single-file build for opening the game without an asset directory.
const fs=require('fs'),path=require('path');
const root=path.join(__dirname,'..');
const source=fs.readFileSync(path.join(root,'index.html'),'utf8');
const html=source.replace(/assets\/portraits\/[a-z]+\.png/g,file=>'data:image/png;base64,'+fs.readFileSync(path.join(root,file)).toString('base64'));
fs.writeFileSync(path.join(root,'conurbano-fighter.html'),html);
fs.writeFileSync(path.join(root,'conurbano-fighter-codigo.txt'),source);
console.log('Built portable HTML and matching TXT source');
